"""Функции возвращают (любой подходящий индекс или −1, сравнения ключей).

У бинарного и интерполяционного поиска вход должен быть отсортирован.
Проверка сортировки не включена в функцию, иначе она добавила бы Θ(n).
"""


def linear_search(a, target):
    comparisons = 0
    for i, value in enumerate(a):
        comparisons += 1
        if value == target:
            return i, comparisons
    return -1, comparisons


def binary_search(a, target):
    lo, hi, comparisons = 0, len(a) - 1, 0
    while lo <= hi:
        # Если ключ существует, он ещё может находиться в [lo, hi].
        mid = (lo + hi) // 2
        comparisons += 1
        if a[mid] == target:
            return mid, comparisons
        comparisons += 1
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, comparisons


def interpolation_search(a, target):
    lo, hi, comparisons = 0, len(a) - 1, 0
    while lo <= hi:
        comparisons += 1
        if target < a[lo]:
            break
        comparisons += 1
        if target > a[hi]:
            break
        comparisons += 1
        if a[lo] == a[hi]:
            # Проверки диапазона выше уже доказывают равенство ключу.
            return lo, comparisons
        pos = lo + (target - a[lo]) * (hi - lo) // (a[hi] - a[lo])
        comparisons += 1
        if a[pos] == target:
            return pos, comparisons
        comparisons += 1
        if a[pos] < target:
            lo = pos + 1
        else:
            hi = pos - 1
    return -1, comparisons
