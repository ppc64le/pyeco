import numpy as np

print("Running subtest_numpy.py...")

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
dot_product = np.dot(a, b)
sum_a = a.sum()
mean_b = b.mean()

print("a:", a)
print("b:", b)
print("Dot product:", dot_product)
print("Sum of a:", sum_a)
print("Mean of b:", mean_b)

assert dot_product == 32
assert sum_a == 6
assert mean_b == 5.0

print("numpy test passed.")
