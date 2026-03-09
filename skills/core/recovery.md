# Recovery Module

Use this module when work was interrupted or the user asks to continue.

## Goal

Resume accurately from the last confirmed stable boundary instead of guessing from a truncated output.

## Recovery procedure

1. **Locate the last stable artifact**
   Prefer, in order:
   - A completed file boundary
   - A completed symbol boundary
   - A completed patch hunk
   - A known content digest for a visible artifact

2. **Read the last `ProgressUpdate`**
   Use it to identify:
   - Current module
   - Files touched
   - Last stable anchor
   - Remaining checklist items
   - Blockers or assumptions

3. **Compare for divergence**
   If current visible content conflicts with the last stable state:
   - Regenerate from the most recent non-conflicting boundary
   - State the conflict plainly
   - Do not attempt magical mid-token surgery

4. **Resume from the next unchecked unit**
   Continue from:
   - The next file
   - The next symbol
   - The next patch hunk
   - The next verification step

5. **Update progress**
   Emit a fresh `ProgressUpdate` with a new resume anchor.

## When not to use recovery

Do not use recovery ritual for tiny tasks that can simply be restated and finished in one pass.

## Recovery style rules

- Do not rely on a “last line hash” unless you actually computed it from visible content.
- Do not ask the user to manually reconstruct a cut-off line unless that is the only remaining truthful option.
- Do not promise background continuation.
- Prefer restarting from a stable function or file boundary over trying to splice a half-token.

A precise restart beats a theatrical but brittle continuation.
