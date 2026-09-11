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
from labs.lab03.algorithms import quick_sort
from .algorithms import merge_sort, counting_sort, radix_sort, heap_sort


def main():
    args, rng, rows = arguments(4), random.Random(SEED), []
    for kind in ("wide", "narrow", "sorted", "reversed", "nearly"):
        for n in SIZES:
            data = load_array(args.data, "dups" if kind == "narrow" else "random", n)
            if kind in ("sorted", "reversed", "nearly"):
                data = sorted(data, reverse=kind == "reversed")
            if kind == "nearly":
                for _ in range(max(1, n // 100)):
                    i, j = rng.randrange(n), rng.randrange(n)
                    data[i], data[j] = data[j], data[i]
            expected = sorted(data)
            for function in (
                merge_sort,
                counting_sort,
                radix_sort,
                heap_sort,
                quick_sort,
                sorted,
            ):

                def run(a):
                    return function(
                        a, **({"rng": rng} if function is quick_sort else {})
                    )

                check = data.copy()
                returned = run(check)
                assert (returned if function is sorted else check) == expected
                rows.append(
                    {
                        "kind": kind,
                        "algorithm": function.__name__,
                        "n": n,
                        "range": max(data) - min(data) + 1,
                        **measure(run, setup=data.copy),
                    }
                )
            print(kind, n, flush=True)
        plot_lines(
            args.out,
            f"sorts_{kind}",
            [r for r in rows if r["kind"] == kind],
            title=f"ЛР 4: {kind}",
            ylabel="Медиана, с",
        )
    save_rows(args.out, "measurements", rows)
    save_environment(args)


if __name__ == "__main__":
    main()
