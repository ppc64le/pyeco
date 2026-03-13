import matplotlib.pyplot as plt
import os

print("Running subtest_matplotlib.py...")

x = [0, 1, 2, 3]
y = [0, 1, 4, 9]

plt.figure()
plt.plot(x, y, label="y = x^2")
plt.title("Matplotlib Plot Test")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()

filename = "matplotlib_test.png"
plt.savefig(filename, dpi=120)
plt.close()

assert os.path.exists(filename)
size_kb = os.path.getsize(filename) // 1024
print(f"matplotlib test passed. Plot saved to {filename} ({size_kb} KB)")
