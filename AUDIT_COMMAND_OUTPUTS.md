# Audit command outputs

## Run date

- 2026-04-27 (UTC)

## 1) Validator run (post-remediation)

```bash
python scripts/validate_repo.py
```

Output:

```text
Repository validation passed.
```

## 2) Required workflow presence

```bash
test -f .github/workflows/validate.yml && echo present
```

Output:

```text
present
```

## 3) Placeholder scan check (including audit markdown)

```bash
python - <<'PY'
from scripts.validate_repo import validate_placeholders
print(validate_placeholders())
PY
```

Output:

```text
[]
```

## 4) Wrapper routing checks

```bash
for f in AGENTS.md CLAUDE.md GEMINI.md .cursorrules .clinerules; do rg -n "SKILL.md" "$f"; done
```

Output:

```text
AGENTS.md:3:Canonical instructions live in `SKILL.md`.
AGENTS.md:6:1. `SKILL.md`
CLAUDE.md:3:Use the canonical skill at `SKILL.md`, then follow `references/codegen-orchestrator.md`.
GEMINI.md:3:Canonical source: `SKILL.md`
GEMINI.md:5:After loading `SKILL.md`, read `references/codegen-orchestrator.md` and only the relevant files in `skills/core/`.
.cursorrules:1:Use the skill in `SKILL.md` as the source of truth.
.clinerules:1:Use the skill in `SKILL.md` as the source of truth.
```

## 5) Internal markdown link check

```bash
python - <<'PY'
import re
from pathlib import Path
pat = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
root = Path('.')
errors = []
for rel in ("README.md", "SKILL.md"):
    text = (root / rel).read_text(encoding="utf-8")
    for target in pat.findall(text):
        if target.startswith("http") or target.startswith("mailto:"):
            continue
        normalized = target.split("#", 1)[0]
        if normalized and not (root / normalized).exists():
            errors.append((rel, target))
print(errors)
PY
```

Output:

```text
[]
```
