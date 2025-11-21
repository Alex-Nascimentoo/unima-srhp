import pytest
from src.core.avl_tree import AvlTree

def extract_structure(tree):
    """Return simplified structure: (root, left child, right child) keys or None."""
    r = tree.root
    return (
        r.key if r else None,
        r.left.key if r and r.left else None,
        r.right.key if r and r.right else None,
    )

def test_single_right_rotation():
    # Causes RR imbalance -> right rotation
    t = AvlTree()
    for k in [30, 20, 10]:
        t.insert(k, None)

    # Expect 20 to be root
    assert extract_structure(t) == (20, 10, 30)

def test_single_left_rotation():
    # Causes LL imbalance -> left rotation
    t = AvlTree()
    for k in [10, 20, 30]:
        t.insert(k, None)

    # Expect 20 to be root
    assert extract_structure(t) == (20, 10, 30)

def test_left_right_rotation():
    # Causes LR imbalance
    t = AvlTree()
    for k in [30, 10, 20]:
        t.insert(k, None)

    # Expect 20 root
    assert extract_structure(t) == (20, 10, 30)

def test_right_left_rotation():
    # Causes RL imbalance
    t = AvlTree()
    for k in [10, 30, 20]:
        t.insert(k, None)

    # Expect 20 root
    assert extract_structure(t) == (20, 10, 30)

def test_rotation_after_delete():
    # Complex structure then delete to force rebalance
    t = AvlTree()
    for k in [50, 30, 70, 20, 40, 60, 80, 10]:
        t.insert(k, None)

    t.delete(80)  # triggers rebalance

    assert t.root.key == 50
    inorder = [k for k, _ in t.inorder()]
    assert inorder == [10, 20, 30, 40, 50, 60, 70]
