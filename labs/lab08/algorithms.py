"""Ассоциативная таблица строковых ключей, без dict внутри реализации."""


def polynomial_hash(key):
    value = 0
    for char in key:
        value = (value * 131 + ord(char)) % 1_000_000_007
    return value


def first_character_hash(key):
    return ord(key[0]) if key else 0


class HashTable:
    def __init__(self, capacity=8, hash_function=polynomial_hash, auto_resize=True):
        if not isinstance(capacity, int) or capacity < 1:
            raise ValueError("capacity must be positive")
        self.buckets = [[] for _ in range(capacity)]
        self._size = 0
        self.hash_function = hash_function
        # Отключение роста используется только в контролируемом опыте по α.
        self.auto_resize = auto_resize
        self.rehashes = 0

    def __len__(self):
        return self._size

    @property
    def load_factor(self):
        return self._size / len(self.buckets)

    def _bucket(self, key):
        if not isinstance(key, str):
            raise TypeError("only string keys are supported")
        return self.buckets[self.hash_function(key) % len(self.buckets)]

    def put(self, key, value):
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self._size += 1
        if self.auto_resize and self.load_factor > 0.75:
            self._rehash()

    def get(self, key):
        for stored_key, value in self._bucket(key):
            if stored_key == key:
                return value
        raise KeyError(key)

    def delete(self, key):
        bucket = self._bucket(key)
        for index, pair in enumerate(bucket):
            if pair[0] == key:
                del bucket[index]
                self._size -= 1
                return
        raise KeyError(key)

    def _rehash(self):
        old = self.buckets
        self.buckets = [[] for _ in range(2 * len(old))]
        for bucket in old:
            for key, value in bucket:
                self._bucket(key).append([key, value])
        self.rehashes += 1

    def chain_lengths(self):
        return [len(bucket) for bucket in self.buckets]

    def validate(self):
        seen = set()
        for index, bucket in enumerate(self.buckets):
            for key, _ in bucket:
                assert self.hash_function(key) % len(self.buckets) == index
                assert key not in seen
                seen.add(key)
        assert len(seen) == self._size
        assert not self.auto_resize or self.load_factor <= 0.75
        return True
