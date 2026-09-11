"""Сортировки изменяют переданный список; возвращают счётчики операций."""

from dataclasses import dataclass
import random


def identity(value):
    return value


@dataclass
class SortStats:
    comparisons: int = 0
    swaps: int = 0
    moves: int = 0


def _swap(a, i, j, stats):
    if i != j:
        a[i], a[j] = a[j], a[i]
        stats.swaps += 1
        stats.moves += 2  # записи в ячейки списка, без локальной переменной


def bubble_sort(a, key=identity):
    stats = SortStats()
    for end in range(len(a) - 1, 0, -1):
        changed = False
        for j in range(end):
            stats.comparisons += 1
            if key(a[j]) > key(a[j + 1]):
                _swap(a, j, j + 1, stats)
                changed = True
        if not changed:
            break
    return stats


def insertion_sort(a, key=identity):
    stats = SortStats()
    for i in range(1, len(a)):
        value, j = a[i], i - 1
        while j >= 0:
            stats.comparisons += 1
            if key(a[j]) <= key(value):
                break
            a[j + 1] = a[j]
            stats.moves += 1
            j -= 1
        a[j + 1] = value
        stats.moves += 1
    return stats


def selection_sort(a, key=identity):
    stats = SortStats()
    for i in range(len(a) - 1):
        smallest = i
        for j in range(i + 1, len(a)):
            stats.comparisons += 1
            if key(a[j]) < key(a[smallest]):
                smallest = j
        _swap(a, i, smallest, stats)
    return stats


def quick_sort(a, key=identity, rng=None):
    """Трёхчастный QuickSort; рекурсия только в меньшую часть, стек O(log n).

    Один RNG передаётся из эксперимента; не переинициализируется на вызовах.
    Равные опорному элементы исключаются из дальнейших разбиений.
    """
    rng = random if rng is None else rng
    stats = SortStats()

    def sort(lo, hi):
        while lo < hi:
            pivot = key(a[rng.randrange(lo, hi + 1)])
            left, current, right = lo, lo, hi
            # [lo,left) < pivot; [left,current) == pivot; (right,hi] > pivot.
            while current <= right:
                stats.comparisons += 1
                if key(a[current]) < pivot:
                    _swap(a, left, current, stats)
                    left += 1
                    current += 1
                else:
                    stats.comparisons += 1
                    if key(a[current]) > pivot:
                        _swap(a, current, right, stats)
                        right -= 1
                    else:
                        current += 1
            if left - lo < hi - right:
                sort(lo, left - 1)
                lo = right + 1
            else:
                sort(right + 1, hi)
                hi = left - 1

    sort(0, len(a) - 1)
    return stats
