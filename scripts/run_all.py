"""Запустить все эксперименты последовательно, не конкурируя за CPU."""

import importlib


def main():
    for number in range(1, 9):
        print(f"\nLAB {number}", flush=True)
        importlib.import_module(f"labs.lab{number:02}.experiment").main()


if __name__ == "__main__":
    main()
