"""Проверить внутренние ссылки Markdown и комплектность лабораторных."""

from pathlib import Path
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent


def main():
    problems, links = [], 0
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts or "data" in path.parts:
            continue
        for match in re.finditer(
            r"!?\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")
        ):
            target = match.group(1).split("#", 1)[0]
            if not target or re.match(r"\w+://", target):
                continue
            links += 1
            if not (path.parent / unquote(target)).is_file():
                problems.append(f"{path.relative_to(ROOT)}: {target}")
    for number in range(1, 9):
        folder = ROOT / "labs" / f"lab{number:02}"
        for name in (
            "README.md",
            "notes.md",
            "report.md",
            "algorithms.py",
            "experiment.py",
            "test_lab.py",
            "results/environment.json",
        ):
            if not (folder / name).is_file():
                problems.append(f"Missing lab{number:02}/{name}")
    if problems:
        raise SystemExit("\n".join(problems))
    print(f"OK: {links} local links and 8 complete lab folders")


if __name__ == "__main__":
    main()
