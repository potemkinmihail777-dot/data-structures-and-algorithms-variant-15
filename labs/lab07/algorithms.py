"""Все вхождения, включая пересечения; пустой шаблон — позиции 0..n.

Возвращается (список позиций, число сравнений символов), включая
предобработку. Сравнения хешей и индексов не считаются символьными.
"""


def naive_search(text, pattern):
    positions, comparisons = [], 0
    for shift in range(len(text) - len(pattern) + 1):
        matched = True
        for j, char in enumerate(pattern):
            comparisons += 1
            if text[shift + j] != char:
                matched = False
                break
        if matched:
            positions.append(shift)
    return positions, comparisons


def _prefix_counted(pattern):
    pi, comparisons = [0] * len(pattern), 0
    for i in range(1, len(pattern)):
        j = pi[i - 1]
        while True:
            comparisons += 1
            if pattern[i] == pattern[j]:
                j += 1
                break
            if j == 0:
                break
            j = pi[j - 1]
        pi[i] = j
    return pi, comparisons


def prefix_function(pattern):
    return _prefix_counted(pattern)[0]


def kmp_search(text, pattern):
    if not pattern:
        return list(range(len(text) + 1)), 0
    pi, comparisons = _prefix_counted(pattern)
    positions, j = [], 0
    for i, char in enumerate(text):
        while True:
            comparisons += 1
            if char == pattern[j]:
                j += 1
                break
            if j == 0:
                break
            j = pi[j - 1]
        if j == len(pattern):
            positions.append(i - len(pattern) + 1)
            j = pi[j - 1]
    return positions, comparisons


def rabin_karp_search(text, pattern, base=257, modulus=1_000_000_007):
    if modulus < 2 or base < 1:
        raise ValueError("positive base and modulus >= 2 required")
    n, m = len(text), len(pattern)
    if not m:
        return list(range(n + 1)), 0
    if m > n:
        return [], 0
    high = pow(base, m - 1, modulus)
    target_hash = window_hash = 0
    for j in range(m):
        target_hash = (target_hash * base + ord(pattern[j])) % modulus
        window_hash = (window_hash * base + ord(text[j])) % modulus
    positions, comparisons = [], 0
    for shift in range(n - m + 1):
        if target_hash == window_hash:
            match = True
            for j in range(m):
                comparisons += 1
                if text[shift + j] != pattern[j]:
                    match = False
                    break
            if match:
                positions.append(shift)
        if shift < n - m:
            window_hash = (
                (window_hash - ord(text[shift]) * high) * base + ord(text[shift + m])
            ) % modulus
    return positions, comparisons


def good_suffix_table(pattern):
    """Линейная предобработка strong good suffix: (сдвиги, сравнения).

    shift[j+1] используется при несовпадении на j, shift[0] — после совпадения.
    border[i] хранит начало следующей границы суффикса pattern[i:].
    """
    m = len(pattern)
    shifts, borders, comparisons = [0] * (m + 1), [0] * (m + 1), 0
    i, j = m, m + 1
    borders[i] = j
    while i > 0:
        while j <= m:
            comparisons += 1
            if pattern[i - 1] == pattern[j - 1]:
                break
            if shifts[j] == 0:
                shifts[j] = j - i
            j = borders[j]
        i -= 1
        j -= 1
        borders[i] = j
    j = borders[0]
    for i in range(m + 1):
        if shifts[i] == 0:
            shifts[i] = j
        if i == j:
            j = borders[j]
    return shifts, comparisons


def boyer_moore_search(text, pattern, good_suffix=True):
    n, m = len(text), len(pattern)
    if not m:
        return list(range(n + 1)), 0
    last = {char: i for i, char in enumerate(pattern)}
    shifts, comparisons = (
        good_suffix_table(pattern) if good_suffix else ([1] * (m + 1), 0)
    )
    positions, shift = [], 0
    while shift <= n - m:
        j = m - 1
        while j >= 0:
            comparisons += 1
            if pattern[j] != text[shift + j]:
                break
            j -= 1
        if j < 0:
            positions.append(shift)
            shift += shifts[0]
        else:
            bad_character = j - last.get(text[shift + j], -1)
            shift += max(1, bad_character, shifts[j + 1])
    return positions, comparisons
