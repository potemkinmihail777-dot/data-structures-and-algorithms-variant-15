import random
import pytest
from .algorithms import HashTable, polynomial_hash, first_character_hash


@pytest.mark.parametrize(
    "hash_function", [polynomial_hash, first_character_hash, lambda key: 0]
)
def test_random_against_dict(hash_function):
    rng, table, reference = (
        random.Random(45),
        HashTable(hash_function=hash_function),
        {},
    )
    for _ in range(4000):
        key, operation = f"user_{rng.randrange(100)}", rng.randrange(3)
        if operation == 0:
            value = rng.choice([None, rng.randrange(1000)])
            table.put(key, value)
            reference[key] = value
        elif operation == 1:
            if key in reference:
                assert table.get(key) == reference[key]
            else:
                with pytest.raises(KeyError):
                    table.get(key)
        elif key in reference:
            table.delete(key)
            del reference[key]
        else:
            with pytest.raises(KeyError):
                table.delete(key)
        assert len(table) == len(reference) and table.validate()
    assert all(table.get(k) == v for k, v in reference.items())


def test_rehash_update_and_empty_key():
    table = HashTable(capacity=1)
    for i in range(300):
        table.put(str(i), i)
    assert table.rehashes > 1 and table.validate()
    assert all(table.get(str(i)) == i for i in range(300))
    capacity = len(table.buckets)
    table.put("1", None)
    assert len(table) == 300 and len(table.buckets) == capacity
    assert table.get("1") is None
    table.put("", "empty")
    assert table.get("") == "empty"
    table.delete("")
    with pytest.raises(TypeError):
        table.put(1, "not a string")


def test_threshold():
    table = HashTable(capacity=8)
    for i in range(6):
        table.put(str(i), i)
    assert len(table.buckets) == 8 and table.load_factor == 0.75
    table.put("6", 6)
    assert len(table.buckets) == 16 and table.validate()
