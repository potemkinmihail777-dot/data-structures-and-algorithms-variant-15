from bisect import bisect_left
import random
import pytest
from .algorithms import linear_search, binary_search, interpolation_search


@pytest.mark.parametrize("search", [linear_search, binary_search, interpolation_search])
def test_search_oracles(search):
    rng = random.Random(45)
    cases = [[], [0], [7] * 50, [-9, -2, 0, 6, 30], [0, 1, 2, 10**30]]
    cases += [
        sorted(rng.randrange(-200, 200) for _ in range(rng.randrange(100)))
        for _ in range(400)
    ]
    for a in cases:
        targets = [-201, 201, 0, 7] + a[:2] + a[-2:]
        for target in targets:
            index, count = search(a, target)
            oracle = bisect_left(a, target)
            exists = oracle < len(a) and a[oracle] == target
            assert (index != -1) == exists
            assert index == -1 or a[index] == target
            assert count >= 0


def test_counter_definition():
    assert linear_search([1, 2, 3], 4) == (-1, 3)
    assert binary_search([1, 2, 3], 2) == (1, 1)
    assert interpolation_search([7, 7], 7) == (0, 3)
    for search in (linear_search, binary_search, interpolation_search):
        assert search([], 0) == (-1, 0)
