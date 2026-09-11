from collections import Counter
import random
import pytest
from .algorithms import merge_sort, counting_sort, radix_sort, heap_sort


@pytest.mark.parametrize("sort", [merge_sort, counting_sort, radix_sort, heap_sort])
def test_sort_oracles(sort):
    rng = random.Random(45)
    cases = [[], [3], [3] * 60, list(range(100)), list(range(100, -1, -1))]
    cases += [
        [rng.randint(-100, 100) for _ in range(rng.randrange(120))] for _ in range(400)
    ]
    for before in cases:
        after = before.copy()
        sort(after)
        assert after == sorted(before)
        assert Counter(after) == Counter(before)


@pytest.mark.parametrize("sort", [merge_sort, counting_sort, radix_sort])
def test_stability(sort):
    rng = random.Random(45)
    for _ in range(200):
        before = [(rng.randrange(-5, 6), i) for i in range(70)]
        after = before.copy()
        sort(after, key=lambda x: x[0])
        assert after == sorted(before, key=lambda x: x[0])


def test_range_and_large_signed_integers():
    with pytest.raises(ValueError):
        counting_sort([-(10**12), 10**12])
    with pytest.raises(TypeError):
        counting_sort([1.5])
    values = [-(10**30), 10**30, 0, -1, 1]
    expected = sorted(values)
    radix_sort(values)
    assert values == expected
