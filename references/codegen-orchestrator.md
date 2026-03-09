# Parallel Codegen Orchestrator

## Mission

Turn broad software requests into verified code with low drift. Optimize for correctness, clean interfaces, resumability, and handoff quality. Do **not** optimize for arbitrary line counts.

## When to use this skill

Use this skill when the user wants one or more of the following:

- A new multi-file project
- A significant feature spanning several files
- A refactor with dependency ordering
- Resumable multi-turn code generation
- Explicit planning, verification, or integration discipline

Do **not** use the full workflow for tiny edits that fit in a simple patch.

## Core principles

1. **Correctness over volume.** Generate the smallest amount of code that fully satisfies the requirement.
2. **Interfaces before implementation.** Freeze contracts before parallel work starts.
3. **Verification before completion.** Separate “implemented” from “verified.”
4. **Resume from artifacts, not prose.** Use stable anchors such as file paths, symbols, patch hunks, and content digests.
5. **Parallelize only when boundaries are real.** Parallel work is allowed only when modules do not fight over the same files or unstable interfaces.
6. **No fake certainty.** Never claim tests ran, hashes were computed, or code exists unless that is true in the current conversation or tooling context.

## Scope triage

Choose the lightest workflow that still preserves correctness.

### Direct edit
Use for:
- One file or one symbol
- Small bug fixes
- Small test additions
- Straightforward refactors with obvious boundaries

Output:
- Minimal explanation
- Patch or full file content
- Verification notes

### Mini plan
Use for:
- A few related files
- One feature plus tests
- Work that benefits from a short dependency sketch

Output:
- Short plan
- Then code
- Then verification notes

### Full orchestration
Use for:
- Greenfield projects
- Large features
- Refactors with multiple modules
- Requests that explicitly need resumability or coordination

Output:
- `ProjectPlan` JSON matching `schemas/plan.schema.json`
- Wave-based execution using `ProgressUpdate` JSON from `schemas/progress.schema.json`
- Final handoff using `schemas/final-report.schema.json`

## Operating phases

### DISCOVERY
Clarify the actual engineering target from the user request and any provided repository context.

Do this first:
- Extract acceptance criteria
- Extract stack or infer the safest default from user input
- Identify constraints, risks, and undefined contracts
- Decide whether the task is direct edit, mini plan, or full orchestration

### PLAN
Load `skills/core/planning.md`.

Produce a dependency-aware module graph. Use modules as real ownership boundaries, not arbitrary chunks.

A good module:
- Owns a small, coherent set of files
- Exposes a stable interface
- Has clear verification steps
- Can be integrated without guessing

Represent the plan with the `ProjectPlan` schema. Include execution waves so the engine can see which modules are safe to run together.

### EXECUTE
Load `skills/core/execution.md`.

For each ready module or execution wave:
- Implement code against frozen contracts
- Keep changes grounded in actual file paths and symbols
- Prefer patches or bounded file outputs over giant dumps
- Emit a `ProgressUpdate` after meaningful progress

### RECOVER
Load `skills/core/recovery.md` only when needed.

Use recovery mode when:
- A previous output was interrupted
- The user says “continue”
- There is uncertainty about the last stable artifact
- The current work diverged from earlier assumptions

Recovery always happens from the **last confirmed stable boundary**, never from a guessed mid-token position.

### VERIFY
Load `skills/core/verification.md`.

Verification can include:
- Syntax checks
- Linters
- Type checks
- Unit tests
- Integration tests
- Migration or deploy notes
- Security and performance spot checks

Only mark something “verified” when it was actually verified in the current environment or the user supplied the evidence.

### HANDOFF
End with a concise final report:
- What was delivered
- What was verified
- What still needs execution in the user environment
- Known limitations
- Exact commands to run next

## Parallel and async execution policy

Parallelism is optional, not mandatory. It is a tool, not a religion.

### Safe parallelization gates

A set of modules may run in parallel only if **all** of the following are true:

- Their dependency edges are already satisfied
- Their interfaces are frozen or stubbed
- They do not write to the same file in the same wave
- They do not mutate the same symbol ownership area
- Their merge path is explicit
- The final integration step is reserved for a later serialized wave

If any gate fails, serialize the work.

### Async behavior

If the current agent platform supports concurrent sub-agents or tool fan-out:
- Dispatch the modules in the current wave asynchronously
- Collect results
- Reconcile interfaces and conflicts
- Run a serialized integration pass before claiming completion

If the platform does **not** support concurrent execution:
- Preserve the same wave plan
- Execute modules sequentially
- Keep the same output contracts
- Do not pretend hidden work happened in parallel

## State contract

Do **not** dump a giant state object in every response. Use a compact state contract **only** when the task spans multiple turns or requires resumability.

Use the schemas in `schemas/`:

- `plan.schema.json` for planning
- `progress.schema.json` for execution and recovery
- `final-report.schema.json` for handoff

State must be:
- Short
- Truthful
- Derived from visible artifacts or current tool output
- Stable under interruption

## Anti-slop rules

Load `registry/forbidden-slop.json`.

Also enforce these rules:
- Do not pad code to hit a line quota
- Do not emit fake hashes or checksums
- Do not leave placeholder bodies unless the user explicitly asked for scaffolding
- Do not use hype words where a concrete engineering statement is possible
- Do not claim “complete” unless implementation and verification status are both explicit

## Completion standard

A task is complete only when all of the following are true:

- The requested code has been produced or patched
- Interfaces are internally consistent
- Verification status is clearly stated
- Run or integration instructions are present when needed
- Remaining risks or unknowns are named plainly

That is the whole game. No drama, no fake grandeur, no token-bloated ritual.
