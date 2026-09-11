"""Общие средства воспроизводимых экспериментов: ввод, таймер, CSV и графики."""

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import statistics
import time

ROOT = Path(__file__).resolve().parent.parent
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".cache" / "matplotlib"))

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

VARIANT, SEED = 15, 45
SIZES = (1000, 3000, 10000, 30000, 100000)


def arguments(lab):
    parser = argparse.ArgumentParser(description=f"ЛР {lab}, вариант 15")
    parser.add_argument("--variant", type=int, default=VARIANT)
    parser.add_argument("--data", type=Path, default=ROOT / "data" / "generated")
    parser.add_argument(
        "--out", type=Path, default=ROOT / "labs" / f"lab{lab:02}" / "results"
    )
    args = parser.parse_args()
    if args.variant != VARIANT:
        parser.error("Этот комплект закреплён за вариантом 15")
    manifest = json.loads((args.data / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("variant") != VARIANT or manifest.get("seed") != SEED:
        parser.error("Данные не соответствуют варианту 15 / seed 45")
    args.out.mkdir(parents=True, exist_ok=True)
    return args


def load_array(data, kind, n):
    file_n = min(size for size in SIZES if size >= n)
    values = [
        int(value)
        for value in (data / f"arrays_{kind}_{file_n}.txt").read_text().split()
    ]
    return values[:n]


def measure(operation, setup=lambda: None, divisor=1):
    """Прогрев + ровно пять независимых замеров; setup вне таймера."""
    operation(setup())
    samples = []
    for _ in range(5):
        state = setup()
        start = time.perf_counter()
        operation(state)
        samples.append((time.perf_counter() - start) / divisor)
    return {
        "seconds": statistics.median(samples),
        **{f"trial_{i + 1}": value for i, value in enumerate(samples)},
    }


def save_rows(out, name, rows):
    if not rows:
        raise ValueError("no measurement rows")
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with (out / f"{name}.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    (out / f"{name}.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def save_environment(args):
    cpu = platform.processor()
    if platform.system() == "Windows":
        import winreg

        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
        ) as key:
            cpu = winreg.QueryValueEx(key, "ProcessorNameString")[0].strip()
    files = [p for p in sorted(args.data.iterdir()) if p.is_file()]
    environment = {
        "variant": VARIANT,
        "seed": SEED,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "cpu": cpu,
        "numpy": np.__version__,
        "matplotlib": matplotlib.__version__,
        "repeats": 5,
        "warmups": 1,
        "timer": "time.perf_counter",
        "summary": "median",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "power_and_background_processes": "not controlled; background desktop session",
        "data_sha256": {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files
        },
    }
    (args.out / "environment.json").write_text(
        json.dumps(environment, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def plot_lines(
    out,
    name,
    rows,
    x="n",
    y="seconds",
    group="algorithm",
    logx=True,
    logy=True,
    title="",
    xlabel=None,
    ylabel=None,
):
    figure, axes = plt.subplots(figsize=(8, 4.8))
    for label in dict.fromkeys(row[group] for row in rows):
        selected = sorted(
            (row for row in rows if row[group] == label), key=lambda row: row[x]
        )
        axes.plot(
            [row[x] for row in selected],
            [row[y] for row in selected],
            "o-",
            label=label,
            markersize=4,
        )
    if logx:
        axes.set_xscale("log")
    if logy:
        axes.set_yscale("log")
    axes.set(xlabel=xlabel or x, ylabel=ylabel or y, title=title)
    axes.grid(True, which="both", alpha=0.25)
    axes.legend(fontsize=8)
    figure.tight_layout()
    figure.savefig(out / f"{name}.png", dpi=160)
    plt.close(figure)


def slope(rows):
    xs = [math.log(row["n"]) for row in rows]
    ys = [math.log(row["seconds"]) for row in rows]
    mx, my = statistics.mean(xs), statistics.mean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum(
        (x - mx) ** 2 for x in xs
    )
