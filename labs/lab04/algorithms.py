"""Стабильные Merge/Counting/Radix и HeapSort in-place."""


def identity(value):
    return value


def merge_sort(a, key=identity):
    auxiliary = [None] * len(a)

    def sort(lo, hi):
        if hi - lo < 2:
            return
        mid = (lo + hi) // 2
        sort(lo, mid)
        sort(mid, hi)
        i, j = lo, mid
        for k in range(lo, hi):
            if i < mid and (j == hi or key(a[i]) <= key(a[j])):
                auxiliary[k] = a[i]
                i += 1
            else:
                auxiliary[k] = a[j]
                j += 1
        for k in range(lo, hi):
            a[k] = auxiliary[k]

    sort(0, len(a))


def counting_sort(a, key=identity, max_range=2_000_001):
    """Целочисленные ключи, включая отрицательные; защита от огромного диапазона."""
    if not a:
        return
    keys = [key(value) for value in a]
    if any(not isinstance(value, int) for value in keys):
        raise TypeError("integer keys required")
    minimum, maximum = min(keys), max(keys)
    width = maximum - minimum + 1
    if width > max_range:
        raise ValueError("key range exceeds memory limit; use MergeSort or RadixSort")
    counts = [0] * width
    for value in keys:
        counts[value - minimum] += 1
    for i in range(1, width):
        counts[i] += counts[i - 1]
    result = [None] * len(a)
    for i in range(len(a) - 1, -1, -1):
        bucket = keys[i] - minimum
        counts[bucket] -= 1
        result[counts[bucket]] = a[i]
    a[:] = result


def radix_sort(a, key=identity):
    """LSD по десятичным цифрам; смещение min поддерживает отрицательные ключи."""
    if not a:
        return
    raw = [key(value) for value in a]
    if any(not isinstance(value, int) for value in raw):
        raise TypeError("integer keys required")
    minimum = min(raw)
    keys = [value - minimum for value in raw]
    maximum, place = max(keys), 1
    while maximum // place:
        counts = [0] * 10
        for value in keys:
            counts[(value // place) % 10] += 1
        for digit in range(1, 10):
            counts[digit] += counts[digit - 1]
        values_out, keys_out = [None] * len(a), [0] * len(a)
        for i in range(len(a) - 1, -1, -1):
            digit = (keys[i] // place) % 10
            counts[digit] -= 1
            values_out[counts[digit]] = a[i]
            keys_out[counts[digit]] = keys[i]
        a[:] = values_out
        keys = keys_out
        place *= 10


def heap_sort(a, key=identity):
    """Макс-куча, построенная снизу; дополнительная память O(1)."""

    def sift_down(root, end):
        while 2 * root + 1 < end:
            child = 2 * root + 1
            if child + 1 < end and key(a[child]) < key(a[child + 1]):
                child += 1
            if key(a[root]) >= key(a[child]):
                break
            a[root], a[child] = a[child], a[root]
            root = child

    for root in range(len(a) // 2 - 1, -1, -1):
        sift_down(root, len(a))
    for end in range(len(a) - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift_down(0, end)
