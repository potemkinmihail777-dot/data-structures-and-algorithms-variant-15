from itertools import product
import random
import pytest
from .algorithms import (
    naive_search,
    kmp_search,
    rabin_karp_search,
    boyer_moore_search,
    prefix_function,
)

SEARCHES = [naive_search, kmp_search, rabin_karp_search, boyer_moore_search]


def reference(text, pattern):
    positions, start = [], 0
    while start <= len(text):
        index = text.find(pattern, start)
        if index < 0:
            break
        positions.append(index)
        start = index + 1
    return positions


@pytest.mark.parametrize("search", SEARCHES)
def test_random_and_boundaries(search):
    rng = random.Random(45)
    cases = [("", ""), ("", "a"), ("aaaaa", "aaa"), ("ёжёжёж", "ёж"), ("abc", "abcd")]
    cases += [
        (
            "".join(rng.choices("abв😀 ", k=rng.randrange(100))),
            "".join(rng.choices("abв😀 ", k=rng.randrange(15))),
        )
        for _ in range(600)
    ]
    for text, pattern in cases:
        positions, comparisons = search(text, pattern)
        assert positions == reference(text, pattern)
        assert comparisons >= 0


def test_boyer_moore_exhaustive_binary():
    texts = ["".join(chars) for n in range(7) for chars in product("ab", repeat=n)]
    patterns = ["".join(chars) for n in range(5) for chars in product("ab", repeat=n)]
    for text in texts:
        for pattern in patterns:
            assert boyer_moore_search(text, pattern)[0] == reference(text, pattern)
            assert boyer_moore_search(text, pattern, False)[0] == reference(
                text, pattern
            )


def test_collision_and_prefix():
    # При base=1 хеши 'ab' и 'ba' одинаковы, но строки различаются.
    assert rabin_karp_search("ba", "ab", base=1, modulus=2)[0] == []
    assert rabin_karp_search("baba", "ab", base=1, modulus=2)[0] == [1]
    assert prefix_function("ababaca") == [0, 0, 1, 2, 3, 0, 1]
    assert prefix_function("") == []
