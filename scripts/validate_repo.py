#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable

try:
    import yaml
except Exception as exc:  # pragma: no cover
    print(f"Missing dependency: PyYAML ({exc})", file=sys.stderr)
    sys.exit(1)

try:
    import jsonschema
except Exception:
    jsonschema = None


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_FRONTMATTER_KEYS = {"name", "description", "license", "metadata"}
AUTHOR = "Iamemily2050"
REPO_URL = "https://github.com/Emily2040/parallel-codegen-orchestrator"
PLACEHOLDER_PATTERN = re.compile(r"your-org|your-repo|example\.com|your-username|openai", re.IGNORECASE)
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SURROGATE_PATTERN = re.compile(r"\\ud[89ab][0-9a-f]{2}", re.IGNORECASE)
REQUIRED_FILES = [
    "SKILL.md",
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".cursorrules",
    ".clinerules",
    ".gitignore",
    "README.md",
    "LICENSE",
    "references/codegen-orchestrator.md",
    "skills/core/planning.md",
    "skills/core/execution.md",
    "skills/core/recovery.md",
    "skills/core/verification.md",
    "registry/forbidden-slop.json",
    "schemas/plan.schema.json",
    "schemas/progress.schema.json",
    "schemas/final-report.schema.json",
    "examples/request.md",
    "examples/plan.json",
    "examples/progress.json",
    "examples/final-report.json",
    "docs/index.html",
    "docs/REDESIGN_NOTES.md",
    "docs/assets/architecture.svg",
    "scripts/validate_repo.py",
    ".github/workflows/validate.yml",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path.name} is missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"{path.name} frontmatter is not closed")
    raw_frontmatter = text[4:end]
    body = text[end + 5 :]
    data = yaml.safe_load(raw_frontmatter)
    if not isinstance(data, dict):
        raise ValueError(f"{path.name} frontmatter did not parse into an object")
    return data, body


def iter_text_files() -> Iterable[Path]:
    for suffix in ("*.md", "*.json", "*.yml", "*.yaml", "*.html"):
        yield from ROOT.rglob(suffix)


def validate_required_files() -> list[str]:
    errors: list[str] = []
    for rel_path in REQUIRED_FILES:
        if not (ROOT / rel_path).exists():
            errors.append(f"Missing required file: {rel_path}")
    if (ROOT / "Skill.md").exists():
        errors.append("Unexpected shim file present: Skill.md")
    return errors


def validate_frontmatter() -> list[str]:
    errors: list[str] = []
    skill_path = ROOT / "SKILL.md"
    try:
        frontmatter, body = parse_frontmatter(skill_path)
    except Exception as exc:
        return [str(exc)]

    extra_keys = set(frontmatter) - ALLOWED_FRONTMATTER_KEYS
    if extra_keys:
        errors.append(f"SKILL.md has unsupported frontmatter keys: {sorted(extra_keys)}")

    for key in ("name", "description", "license"):
        value = frontmatter.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"SKILL.md frontmatter key '{key}' must be a non-empty string")

    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        errors.append("SKILL.md frontmatter key 'metadata' must be an object")
    else:
        if metadata.get("author") != AUTHOR:
            errors.append("SKILL.md metadata.author must match the expected author")
        if metadata.get("repo") != REPO_URL:
            errors.append("SKILL.md metadata.repo must match the canonical GitHub URL")

    char_budget = len(skill_path.read_text(encoding="utf-8"))
    if char_budget >= 500:
        errors.append(f"SKILL.md must stay under 500 characters; found {char_budget}")

    if "references/codegen-orchestrator.md" not in body:
        errors.append("SKILL.md body should route to references/codegen-orchestrator.md")

    return errors


def validate_wrappers() -> list[str]:
    errors: list[str] = []
    for rel_path in ("AGENTS.md", "CLAUDE.md", "GEMINI.md", ".cursorrules", ".clinerules"):
        text = (ROOT / rel_path).read_text(encoding="utf-8")
        if "SKILL.md" not in text:
            errors.append(f"{rel_path} should point to SKILL.md")
    return errors


def validate_no_extraneous_readmes() -> list[str]:
    errors: list[str] = []
    for path in ROOT.rglob("README.md"):
        if path == ROOT / "README.md":
            continue
        errors.append(f"Extraneous README.md inside skill package: {path.relative_to(ROOT)}")
    return errors


def validate_no_cache_files() -> list[str]:
    errors: list[str] = []
    for path in ROOT.rglob("__pycache__"):
        errors.append(f"Cache directory present: {path.relative_to(ROOT)}")
    for path in ROOT.rglob(".DS_Store"):
        errors.append(f"MacOS cache file present: {path.relative_to(ROOT)}")
    return errors


def validate_gitignore() -> list[str]:
    errors: list[str] = []
    text = (ROOT / ".gitignore").read_text(encoding="utf-8")
    for needle in ("__pycache__/", ".DS_Store"):
        if needle not in text:
            errors.append(f".gitignore missing entry: {needle}")
    return errors


def validate_placeholders() -> list[str]:
    errors: list[str] = []
    for path in iter_text_files():
        text = path.read_text(encoding="utf-8")
        if PLACEHOLDER_PATTERN.search(text):
            errors.append(f"Placeholder-like text found in {path.relative_to(ROOT)}")
    return errors


def validate_internal_links() -> list[str]:
    errors: list[str] = []
    for rel_path in ("README.md", "SKILL.md"):
        text = (ROOT / rel_path).read_text(encoding="utf-8")
        for target in MARKDOWN_LINK_PATTERN.findall(text):
            if target.startswith("http") or target.startswith("mailto:"):
                continue
            normalized = target.split("#", 1)[0]
            if not normalized:
                continue
            if not (ROOT / normalized).exists():
                errors.append(f"Broken markdown link in {rel_path}: {target}")
    return errors


def validate_author_identity() -> list[str]:
    errors: list[str] = []
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    docs_index = (ROOT / "docs/index.html").read_text(encoding="utf-8")

    if f"Created by **{AUTHOR}**" not in readme:
        errors.append("README.md missing canonical author line")
    for needle in (
        "https://github.com/Emily2040",
        "https://Iamemily2050.com",
        "https://x.com/iamemily2050",
        "https://instagram.com/iamemily2050",
    ):
        if needle not in readme:
            errors.append(f"README.md missing author link: {needle}")

    if f"Copyright (c) 2026 {AUTHOR}" not in license_text:
        errors.append("LICENSE copyright line is incorrect")

    if "https://github.com/Emily2040" not in docs_index:
        errors.append("docs/index.html footer must link to the GitHub profile")

    return errors


def validate_readme() -> list[str]:
    errors: list[str] = []
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    for needle in (
        "## What this is for",
        "## Repository map",
        "## Installation",
        "## Validation",
        "## Author",
    ):
        if needle not in text:
            errors.append(f"README.md missing section: {needle}")
    if "actions/workflow/status/Emily2040/parallel-codegen-orchestrator/validate.yml" not in text:
        errors.append("README.md missing CI badge")
    return errors


def load_json(rel_path: str) -> dict:
    return json.loads((ROOT / rel_path).read_text(encoding="utf-8"))


def validate_registry() -> list[str]:
    errors: list[str] = []
    registry = load_json("registry/forbidden-slop.json")
    for key in ("banned_phrases", "rules", "preferred_substitutions"):
        if key not in registry:
            errors.append(f"registry/forbidden-slop.json missing '{key}'")
    if "banned_phrases" in registry and not isinstance(registry["banned_phrases"], list):
        errors.append("banned_phrases must be a list")
    return errors


def validate_examples() -> list[str]:
    errors: list[str] = []
    schemas = {
        "examples/plan.json": load_json("schemas/plan.schema.json"),
        "examples/progress.json": load_json("schemas/progress.schema.json"),
        "examples/final-report.json": load_json("schemas/final-report.schema.json"),
    }
    for example_rel, schema in schemas.items():
        instance = load_json(example_rel)
        if jsonschema is None:
            continue
        try:
            jsonschema.Draft202012Validator(schema).validate(instance)
        except Exception as exc:
            errors.append(f"{example_rel} failed schema validation: {exc}")
    return errors


def validate_surrogates() -> list[str]:
    errors: list[str] = []
    for path in iter_text_files():
        text = path.read_text(encoding="utf-8")
        if SURROGATE_PATTERN.search(text):
            errors.append(f"Unicode surrogate escape found in {path.relative_to(ROOT)}")
    return errors


def main() -> int:
    validators = [
        validate_required_files,
        validate_frontmatter,
        validate_wrappers,
        validate_no_extraneous_readmes,
        validate_no_cache_files,
        validate_gitignore,
        validate_placeholders,
        validate_internal_links,
        validate_author_identity,
        validate_readme,
        validate_registry,
        validate_examples,
        validate_surrogates,
    ]
    errors: list[str] = []
    for validator in validators:
        errors.extend(validator())

    if errors:
        for error in errors:
            fail(error)
        return 1

    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
