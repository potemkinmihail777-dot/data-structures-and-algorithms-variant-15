import random
from labs.common import (
    arguments,
    load_array,
    measure,
    save_rows,
    save_environment,
    plot_lines,
    SIZES,
    SEED,
)
from .algorithms import BST


def main():
    args, rng, rows, heights = arguments(5), random.Random(SEED), [], []
    for n in SIZES:
        values = load_array(args.data, "random", n)
        tree = BST()
        for value in values:
            tree.insert(value)
        assert tree.validate()
        heights.append(
            {"n": n, "unique": len(tree), "height": tree.height(), "kind": "random"}
        )
        for kind in ("hit", "miss"):
            queries = (
                rng.choices(values, k=64)
                if kind == "hit"
                else [2_000_000 + rng.randrange(1_000_000) for _ in range(64)]
            )
            for name, search in (
                ("BST", tree.search),
                ("list.in", lambda key: key in values),
            ):
                assert all(search(key) == (kind == "hit") for key in queries)
                rows.append(
                    {
                        "algorithm": name,
                        "kind": kind,
                        "n": n,
                        **measure(
                            lambda _: [search(q) for q in queries], divisor=len(queries)
                        ),
                    }
                )
        print("BST", n, tree.height(), flush=True)
    for n in (16, 64, 256, 512):
        tree = BST()
        for key in range(n):
            tree.insert(key)
        heights.append({"n": n, "unique": n, "height": tree.height(), "kind": "sorted"})
    save_rows(args.out, "search", rows)
    save_rows(args.out, "heights", heights)
    for kind in ("hit", "miss"):
        plot_lines(
            args.out,
            f"search_{kind}",
            [r for r in rows if r["kind"] == kind],
            title=f"ЛР 5: поиск {kind}",
            ylabel="Медиана, с/запрос",
        )
    plot_lines(
        args.out,
        "height",
        heights,
        y="height",
        group="kind",
        title="ЛР 5: высота случайного и вырожденного BST",
        ylabel="Высота, рёбра",
    )
    save_environment(args)


if __name__ == "__main__":
    main()
