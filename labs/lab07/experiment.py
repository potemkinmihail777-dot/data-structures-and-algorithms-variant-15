from labs.common import arguments, measure, save_rows, save_environment, plot_lines
from .algorithms import naive_search, kmp_search, rabin_karp_search, boyer_moore_search


def main():
    args, rows = arguments(7), []
    patterns = (args.data / "patterns.txt").read_text(encoding="utf-8").splitlines()
    texts = {
        name: (args.data / name).read_text(encoding="utf-8").rstrip("\n")
        for name in ("texts_small_alphabet.txt", "texts_natural.txt")
    }
    for pattern_id, line in enumerate(patterns):
        filename, pattern = line.split("\t", 1)
        text = texts[filename]
        reference = naive_search(text, pattern)[0]
        functions = [
            ("naive", naive_search),
            ("KMP", kmp_search),
            ("Rabin-Karp", rabin_karp_search),
            ("BM bad", lambda t, p: boyer_moore_search(t, p, False)),
            ("BM both", boyer_moore_search),
        ]
        for name, function in functions:
            found, comparisons = function(text, pattern)
            assert found == reference and found
            rows.append(
                {
                    "kind": filename,
                    "algorithm": name,
                    "pattern_id": pattern_id,
                    "pattern": pattern,
                    "m": len(pattern),
                    "n": len(text),
                    "matches": len(found),
                    "comparisons": comparisons,
                    **measure(lambda _: function(text, pattern)),
                }
            )
        print(filename, len(pattern), len(reference), flush=True)
    save_rows(args.out, "measurements", rows)
    for filename in texts:
        selected = [r for r in rows if r["kind"] == filename]
        name = "small" if "small" in filename else "natural"
        for metric in ("seconds", "comparisons"):
            plot_lines(
                args.out,
                f"{name}_{metric}",
                selected,
                x="m",
                y=metric,
                logx=False,
                title=f"ЛР 7: {name}, {metric}",
                xlabel="Длина шаблона m",
            )
    save_environment(args)


if __name__ == "__main__":
    main()
