# catboost_example.py - Integration test for CatBoost with numpy, pandas, and scikit-learn
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
from catboost import CatBoostClassifier, Pool

print("✅ Starting CatBoost integration test...")

# ----------------------------------------
# 1. Generate synthetic dataset using scikit-learn
# ----------------------------------------
print("📊 Generating synthetic classification dataset...")
X, y = make_classification(
    n_samples=1000,
    n_features=20,
    n_informative=15,
    n_redundant=5,
    random_state=42
)
print(f"✅ Dataset created: {X.shape[0]} samples, {X.shape[1]} features")

# ----------------------------------------
# 2. Convert to pandas DataFrame
# ----------------------------------------
print("🐼 Converting to pandas DataFrame...")
feature_names = [f"feature_{i}" for i in range(X.shape[1])]
df = pd.DataFrame(X, columns=feature_names)
df['target'] = y
print("✅ DataFrame created with shape:", df.shape)

# ----------------------------------------
# 3. Split data using scikit-learn
# ----------------------------------------
print("✂️ Splitting data into train and test sets...")
X_train, X_test, y_train, y_test = train_test_split(
    df[feature_names], df['target'], 
    test_size=0.2, 
    random_state=42
)
print(f"✅ Train set: {X_train.shape[0]} samples, Test set: {X_test.shape[0]} samples")

# ----------------------------------------
# 4. Create CatBoost Pool objects
# ----------------------------------------
print("🏊 Creating CatBoost Pool objects...")
train_pool = Pool(X_train, y_train)
test_pool = Pool(X_test, y_test)
print("✅ CatBoost Pool objects created")

# ----------------------------------------
# 5. Train CatBoost model
# ----------------------------------------
print("🚀 Training CatBoost classifier...")
model = CatBoostClassifier(
    iterations=100,
    learning_rate=0.1,
    depth=6,
    loss_function='Logloss',
    verbose=False,
    random_seed=42
)
model.fit(train_pool)
print("✅ CatBoost model trained successfully")

# ----------------------------------------
# 6. Make predictions
# ----------------------------------------
print("🔮 Making predictions...")
y_pred = model.predict(test_pool)
y_pred_proba = model.predict_proba(test_pool)[:, 1]
print("✅ Predictions generated")

# ----------------------------------------
# 7. Evaluate model using scikit-learn metrics
# ----------------------------------------
print("📈 Evaluating model performance...")
accuracy = accuracy_score(y_test, y_pred)
auc_score = roc_auc_score(y_test, y_pred_proba)
print(f"✅ Accuracy: {accuracy:.4f}")
print(f"✅ AUC-ROC Score: {auc_score:.4f}")

# ----------------------------------------
# 8. Feature importance analysis
# ----------------------------------------
print("🔍 Analyzing feature importance...")
feature_importance = model.get_feature_importance()
importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': feature_importance
}).sort_values('importance', ascending=False)
print("Top 5 most important features:")
print(importance_df.head())

# ----------------------------------------
print("\n🎉 All packages tested successfully together!")
print("✅ CatBoost, NumPy, Pandas, and Scikit-learn integration complete!")


