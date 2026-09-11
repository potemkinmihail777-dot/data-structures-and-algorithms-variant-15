import math
from labs.common import (
    arguments,
    load_array,
    measure,
    save_rows,
    save_environment,
    plot_lines,
    slope,
    SIZES,
)
from .algorithms import array_sum, array_max, count_equal_pairs, binary_pow


def main():
    args, rows = arguments(1), []
    for name, function, sizes, kind in [
        ("sum", array_sum, SIZES, "random"),
        ("max", array_max, SIZES, "random"),
        ("equal_pairs", count_equal_pairs, (500, 1000, 3000, 10000, 30000), "dups"),
    ]:
        for n in sizes:
            data = load_array(args.data, kind, n)
            row = {"algorithm": name, "n": n, **measure(lambda _: function(data))}
            rows.append(row)
            print(name, n, row["seconds"], flush=True)
    save_rows(args.out, "measurements", rows)
    plot_lines(
        args.out,
        "complexity",
        rows,
        title="ЛР 1: время и размер входа",
        ylabel="Медиана, с",
    )
    save_rows(
        args.out,
        "slopes",
        [
            {
                "algorithm": name,
                "slope": slope([r for r in rows if r["algorithm"] == name]),
            }
            for name in ("sum", "max", "equal_pairs")
        ],
    )
    powers = []
    for exponent in (10**3, 10**4, 10**5, 10**6, 10**7):

        def batch(_):
            for _ in range(20000):
                binary_pow(3, exponent, 1_000_000_007)

        powers.append(
            {
                "algorithm": "binary_pow",
                "n": exponent,
                "log2_n": math.log2(exponent),
                **measure(batch, divisor=20000),
            }
        )
    save_rows(args.out, "powers", powers)
    plot_lines(
        args.out,
        "binary_power",
        powers,
        x="log2_n",
        logx=False,
        logy=False,
        title="ЛР 1: бинарная степень по модулю",
        xlabel="log₂ показателя",
        ylabel="Медиана одного вызова, с",
    )
    save_environment(args)


if __name__ == "__main__":
    main()
