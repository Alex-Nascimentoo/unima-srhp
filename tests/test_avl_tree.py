import pytest

from src.core.avl_tree import AvlTree


def keys_from_inorder(lst):
    return [k for k, v in lst]


def test_insert_and_inorder(empty_tree):
    t = empty_tree
    items = [(30, 'a'), (20, 'b'), (40, 'c'), (10, 'd'), (25, 'e'), (35, 'f'), (50, 'g')]
    for k, v in items:
        t.insert(k, v)

    inorder = t.inorder()
    assert keys_from_inorder(inorder) == sorted([k for k, _ in items])

    # values should match the insertion mapping
    expected = {k: v for k, v in items}
    for k, v in inorder:
        assert expected[k] == v


def test_search_returns_values(empty_tree):
    t = empty_tree
    t.insert(1, 'one')
    t.insert(2, 'two')
    t.insert(3, 'three')

    assert t.search(1) == 'one'
    assert t.search(2) == 'two'
    assert t.search(3) == 'three'
    assert t.search(999) is None


def test_delete_leaf_and_internal_nodes(empty_tree):
    t = empty_tree
    for k in [20, 10, 30, 5, 15, 25, 35]:
        t.insert(k, str(k))

    # Delete a leaf
    t.delete(5)
    assert t.search(5) is None
    assert keys_from_inorder(t.inorder()) == [10, 15, 20, 25, 30, 35]

    # Delete node with one child
    t.delete(30)
    assert t.search(30) is None
    assert 30 not in keys_from_inorder(t.inorder())

    # Delete node with two children
    t.delete(20)
    assert t.search(20) is None
    assert 20 not in keys_from_inorder(t.inorder())


def test_balancing_after_rotations():
    t = AvlTree()

    # Insert in strictly decreasing order -> should cause rotations (right rotations)
    for k in [3, 2, 1]:
        t.insert(k, None)

    # After balancing the root should be 2
    assert t.root is not None
    assert t.root.key == 2

    # Insert strictly increasing order -> left rotations
    t2 = AvlTree()
    for k in [1, 2, 3]:
        t2.insert(k, None)
    assert t2.root is not None
    assert t2.root.key == 2


def test_level_order_structure(empty_tree):
    t = empty_tree
    # Build a tree where level structure is predictable
    for k in [50, 30, 70, 20, 40, 60, 80]:
        t.insert(k, k)

    levels = t.level_order()
    # top level should be the root
    assert len(levels) >= 1
    assert (levels[0][0][0] == t.root.key)

    # Check that inorder keys equal sorted keys from the inserted set
    inorder_keys = keys_from_inorder(t.inorder())
    assert inorder_keys == sorted([20, 30, 40, 50, 60, 70, 80])
