import random
from collections import Counter
from labs.common import (
    arguments,
    measure,
    save_rows,
    save_environment,
    plot_lines,
    SEED,
)
import matplotlib.pyplot as plt
from .algorithms import HashTable, polynomial_hash, first_character_hash


def main():
    args, rng, rows = arguments(8), random.Random(SEED), []
    keys = list(
        dict.fromkeys(
            (args.data / "pairs_keys.txt").read_text(encoding="utf-8").splitlines()
        )
    )
    rng.shuffle(keys)
    chain_rows = []
    figure, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, (name, hash_function) in zip(
        axes,
        (("polynomial", polynomial_hash), ("first_character", first_character_hash)),
    ):
        table = HashTable(
            capacity=16384, hash_function=hash_function, auto_resize=False
        )
        for i, key in enumerate(keys):
            table.put(key, i)
        assert table.validate()
        histogram = Counter(table.chain_lengths())
        for length, count in sorted(histogram.items()):
            chain_rows.append(
                {
                    "hash": name,
                    "chain_length": length,
                    "buckets": count,
                    "alpha": table.load_factor,
                }
            )
        ax.bar(
            [str(x) for x in sorted(histogram)],
            [histogram[x] for x in sorted(histogram)],
        )
        ax.set(xlabel="Длина цепочки", ylabel="Число бакетов (log)", title=name)
        ax.set_yscale("log")
    figure.tight_layout()
    figure.savefig(args.out / "chains.png", dpi=160)
    plt.close(figure)
    save_rows(args.out, "chains", chain_rows)
    for requested_alpha in (0.1, 0.25, 0.5, 0.75, 1.0, 2.0, 4.0):
        n, capacity = int(1024 * requested_alpha), 1024
        initial = keys[:n]
        new = keys[n : n + 64]
        queries = rng.choices(initial, k=64)
        for implementation in ("polynomial", "first_character", "dict"):

            def build():
                if implementation == "dict":
                    return {key: i for i, key in enumerate(initial)}
                table = HashTable(
                    capacity,
                    (
                        polynomial_hash
                        if implementation == "polynomial"
                        else first_character_hash
                    ),
                    False,
                )
                for i, key in enumerate(initial):
                    table.put(key, i)
                return table

            for operation in ("get_hit", "get_miss", "put_update", "put_new"):

                def batch(table):
                    if operation == "put_new":
                        selected = new
                    elif operation == "get_miss":
                        selected = new
                    else:
                        selected = queries
                    for i, key in enumerate(selected):
                        if operation.startswith("put"):
                            if implementation == "dict":
                                table[key] = i
                            else:
                                table.put(key, i)
                        else:
                            try:
                                if implementation == "dict":
                                    table[key]
                                else:
                                    table.get(key)
                            except KeyError:
                                if operation != "get_miss":
                                    raise

                rows.append(
                    {
                        "implementation": implementation,
                        "operation": operation,
                        "algorithm": implementation,
                        "n": n,
                        "alpha": n / capacity,
                        "alpha_after": (
                            (n + 64) / capacity
                            if operation == "put_new"
                            else n / capacity
                        ),
                        **measure(batch, setup=build, divisor=64),
                    }
                )
        print("alpha", n / capacity, flush=True)
    save_rows(args.out, "operations", rows)
    for operation in ("get_hit", "get_miss", "put_update", "put_new"):
        plot_lines(
            args.out,
            operation,
            [r for r in rows if r["operation"] == operation],
            x="alpha",
            logx=False,
            title=f"ЛР 8: {operation}",
            xlabel="Начальная α = n / 1024",
            ylabel="Медиана, с/операцию",
        )
    save_environment(args)


if __name__ == "__main__":
    main()
