# seaborn-full-example.py

import io
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

print("="*60)
print("🚀 STARTING FULL SEABORN INTEGRATION TEST")
print("="*60)

print(f"Seaborn version: {sns.__version__}")
print(f"Pandas version: {pd.__version__}")
print(f"NumPy version: {np.__version__}")

# ----------------------------------------
# 1. Dataset Creation
# ----------------------------------------
print("\n📊 Generating dataset...")
np.random.seed(123)

rows = 2000
df = pd.DataFrame({
    "feature1": np.random.normal(0, 1, rows),
    "feature2": np.random.normal(5, 2, rows),
    "feature3": np.random.uniform(-3, 3, rows),
    "category": np.random.choice(["A", "B", "C"], rows)
})

print("Dataset shape:", df.shape)
print("Dataset summary:")
print(df.describe())

# ----------------------------------------
# 2. Correlation Matrix
# ----------------------------------------
print("\n🔥 Computing correlation matrix...")
corr = df[["feature1", "feature2", "feature3"]].corr()
print("Correlation matrix:")
print(corr)

plt.figure()
sns.heatmap(corr, annot=True)
plt.close()
print("✅ Heatmap rendered successfully")

# ----------------------------------------
# 3. Regression Plot
# ----------------------------------------
print("\n📈 Performing regression analysis...")

# compute regression manually for terminal output
coef = np.polyfit(df["feature1"], df["feature2"], 1)
print(f"Regression slope: {coef[0]:.4f}")
print(f"Regression intercept: {coef[1]:.4f}")

plt.figure()
sns.regplot(data=df, x="feature1", y="feature2")
plt.close()

print("✅ Regression plot rendered")

# ----------------------------------------
# 4. FacetGrid
# ----------------------------------------
print("\n🧩 Creating FacetGrid by category...")
g = sns.FacetGrid(df, col="category")
g.map_dataframe(sns.scatterplot, x="feature1", y="feature3")
plt.close()

print("Categories found:", df["category"].unique())
print("✅ FacetGrid rendered")

# ----------------------------------------
# 5. Pairplot
# ----------------------------------------
print("\n🔎 Creating pairplot sample...")
sample_df = df.sample(300)
sns.pairplot(sample_df, hue="category")
plt.close()

print("Pairplot sample size:", sample_df.shape)
print("✅ Pairplot rendered")

# ----------------------------------------
# 6. Save & Validate Image
# ----------------------------------------
print("\n💾 Saving validation plot to memory...")

plt.figure()
sns.boxplot(data=df, x="category", y="feature2")

buffer = io.BytesIO()
plt.savefig(buffer, format="PNG")
plt.close()
buffer.seek(0)

image_size = len(buffer.getvalue())
print(f"Generated image size (bytes): {image_size}")

img = Image.open(buffer)
img.verify()

print("✅ Image verified using Pillow")

print("\n" + "="*60)
print("🎉 FULL SEABORN INTEGRATION TEST PASSED SUCCESSFULLY")
print("="*60)
