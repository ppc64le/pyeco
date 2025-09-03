import pandas as pd
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# --- Scikit-learn: Generate synthetic data ---
X, y = make_classification(n_samples=100, n_features=5, n_classes=2, random_state=42)
print("Generated data shape:", X.shape)

# --- Scikit-learn: Split and scale data ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Training features mean (approx 0):", X_train_scaled.mean(axis=0))

# --- Pandas: Create DataFrame from test data ---
df_test = pd.DataFrame(X_test_scaled, columns=[f"feature_{i}" for i in range(X.shape[1])])
df_test['true_label'] = y_test
print("\nTest DataFrame head:")
print(df_test.head())
