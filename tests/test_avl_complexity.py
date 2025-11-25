import os
import time
import math
import random
import matplotlib.pyplot as plt

from src.core.avl_tree import AvlTree

RESULT_DIR = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(RESULT_DIR, exist_ok=True)


def measure_time(operation, *args):
    start = time.perf_counter()
    operation(*args)
    return time.perf_counter() - start


def test_avl_complexity_insert_and_search():
    sizes = [100, 200, 400, 800, 1600, 3200]

    insert_times = []
    search_times = []

    for n in sizes:
        tree = AvlTree()
        data = random.sample(range(1, n * 10), n)

        # Measure insertion times
        total_insert = 0
        for value in data:
            total_insert += measure_time(tree.insert, value)
        insert_times.append(total_insert / n)

        # Measure search times
        total_search = 0
        for value in data:
            total_search += measure_time(tree.search, value)
        search_times.append(total_search / n)

    # Theoretical complexity curve (normalized)
    theoretical = [math.log2(n) for n in sizes]
    max_real = max(max(insert_times), max(search_times))
    coef = max_real / max(theoretical)
    theoretical = [t * coef for t in theoretical]

    # Plot results
    plt.figure(figsize=(10, 6))
    plt.title("AVL Tree | Complexity Experiment")
    plt.plot(sizes, insert_times, label="Insert (experimental)", marker="o")
    plt.plot(sizes, search_times, label="Search (experimental)", marker="o")
    plt.plot(sizes, theoretical, label="O(log n) (reference)", linestyle="--")
    plt.xlabel("Number of elements (n)")
    plt.ylabel("Average time (seconds)")
    plt.legend()
    plt.grid(True)

    output_file = os.path.join(RESULT_DIR, "avl_complexity.png")
    plt.savefig(output_file)

    print(f"\n[Complexity Graph Generated] -> {output_file}\n")
