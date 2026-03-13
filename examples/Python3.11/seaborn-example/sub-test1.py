import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def test_distribution_stress():
    print("\n" + "-"*50)
    print("🎯 SUBTEST 1: Distribution Stress Test")
    print("-"*50)

    data = pd.DataFrame({
        "values": np.random.randn(5000),
        "group": np.random.choice(["G1", "G2", "G3"], 5000)
    })

    print("Data shape:", data.shape)
    print("Group counts:")
    print(data["group"].value_counts())

    mean_val = data["values"].mean()
    std_val = data["values"].std()

    print(f"Mean: {mean_val:.4f}")
    print(f"Std Dev: {std_val:.4f}")

    plt.figure()
    sns.histplot(data=data, x="values", hue="group", kde=True, bins=50)
    plt.close()

    print("✅ Distribution plot rendered successfully")

if __name__ == "__main__":
    test_distribution_stress()
