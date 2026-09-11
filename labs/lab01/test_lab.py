from collections import Counter
import random
import pytest
from .algorithms import array_sum, array_max, count_equal_pairs, binary_pow


@pytest.mark.parametrize("values", [[], [4], [2, 2, 2], [-2, 3, -2], list(range(30))])
def test_boundary(values):
    assert array_sum(values) == sum(values)
    assert count_equal_pairs(values) == sum(
        c * (c - 1) // 2 for c in Counter(values).values()
    )
    if values:
        assert array_max(values) == max(values)
    else:
        with pytest.raises(ValueError):
            array_max(values)


def test_random_oracles():
    rng = random.Random(45)
    for _ in range(400):
        values = [rng.randint(-30, 30) for _ in range(rng.randrange(70))]
        assert array_sum(values) == sum(values)
        assert count_equal_pairs(values) == sum(
            c * (c - 1) // 2 for c in Counter(values).values()
        )
        if values:
            assert array_max(values) == max(values)
        base, exponent, mod = (
            rng.randint(-100, 100),
            rng.randrange(65),
            rng.randint(1, 1000),
        )
        assert binary_pow(base, exponent, mod) == pow(base, exponent, mod)
        assert binary_pow(base, exponent) == pow(base, exponent)


@pytest.mark.parametrize("args", [(2, -1), (2, 2.5), (2, 3, 0), (2, 3, -5)])
def test_invalid(args):
    with pytest.raises(ValueError):
        binary_pow(*args)
