# Audit command outputs

## Run date

- 2026-04-27 (UTC)

## 1) Validator execution attempt

```bash
python --version
python scripts/validate_repo.py
```

Output:

```text
Python 3.10.19
Missing dependency: PyYAML (No module named 'yaml')
```

## 2) Dependency install attempt (environment limitation)

```bash
python -m pip install --user pyyaml jsonschema
```

Output (truncated):

```text
WARNING: Retrying ... ProxyError ... 403 Forbidden
ERROR: Could not find a version that satisfies the requirement pyyaml
ERROR: No matching distribution found for pyyaml
```

## 3) Root skill size

```bash
wc -c < SKILL.md
```

Output:

```text
412
```

## 4) Required file presence snapshot

```bash
for f in ...; do [ -e "$f" ] || echo "$f"; done
```

Output before remediation:

```text
.github/workflows/validate.yml
```

## 5) Placeholder scan

```bash
rg -n "your-org|your-repo|example\.com|your-username|openai" -g "*.md" -g "*.json" -g "*.yml" -g "*.yaml" -g "*.html" || true
```

Output:

```text
(no matches)
```

## 6) Cache artifact scan

```bash
find . \( -type d -name '__pycache__' -o -name '.DS_Store' \) -print
```

Output:

```text
(no matches)
```

## 7) Wrapper routing checks

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

## 8) Internal markdown link check

```bash
python - <<'PY'
# check README.md and SKILL.md local markdown links
PY
```

Output:

```text
No broken internal markdown links in README.md and SKILL.md
```
