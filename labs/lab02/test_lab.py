from collections import deque
import math
import random
import pytest
from .algorithms import factorial, fibonacci, hanoi, DynamicArray, Stack, Deque


def test_recursion():
    previous, current = 0, 1
    for n in range(18):
        assert factorial(n) == math.factorial(n)
        plain, calls = fibonacci(n)
        cached, cached_calls = fibonacci(n, True)
        assert plain == cached == previous
        if n >= 2:
            assert cached_calls == 2 * n - 1
            assert calls >= cached_calls
        previous, current = current, previous + current


@pytest.mark.parametrize("n", range(11))
def test_hanoi_legal_moves(n):
    pegs = {"A": list(range(n, 0, -1)), "B": [], "C": []}
    count = 0
    for disk, source, target in hanoi(n):
        assert pegs[source].pop() == disk
        assert not pegs[target] or pegs[target][-1] > disk
        pegs[target].append(disk)
        count += 1
    assert count == 2**n - 1
    assert pegs["C"] == list(range(n, 0, -1))


def test_array_growth_and_access():
    a = DynamicArray()
    for i in range(1025):
        a.append(i)
        assert a.get(i) == i
        assert a.validate()
    assert a.capacity == 2048 and a.copies == 2047
    assert a.copies < 2 * len(a)
    a.set(0, None)
    assert a.get(0) is None
    for index in (-1, len(a)):
        with pytest.raises(IndexError):
            a.get(index)
    while len(a):
        a.pop()
    with pytest.raises(IndexError):
        a.pop()
    assert a.validate()


def test_random_stack_and_deque():
    rng, stack, stack_ref, own, ref = random.Random(45), Stack(), [], Deque(), deque()
    for _ in range(3000):
        value = rng.randrange(100)
        if not stack_ref or rng.random() < 0.6:
            stack.push(value)
            stack_ref.append(value)
        else:
            assert stack.peek() == stack_ref[-1]
            assert stack.pop() == stack_ref.pop()
        op = rng.choice(("append", "appendleft", "pop", "popleft"))
        if op.startswith("append"):
            getattr(own, op)(value)
            getattr(ref, op)(value)
        elif ref:
            assert getattr(own, op)() == getattr(ref, op)()
        else:
            with pytest.raises(IndexError):
                getattr(own, op)()
        assert list(own) == list(ref)
        assert len(stack) == len(stack_ref)
        assert own.validate()


def test_negative_recursion():
    for function in (factorial, fibonacci, lambda n: list(hanoi(n))):
        with pytest.raises(ValueError):
            function(-1)
