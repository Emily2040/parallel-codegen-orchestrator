# Redesign Notes

This repository is a first-principles refactor of a monolithic “unbreakable code generation prompt” into a portable skill.

## Why the original prompt was brittle

The original prompt had a few useful instincts:
- state tracking
- modular work
- resumability
- verification intent

But it wrapped them in brittle mechanics that tend to fail in real agent systems:

1. **Arbitrary line quotas**
   Requiring 1000+ lines encourages filler, duplicated logic, and ornamental complexity. Code should be sized by the requirement, not by ritual.

2. **Massive state object on every turn**
   A giant JSON blob in every response wastes context and increases instruction drift. State should be compact and only emitted when the task truly spans turns.

3. **Mid-line truncation as a feature**
   Forcing outputs to run into the interface wall is fragile. Recovery should restart from stable boundaries, not from a guessed half-token.

4. **Fake or unverifiable hashes**
   Requiring hashes and checksums in conversational turns is only valid if they are actually computed from visible artifacts. Otherwise it becomes theater.

5. **Single-module-only generation**
   That blocks legitimate parallel work. A dependency graph with waves is a better abstraction.

6. **Approval-heavy choreography**
   Some tasks do need a planning checkpoint, but not every substantial task needs a ceremonial stop sign.

## What changed

### 1) The big GSO became three small contracts
Instead of one giant state machine object in every reply, the skill uses:
- `ProjectPlan`
- `ProgressUpdate`
- `FinalReport`

That lowers context cost and makes recovery easier.

### 2) “Continue from the last character” became “resume from stable anchors”
Recovery now uses:
- file boundaries
- symbol boundaries
- patch hunks
- artifact digests

That is much more resilient.

### 3) Monolithic sequencing became DAG + execution waves
The skill plans real dependencies and allows safe parallel waves when interfaces are frozen and file ownership does not overlap.

### 4) Output volume targets became acceptance criteria
The redesign optimizes for:
- correctness
- grounded file ownership
- tests
- integration safety
- truthful verification

### 5) Prompt theater became repository-quality skill design
This repo follows a portable skill layout:
- compact root `SKILL.md`
- orchestrator
- modular core files
- wrappers for multiple agents
- JSON schemas
- validator
- CI workflow
- anti-slop registry

## Async and parallel stance

Parallelism is now explicit and conditional.

Safe parallel work requires:
- satisfied dependencies
- frozen interfaces
- non-overlapping file ownership
- a later serialized integration pass

If a platform supports concurrent tools or sub-agents, the same wave can run asynchronously. If not, the plan still works sequentially without pretending secret work happened.

## Bottom line

The new skill is less theatrical, more portable, and more truthful. It trades “unbreakable industrial-grade prompt” energy for something much closer to actual engineering discipline.
