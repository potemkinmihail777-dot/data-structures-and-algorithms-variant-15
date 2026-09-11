"""Элементарные алгоритмы, реализованные без библиотечных аналогов."""


def array_sum(values):
    """Сумма пустого массива равна нулю; время Θ(n), память O(1)."""
    total = 0
    for value in values:
        total += value
    return total


def array_max(values):
    """Максимум; для пустого входа ValueError, как у max()."""
    if not values:
        raise ValueError("maximum of empty array")
    largest = values[0]
    for i in range(1, len(values)):
        if values[i] > largest:
            largest = values[i]
    return largest


def count_equal_pairs(values):
    """Число равных пар с i < j. Ровно n(n−1)/2 сравнений."""
    count = 0
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            if values[i] == values[j]:
                count += 1
    return count


def binary_pow(base, exponent, mod=None):
    """Неотрицательная целая степень; mod — положительное целое."""
    if not isinstance(exponent, int) or exponent < 0:
        raise ValueError("exponent must be a nonnegative integer")
    if mod is not None and (not isinstance(mod, int) or mod <= 0):
        raise ValueError("mod must be a positive integer")
    result = 1 if mod is None else 1 % mod
    if mod is not None:
        base %= mod
    # Инвариант: result * base**exponent равен исходной степени (по mod).
    while exponent:
        if exponent & 1:
            result *= base
            if mod is not None:
                result %= mod
        exponent //= 2
        if exponent:
            base *= base
            if mod is not None:
                base %= mod
    return result
