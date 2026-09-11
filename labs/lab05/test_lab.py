import random
from .algorithms import BST


def build(values):
    tree = BST()
    for value in values:
        tree.insert(value)
    return tree


def test_traversals_and_height():
    tree = build([4, 2, 6, 1, 3, 5, 7])
    assert tree.inorder() == [1, 2, 3, 4, 5, 6, 7]
    assert tree.preorder() == [4, 2, 1, 3, 6, 5, 7]
    assert tree.postorder() == [1, 3, 2, 5, 7, 6, 4]
    assert tree.levelorder() == [4, 2, 6, 1, 3, 5, 7]
    assert tree.height() == 2 and tree.count_nodes() == len(tree) == 7
    assert BST().height() == -1


def test_delete_shapes():
    for values in ([4], [4, 2], [4, 6], [4, 2, 6], [4, 2, 8, 6, 7, 9, 5]):
        for key in values:
            tree = build(values)
            assert tree.delete(key)
            assert not tree.delete(key)
            assert tree.inorder() == sorted(set(values) - {key})
            assert tree.validate()


def test_random_operations():
    rng, tree, reference = random.Random(45), BST(), set()
    for _ in range(4000):
        key, operation = rng.randrange(-200, 200), rng.randrange(3)
        if operation == 0:
            assert tree.insert(key) == (key not in reference)
            reference.add(key)
        elif operation == 1:
            assert tree.delete(key) == (key in reference)
            reference.discard(key)
        else:
            assert tree.search(key) == (key in reference)
        assert tree.inorder() == sorted(reference)
        assert tree.validate() and len(tree) == len(reference)


def test_degenerate_tree_iterative_operations():
    tree = build(range(1200))
    assert tree.height() == 1199 and tree.search(1199)
    assert tree.delete(600) and tree.validate()
