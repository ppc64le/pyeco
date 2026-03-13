import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def test_advanced_categorical():
    print("\n" + "-"*50)
    print("📊 SUBTEST 2: Advanced Categorical Plot Test")
    print("-"*50)

    df = pd.DataFrame({
        "group": np.random.choice(["Alpha", "Beta", "Gamma"], 600),
        "score": np.random.randn(600)
    })

    print("Unique groups:", df["group"].unique())
    print("Score summary:")
    print(df["score"].describe())

    plt.figure(figsize=(6, 4))
    sns.violinplot(data=df, x="group", y="score", inner="box")
    plt.close()

    print("✅ Violin plot with inner box rendered successfully.")

if __name__ == "__main__":
    test_advanced_categorical()
