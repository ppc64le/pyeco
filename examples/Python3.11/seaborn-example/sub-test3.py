import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def test_theme_and_style_rendering():
    print("\n" + "-"*50)
    print("🎨 SUBTEST 3: Seaborn Theme & Style Test")
    print("-"*50)

    sns.set_theme(style="darkgrid", palette="muted")

    x = np.linspace(0, 2 * np.pi, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)

    print("Plotting sine and cosine curves with theme...")

    plt.figure()
    sns.lineplot(x=x, y=y1, label="sin(x)")
    sns.lineplot(x=x, y=y2, label="cos(x)")
    plt.title("Trigonometric Curves")
    plt.xlabel("x")
    plt.ylabel("value")
    plt.legend()
    plt.close()

    print("✅ Themed line plot rendered successfully.")

if __name__ == "__main__":
    test_theme_and_style_rendering()
