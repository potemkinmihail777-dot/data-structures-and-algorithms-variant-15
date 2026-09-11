from collections import deque
from labs.common import (
    arguments,
    load_array,
    measure,
    save_rows,
    save_environment,
    plot_lines,
    SIZES,
)
from .algorithms import fibonacci, hanoi, DynamicArray, Deque


def main():
    args, rows = arguments(2), []
    for n in SIZES:
        data = load_array(args.data, "random", n)
        for name, constructor, method in [
            ("DynamicArray.append", DynamicArray, "append"),
            ("list.append", list, "append"),
            ("Deque.appendleft", Deque, "appendleft"),
            ("deque.appendleft", deque, "appendleft"),
            ("list.insert(0)", list, "insert"),
        ]:

            def batch(container):
                for value in data:
                    if method == "insert":
                        container.insert(0, value)
                    else:
                        getattr(container, method)(value)

            rows.append(
                {
                    "algorithm": name,
                    "n": n,
                    **measure(batch, setup=constructor, divisor=n),
                }
            )
        print("structures", n, flush=True)
    save_rows(args.out, "append", rows)
    plot_lines(
        args.out,
        "append",
        rows,
        title="ЛР 2: средняя стоимость добавления",
        ylabel="Медиана, с/операцию",
    )
    recursion = []
    for n in (5, 10, 15, 20, 25):
        for cached in (False, True):
            result, calls = fibonacci(n, cached)
            recursion.append(
                {
                    "algorithm": "memo" if cached else "naive",
                    "n": n,
                    "result": result,
                    "calls": calls,
                    **measure(lambda _: fibonacci(n, cached)),
                }
            )
    save_rows(args.out, "recursion", recursion)
    plot_lines(
        args.out,
        "fibonacci_calls",
        recursion,
        y="calls",
        title="ЛР 2: вызовы Фибоначчи",
        ylabel="Число вызовов",
    )
    transfers = [
        {"n": n, "moves": sum(1 for _ in hanoi(n)), "formula": 2**n - 1}
        for n in range(1, 16)
    ]
    save_rows(args.out, "hanoi", transfers)
    growth = []
    a = DynamicArray()
    for i in range(1, 1026):
        a.append(i)
        if i == 1 or i & (i - 1) == 0 or (i - 1) & (i - 2) == 0:
            growth.append(
                {
                    "n": i,
                    "capacity": a.capacity,
                    "copies": a.copies,
                    "credit_cost_3": 3 * i,
                    "writes_plus_copies": i + a.copies,
                }
            )
    save_rows(args.out, "growth", growth)
    save_environment(args)


if __name__ == "__main__":
    main()
