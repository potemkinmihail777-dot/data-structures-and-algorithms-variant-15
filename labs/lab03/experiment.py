import random
from labs.common import (
    arguments,
    load_array,
    measure,
    save_rows,
    save_environment,
    plot_lines,
    slope,
    SEED,
)
from .algorithms import bubble_sort, insertion_sort, selection_sort, quick_sort


def main():
    args, rng, rows = arguments(3), random.Random(SEED), []
    functions = [bubble_sort, insertion_sort, selection_sort, quick_sort]
    for kind in ("random", "sorted", "reversed"):
        for n in (100, 250, 630, 1600, 4000):
            data = load_array(args.data, "random", n)
            if kind != "random":
                data = sorted(data, reverse=kind == "reversed")
            for function in functions:

                def run(a):
                    return function(
                        a, **({"rng": rng} if function is quick_sort else {})
                    )

                stats = run(data.copy())
                rows.append(
                    {
                        "kind": kind,
                        "algorithm": function.__name__,
                        "n": n,
                        "comparisons": stats.comparisons,
                        "swaps": stats.swaps,
                        "moves": stats.moves,
                        **measure(run, setup=data.copy),
                    }
                )
            print(kind, n, flush=True)
        selected = [row for row in rows if row["kind"] == kind]
        plot_lines(
            args.out,
            f"sorts_{kind}",
            selected,
            title=f"ЛР 3: {kind}",
            ylabel="Медиана, с",
        )
    save_rows(args.out, "measurements", rows)
    save_rows(
        args.out,
        "slopes",
        [
            {
                "kind": kind,
                "algorithm": function.__name__,
                "slope": slope(
                    [
                        r
                        for r in rows
                        if r["kind"] == kind and r["algorithm"] == function.__name__
                    ]
                ),
            }
            for kind in ("random", "sorted", "reversed")
            for function in functions
        ],
    )
    stability = []
    original = [(2, "a"), (2, "b"), (1, "c")]
    for function in functions:
        result = original.copy()
        function(
            result,
            key=lambda x: x[0],
            **({"rng": rng} if function is quick_sort else {}),
        )
        stability.append(
            {
                "algorithm": function.__name__,
                "before": original,
                "after": result,
                "stable_on_this_input": result == sorted(original, key=lambda x: x[0]),
            }
        )
    save_rows(args.out, "stability", stability)
    save_environment(args)


if __name__ == "__main__":
    main()
