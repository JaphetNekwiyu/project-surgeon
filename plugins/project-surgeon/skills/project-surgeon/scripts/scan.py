#!/usr/bin/env python3
"""Read-only repository scanner. Results are candidates, not proof of dead code."""
import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

EXTS = {".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".java", ".cs", ".rb", ".php", ".vue", ".svelte", ".sql", ".css", ".scss"}
SKIP = {"node_modules", ".git", ".next", ".nuxt", "dist", "build", "coverage", ".venv", "venv", "__pycache__", ".turbo", "vendor", "target"}
SENSITIVE = {".env", ".pem", ".key", ".p12", ".pfx", "id_rsa", "credentials.json", "secrets.json"}

def source_files(root):
    for file in root.rglob("*"):
        if not file.is_file() or file.is_symlink() or any(p in SKIP for p in file.relative_to(root).parts):
            continue
        if file.name.lower() in SENSITIVE or file.name.lower().startswith(".env"):
            continue
        if file.suffix.lower() not in EXTS or file.stat().st_size > 1024 * 1024:
            continue
        yield file

def scan(root):
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError("Repository directory does not exist")
    seen = defaultdict(list)
    blocks = defaultdict(list)
    large = []
    count = 0
    for file in source_files(root):
        count += 1
        rel = file.relative_to(root).as_posix()
        try:
            raw = file.read_bytes()
            content = raw.decode("utf-8")
        except (OSError, UnicodeError):
            continue
        seen[hashlib.sha256(raw).hexdigest()].append(rel)
        lines = content.splitlines()
        if len(lines) > 450:
            large.append({"path": rel, "lines": len(lines)})
        # Consecutive nonempty normalized blocks; these are hints, not semantic clones.
        for i in range(max(0, len(lines) - 7)):
            block = tuple(s.strip() for s in lines[i:i + 8])
            if all(block) and sum(len(s) for s in block) >= 160:
                blocks[hashlib.sha256("\n".join(block).encode()).hexdigest()].append({"path": rel, "line": i + 1})
    duplicates = [paths for paths in seen.values() if len(paths) > 1]
    repetitions = [positions for positions in blocks.values() if len({p["path"] for p in positions}) > 1]
    return {"root": str(root), "source_files": count,
            "exact_duplicate_files": duplicates,
            "repeated_code_candidates": repetitions[:100],
            "large_file_candidates": sorted(large, key=lambda x: -x["lines"])[:100],
            "disclaimer": "All findings are candidates; review references and behavior before deleting or modifying code."}

def markdown(result):
    out = ["# Project Surgeon audit", "", "Files inspected: " + str(result["source_files"]), "", result["disclaimer"], ""]
    for key, heading in [("exact_duplicate_files", "Exact duplicate files"), ("repeated_code_candidates", "Repeated code candidates"), ("large_file_candidates", "Large file candidates")]:
        out.extend(["## " + heading, ""])
        values = result[key]
        if not values:
            out.append("None found.")
        for item in values:
            out.append("- " + json.dumps(item, ensure_ascii=False))
        out.append("")
    return "\n".join(out)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo", default=".")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--output")
    args = p.parse_args()
    result = scan(args.repo)
    report = json.dumps(result, indent=2, ensure_ascii=False) if args.format == "json" else markdown(result)
    if args.output:
        Path(args.output).write_text(report + "\n", encoding="utf-8")
    else:
        print(report)

if __name__ == "__main__":
    main()
