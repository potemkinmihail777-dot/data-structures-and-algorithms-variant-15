import hashlib
import statistics
import numpy as np
from labs.common import (
    arguments,
    measure,
    save_rows,
    save_environment,
    plot_lines,
    SIZES,
    SEED,
)
from .algorithms import linear_search, binary_search, interpolation_search


def main():
    args, rng, rows, inputs = arguments(6), np.random.default_rng(SEED), [], []
    for kind in ("uniform", "exponential"):
        for n in SIZES:
            base = (
                rng.integers(0, 1_000_001, n)
                if kind == "uniform"
                else np.floor(rng.exponential(10000, n)).astype(np.int64)
            )
            # Только чётные ключи: нечётные запросы гарантированно отсутствуют.
            data = sorted(int(value) * 2 for value in base)
            inputs.append(
                {
                    "kind": kind,
                    "n": n,
                    "sha256": hashlib.sha256(
                        ",".join(map(str, data)).encode()
                    ).hexdigest(),
                }
            )
            hits = [data[int(index)] for index in rng.integers(0, n, 64)]
            for query_kind, queries in (
                ("hit", hits),
                ("miss", [value + 1 for value in hits]),
            ):
                for function in (linear_search, binary_search, interpolation_search):
                    results = [function(data, query) for query in queries]
                    assert all(
                        (index != -1) == (query_kind == "hit") for index, _ in results
                    )
                    comparisons = statistics.mean(count for _, count in results)
                    rows.append(
                        {
                            "kind": kind,
                            "query": query_kind,
                            "algorithm": function.__name__,
                            "n": n,
                            "comparisons": comparisons,
                            **measure(
                                lambda _: [function(data, q) for q in queries],
                                divisor=len(queries),
                            ),
                        }
                    )
            print(kind, n, flush=True)
        for query in ("hit", "miss"):
            selected = [r for r in rows if r["kind"] == kind and r["query"] == query]
            for metric in ("seconds", "comparisons"):
                plot_lines(
                    args.out,
                    f"{kind}_{query}_{metric}",
                    selected,
                    y=metric,
                    title=f"ЛР 6: {kind}, {query}, {metric}",
                )
    save_rows(args.out, "measurements", rows)
    save_rows(args.out, "inputs", inputs)
    # Отдельный конструктивный худший случай: один огромный выброс справа.
    worst = []
    for n in (100, 300, 1000, 3000, 10000):
        data = list(range(n - 1)) + [10**12]
        for function in (binary_search, interpolation_search):
            index, comparisons = function(data, n - 2)
            assert index == n - 2
            worst.append(
                {
                    "algorithm": function.__name__,
                    "n": n,
                    "comparisons": comparisons,
                    **measure(lambda _: function(data, n - 2)),
                }
            )
    save_rows(args.out, "worst_case", worst)
    plot_lines(
        args.out,
        "worst_case",
        worst,
        y="comparisons",
        title="ЛР 6: выброс 10¹² в конце массива",
        ylabel="Сравнения",
    )
    save_environment(args)


if __name__ == "__main__":
    main()
