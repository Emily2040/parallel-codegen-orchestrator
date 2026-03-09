# Execution Module

Use this module to implement one ready module or one safe execution wave.

## Goal

Produce code grounded in the plan, then emit a `ProgressUpdate` JSON object that makes recovery easy.

## Execution rules

1. **Honor the plan unless reality changed**
   - If the repository context or user feedback invalidates the plan, revise the plan first.
   - Do not quietly drift.

2. **Implement against frozen contracts**
   - Shared interfaces must not mutate casually mid-wave.
   - If a contract must change, update the plan and affected modules explicitly.

3. **Prefer bounded outputs**
   Use:
   - Patch hunks
   - Full file outputs for small files
   - Focused module batches

   Avoid giant monolithic dumps when smaller units make recovery easier.

4. **Own your file scope**
   A module should touch only the files assigned to it unless a legitimate dependency requires more.

5. **Include verification hooks**
   Alongside implementation, include:
   - Tests
   - Commands
   - Notes on what was not run

6. **Emit progress state**
   After meaningful completion, emit `ProgressUpdate` JSON:
   - `module_id`
   - `status`
   - `files_touched`
   - `resume_anchor`
   - `verification`
   - `next_actions`

## Parallel wave execution

When the current platform supports real concurrency:
- Dispatch all modules in the wave asynchronously
- Keep outputs separated by module
- Join results before integration
- Reconcile any contract drift immediately

When the platform does not support real concurrency:
- Execute modules in the same wave sequentially
- Preserve the same module boundaries and contracts
- Do not pretend anything happened in the background

## Resume anchors

Every progress update should include a stable anchor. Prefer one of these:
- `file_boundary`: the whole file is complete
- `symbol_boundary`: a class, function, or section is complete
- `patch_hunk`: a specific patch region is complete
- `artifact_digest`: content digest of a complete visible artifact

Choose the strongest anchor that is true.

## Never do these

- Do not chase arbitrary line counts
- Do not continue from a guessed mid-character position
- Do not emit fake checksums
- Do not mark a module done without naming the verification state
- Do not let two parallel modules fight over the same file

That path leads to nonsense and broken merges.
