"""BST с уникальными сравнимыми ключами. Высота измеряется числом рёбер."""

from collections import deque
from dataclasses import dataclass


@dataclass
class Node:
    key: object
    left: "Node | None" = None
    right: "Node | None" = None


class BST:
    def __init__(self):
        self.root = None
        self._size = 0

    def __len__(self):
        return self._size

    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
            self._size = 1
            return True
        node = self.root
        while True:
            if key == node.key:
                return False
            side = "left" if key < node.key else "right"
            child = getattr(node, side)
            if child is None:
                setattr(node, side, Node(key))
                self._size += 1
                return True
            node = child

    def search(self, key):
        node = self.root
        while node is not None:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def delete(self, key):
        parent, node = None, self.root
        while node is not None and key != node.key:
            parent, node = node, node.left if key < node.key else node.right
        if node is None:
            return False
        if node.left is not None and node.right is not None:
            # У преемника нет левого ребёнка: сводим удаление к простому случаю.
            successor_parent, successor = node, node.right
            while successor.left is not None:
                successor_parent, successor = successor, successor.left
            node.key = successor.key
            parent, node = successor_parent, successor
        child = node.left if node.left is not None else node.right
        if parent is None:
            self.root = child
        elif parent.left is node:
            parent.left = child
        else:
            parent.right = child
        self._size -= 1
        return True

    def _traverse(self, order):
        result = []

        def visit(node):
            if node is None:
                return
            if order == "pre":
                result.append(node.key)
            visit(node.left)
            if order == "in":
                result.append(node.key)
            visit(node.right)
            if order == "post":
                result.append(node.key)

        visit(self.root)
        return result

    def inorder(self):
        return self._traverse("in")

    def preorder(self):
        return self._traverse("pre")

    def postorder(self):
        return self._traverse("post")

    def levelorder(self):
        queue = deque([self.root]) if self.root is not None else deque()
        result = []
        while queue:
            node = queue.popleft()
            result.append(node.key)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        return result

    def height(self):
        maximum = -1
        stack = [(self.root, 0)] if self.root is not None else []
        while stack:
            node, depth = stack.pop()
            maximum = max(maximum, depth)
            if node.left is not None:
                stack.append((node.left, depth + 1))
            if node.right is not None:
                stack.append((node.right, depth + 1))
        return maximum

    def count_nodes(self):
        return len(self.levelorder())

    def validate(self):
        # Итеративная проверка также работает на очень глубоком дереве.
        stack = [(self.root, None, None)] if self.root is not None else []
        count, seen = 0, set()
        while stack:
            node, lower, upper = stack.pop()
            assert id(node) not in seen
            seen.add(id(node))
            assert lower is None or lower < node.key
            assert upper is None or node.key < upper
            count += 1
            if node.left is not None:
                stack.append((node.left, lower, node.key))
            if node.right is not None:
                stack.append((node.right, node.key, upper))
        assert count == self._size
        return True
