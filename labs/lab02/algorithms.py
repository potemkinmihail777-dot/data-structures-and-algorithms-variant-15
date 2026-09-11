"""Рекурсия, массив с удвоением ёмкости, стек и связный дек."""

from dataclasses import dataclass


def _check_n(n):
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a nonnegative integer")


def factorial(n):
    _check_n(n)
    return 1 if n < 2 else n * factorial(n - 1)


def fibonacci(n, memoized=False):
    """Вернуть (F_n, число вызовов), включая попадания в кэш."""
    _check_n(n)
    calls = 0
    cache = {}

    def visit(k):
        nonlocal calls
        calls += 1
        if memoized and k in cache:
            return cache[k]
        result = k if k < 2 else visit(k - 1) + visit(k - 2)
        if memoized:
            cache[k] = result
        return result

    return visit(n), calls


def hanoi(n, source="A", target="C", spare="B"):
    """Генератор перемещений (диск, откуда, куда), без хранения всех ходов."""
    _check_n(n)
    if len({source, target, spare}) != 3:
        raise ValueError("peg names must differ")

    def move(k, start, end, auxiliary):
        if k:
            yield from move(k - 1, start, auxiliary, end)
            yield k, start, end
            yield from move(k - 1, auxiliary, end, start)

    yield from move(n, source, target, spare)


class DynamicArray:
    """Буфер фиксированной длины; рост и копирование выполняются вручную."""

    def __init__(self):
        self.capacity = 1
        self._size = 0
        self._buffer = [None] * self.capacity
        self.copies = 0

    def __len__(self):
        return self._size

    def append(self, value):
        if self._size == self.capacity:
            replacement = [None] * (2 * self.capacity)
            for i in range(self._size):
                replacement[i] = self._buffer[i]
            self.copies += self._size
            self._buffer = replacement
            self.capacity *= 2
        self._buffer[self._size] = value
        self._size += 1

    def _index(self, index):
        if not isinstance(index, int) or not 0 <= index < self._size:
            raise IndexError("index outside 0..size-1")

    def get(self, index):
        self._index(index)
        return self._buffer[index]

    def set(self, index, value):
        self._index(index)
        self._buffer[index] = value

    def pop(self):
        if not self._size:
            raise IndexError("pop from empty array")
        self._size -= 1
        value = self._buffer[self._size]
        self._buffer[self._size] = None
        return value

    def validate(self):
        assert 0 <= self._size <= self.capacity == len(self._buffer)
        assert self.capacity > 0 and self.capacity & (self.capacity - 1) == 0
        assert all(x is None for x in self._buffer[self._size :])
        return True


class Stack:
    """LIFO на собственном динамическом массиве."""

    def __init__(self):
        self._data = DynamicArray()

    def __len__(self):
        return len(self._data)

    def push(self, value):
        self._data.append(value)

    def pop(self):
        return self._data.pop()

    def peek(self):
        return self._data.get(len(self._data) - 1)


@dataclass
class _Node:
    value: object
    previous: "_Node | None" = None
    next: "_Node | None" = None


class Deque:
    """Двусвязный список: операции на обоих концах за O(1)."""

    def __init__(self):
        self.head = self.tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node.value
            node = node.next

    def append(self, value):
        node = _Node(value, previous=self.tail)
        if self.tail is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self._size += 1

    def appendleft(self, value):
        node = _Node(value, next=self.head)
        if self.head is None:
            self.tail = node
        else:
            self.head.previous = node
        self.head = node
        self._size += 1

    def pop(self):
        if self.tail is None:
            raise IndexError("pop from empty deque")
        node = self.tail
        self.tail = node.previous
        if self.tail is None:
            self.head = None
        else:
            self.tail.next = None
        node.previous = None
        self._size -= 1
        return node.value

    def popleft(self):
        if self.head is None:
            raise IndexError("popleft from empty deque")
        node = self.head
        self.head = node.next
        if self.head is None:
            self.tail = None
        else:
            self.head.previous = None
        node.next = None
        self._size -= 1
        return node.value

    def validate(self):
        previous, current, count = None, self.head, 0
        while current is not None:
            assert current.previous is previous
            count += 1
            assert count <= self._size  # в том числе обнаружение цикла
            previous, current = current, current.next
        assert previous is self.tail and count == self._size
        assert (self.head is None) == (self.tail is None) == (self._size == 0)
        return True
