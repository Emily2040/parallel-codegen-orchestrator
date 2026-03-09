# Planning Module

Use this module to produce a dependency-aware implementation plan.

## Goal

Transform a user request into a compact `ProjectPlan` JSON object that is useful for execution, recovery, and verification.

## Planning algorithm

1. **Extract acceptance criteria**
   - What must exist when the task is done?
   - What language, framework, or runtime is implied?
   - Are there tests, migrations, or deployment concerns?

2. **Identify repository grounding**
   - Use the user’s actual paths, file names, and symbols when available.
   - If there is no repository context, choose conventional paths and say they are assumptions.

3. **Choose module boundaries**
   Split by:
   - File ownership
   - Interface boundary
   - Domain responsibility
   - Verification strategy

   Avoid splitting one logical unit into fake fragments just to make more modules.

4. **Freeze interfaces**
   Before parallel work, define:
   - Shared types
   - Function signatures
   - API routes
   - Database contracts
   - Event payloads
   - Environment variables

   Put unstable contracts into an earlier module if needed.

5. **Assign dependencies**
   Every module dependency must answer: “What concrete thing must exist first?”

6. **Decide parallelization**
   Mark `can_parallelize: true` only when:
   - Dependencies are satisfied
   - Interfaces are frozen
   - File ownership does not overlap
   - A later integration pass is possible

7. **Build execution waves**
   Group only truly independent modules into the same wave.
   Each wave should be topologically valid.

8. **Attach verification**
   Every module must include at least one verification path:
   - Unit test
   - Integration test
   - Static check
   - Manual validation command

## Required planning behaviors

- Prefer fewer, stronger modules over many weak ones.
- Use real file paths.
- Keep descriptions concrete.
- Name assumptions and risks.
- If the task is small, use a mini plan instead of full orchestration.

## Output contract

Emit `ProjectPlan` JSON that validates against `schemas/plan.schema.json`.

### Planning quality bar

A good plan lets another engineer answer these questions quickly:
- What will be built?
- In what order?
- What can run in parallel?
- Where are the risky seams?
- How will we know it works?

If the plan cannot answer those, it is fluff. Fix it.
