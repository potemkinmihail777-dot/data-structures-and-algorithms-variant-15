from collections import Counter
import random
import pytest
from .algorithms import bubble_sort, insertion_sort, selection_sort, quick_sort

SORTS = [bubble_sort, insertion_sort, selection_sort, quick_sort]


@pytest.mark.parametrize("sort", SORTS)
def test_sort_oracles(sort):
    rng = random.Random(45)
    cases = [[], [0], [2] * 100, list(range(100)), list(range(100, -1, -1))]
    cases += [
        [rng.randint(-25, 25) for _ in range(rng.randrange(100))] for _ in range(400)
    ]
    for before in cases:
        after = before.copy()
        sort(after, **({"rng": rng} if sort is quick_sort else {}))
        assert after == sorted(before)
        assert Counter(after) == Counter(before)


@pytest.mark.parametrize("sort", [bubble_sort, insertion_sort])
def test_stability(sort):
    before = [(2, "a"), (2, "b"), (1, "c"), (2, "d"), (1, "e")]
    after = before.copy()
    sort(after, key=lambda pair: pair[0])
    assert after == sorted(before, key=lambda pair: pair[0])


def test_exact_counters():
    for n in range(2, 30):
        assert selection_sort(list(range(n))).comparisons == n * (n - 1) // 2
        assert bubble_sort(list(range(n))).comparisons == n - 1
        assert insertion_sort(list(range(n))).comparisons == n - 1
    stats = bubble_sort([3, 2, 1])
    assert (stats.comparisons, stats.swaps, stats.moves) == (3, 3, 6)


def test_quicksort_deep_and_equal():
    a = list(range(12000))
    quick_sort(a, rng=random.Random(45))
    assert a == list(range(12000))
    equal = [7] * 12000
    assert quick_sort(equal, rng=random.Random(45)).comparisons == 24000


@pytest.mark.parametrize("sort", [selection_sort, quick_sort])
def test_instability_witness(sort):
    before = [(2, "a"), (2, "b"), (1, "c")]
    after = before.copy()
    sort(after, key=lambda pair: pair[0])
    assert after == [(1, "c"), (2, "b"), (2, "a")]
