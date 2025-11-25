import math
import time
from src.core.avl_tree import AvlTree

# Expected AVL height bounds
def expected_max_height(n):
    # theoretical AVL height: <= 1.44 * log2(n+2) - 0.328
    return int(1.44 * math.log2(n + 2) - 0.328) + 1

def test_massive_insert_performance():
    t = AvlTree()
    AMOUNT = 20000  # Stress test

    start = time.time()
    for i in range(AMOUNT):
        t.insert(i, None)
    duration = time.time() - start

    # Must finish fast (< 0.7s typical limit)
    assert duration < 1.2, f"Insertion too slow: {duration:.3f}s"

    # Height must be logarithmic
    h = t.height()
    assert h <= expected_max_height(AMOUNT), f"Tree too tall: {h}"

def test_randomized_insert_delete_performance():
    import random
    t = AvlTree()
    AMOUNT = 10000
    keys = list(range(AMOUNT))
    random.shuffle(keys)

    # Insert shuffled
    for k in keys:
        t.insert(k, k)

    # Random deletions
    random.shuffle(keys)
    delete_sample = keys[:AMOUNT // 4]

    start = time.time()
    for k in delete_sample:
        t.delete(k)
    duration = time.time() - start

    assert duration < 1.2, f"Delete operations too slow: {duration:.3f}s"
