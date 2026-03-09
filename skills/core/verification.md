# Verification Module

Use this module to separate implementation from evidence.

## Goal

Make completion claims precise. “Built” and “verified” are not synonyms.

## Verification layers

### Syntax and parsing
Check that files are syntactically valid for the target language.

### Static checks
When relevant:
- Formatting
- Linting
- Type checking
- Schema validation
- Build graph sanity

### Unit tests
Verify the smallest useful behaviors local to the module.

### Integration tests
Verify cross-module contracts:
- API to service
- service to database
- event producer to consumer
- UI to API

### Manual validation
If no automated checks are available, provide exact commands or click-path steps.

## Verification reporting rules

For every module and for the final report:
- State what was implemented
- State what was actually run
- State what was not run
- State what the user should run next
- State known risks or assumptions

## Parallel verification policy

Parallel modules may be verified locally in parallel if the platform supports it, but final integration verification must be serialized after the join step.

## Minimal final handoff

The final report should answer:
- What files changed?
- What commands should be run?
- Which checks passed?
- Which checks were not executed here?
- What is the remaining risk surface?

No chest-thumping. Just evidence.
