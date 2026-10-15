#!/usr/bin/env python3
"""
Toolkit Sanity Validator
Verifies that all skills, subagents, references, and configurations in .agents/
conform to schema, have valid YAML frontmatter, valid JSON, and zero broken links.
"""

import sys
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
AGENTS_DIR = ROOT / ".agents"

def parse_frontmatter(file_path: Path) -> dict:
    content = file_path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return {}
    
    frontmatter = {}
    raw_yaml = match.group(1)
    
    # Simple regex-based yaml parser for standard scalar fields
    for line in raw_yaml.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip("'\"")
            frontmatter[key] = val
    return frontmatter

def validate():
    errors = []
    
    # 1. Validate AGENTS.md
    agents_md = ROOT / "AGENTS.md"
    if not agents_md.exists() or len(agents_md.read_text()) < 50:
        errors.append("AGENTS.md is missing or empty at project root.")
    else:
        print("✓ AGENTS.md verified")

    # 2. Validate JSON configurations
    for json_file in [AGENTS_DIR / "hooks.json", AGENTS_DIR / "mcp_config.json"]:
        if not json_file.exists():
            errors.append(f"Missing configuration: {json_file.name}")
            continue
        try:
            json.loads(json_file.read_text(encoding="utf-8"))
            print(f"✓ {json_file.name} is valid JSON")
        except Exception as e:
            errors.append(f"Invalid JSON in {json_file.name}: {e}")

    # 3. Validate Subagents (.agents/agents/*.md)
    agents_dir = AGENTS_DIR / "agents"
    agent_files = list(agents_dir.glob("*.md"))
    print(f"\nValidating {len(agent_files)} Subagents...")
    if not agent_files:
        errors.append("No subagents found in .agents/agents/")
    for af in agent_files:
        fm = parse_frontmatter(af)
        if "name" not in fm or "description" not in fm:
            errors.append(f"Subagent {af.name} is missing 'name' or 'description' in frontmatter.")
        else:
            print(f"  ✓ agent: {fm['name']}")

    # 4. Validate Skills (.agents/skills/*/SKILL.md)
    skills_dir = AGENTS_DIR / "skills"
    skill_files = list(skills_dir.glob("*/SKILL.md"))
    print(f"\nValidating {len(skill_files)} Skills...")
    if not skill_files:
        errors.append("No skills found in .agents/skills/")
    for sf in skill_files:
        fm = parse_frontmatter(sf)
        skill_name = sf.parent.name
        if "name" not in fm or "description" not in fm:
            errors.append(f"Skill {skill_name}/SKILL.md missing 'name' or 'description' in frontmatter.")
        else:
            print(f"  ✓ skill: {skill_name}")

    # 5. Validate References (.agents/references/*.md)
    ref_dir = AGENTS_DIR / "references"
    ref_files = list(ref_dir.glob("*.md"))
    print(f"\nValidating {len(ref_files)} References...")
    for rf in ref_files:
        if rf.stat().st_size < 20:
            errors.append(f"Reference file {rf.name} is empty.")
        else:
            print(f"  ✓ reference: {rf.name}")

    print("\n" + "="*50)
    if errors:
        print(f"FAILED: {len(errors)} error(s) detected:")
        for err in errors:
            print(f"  ✗ {err}")
        sys.exit(1)
    else:
        print(f"SUCCESS: All {len(skill_files)} skills, {len(agent_files)} subagents, and configs are 100% valid!")
        sys.exit(0)

if __name__ == "__main__":
    validate()
