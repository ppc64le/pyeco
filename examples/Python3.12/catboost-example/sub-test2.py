import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from catboost import CatBoostClassifier

def test_catboost_cross_validation():
    print(" Starting CatBoost cross-validation test-2...")

    # 1. Load dataset
    iris = load_iris()
    X = iris.data
    y = iris.target
    print(f" Dataset loaded: {X.shape[0]} samples, {X.shape[1]} features")

    # 2. Convert to DataFrame
    df = pd.DataFrame(X, columns=iris.feature_names)
    df['target'] = y

    # 3. Setup KFold
    print(" Performing 5-fold manual cross-validation...")
    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    scores = []

    # 4. Manual CV loop
    for fold, (train_idx, test_idx) in enumerate(kf.split(df), 1):
        print(f" Fold {fold}")

        X_train = df.iloc[train_idx][iris.feature_names]
        y_train = df.iloc[train_idx]['target']
        X_test = df.iloc[test_idx][iris.feature_names]
        y_test = df.iloc[test_idx]['target']

        model = CatBoostClassifier(
            iterations=50,
            learning_rate=0.1,
            depth=4,
            loss_function='MultiClass',
            verbose=False,
            random_seed=42
        )

        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        scores.append(acc)

        print(f"   Accuracy: {acc:.4f}")

    # 5. Results
    print(" Cross-validation results:")
    print(f"   Scores: {scores}")
    print(f"   Mean accuracy: {np.mean(scores):.4f}")
    print(f"   Std deviation: {np.std(scores):.4f}")

    print("✅ Manual cross-validation test passed successfully!")

if __name__ == "__main__":
    test_catboost_cross_validation()