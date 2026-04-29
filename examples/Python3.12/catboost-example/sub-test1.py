import numpy as np
import pandas as pd
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from catboost import CatBoostRegressor, Pool

def test_catboost_regression():
    print(" Starting CatBoost regression test-3...")

    # 1. Generate regression dataset
    X, y = make_regression(
        n_samples=500,
        n_features=10,
        n_informative=8,
        noise=10,
        random_state=42
    )
    print(f" Dataset created: {X.shape[0]} samples, {X.shape[1]} features")

    # 2. Convert to DataFrame
    feature_names = [f"feature_{i}" for i in range(X.shape[1])]
    df = pd.DataFrame(X, columns=feature_names)
    df['target'] = y
    print(" DataFrame created")

    # 3. Split data
    print(" Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        df[feature_names], df['target'],
        test_size=0.2,
        random_state=42
    )
    print(f" Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")

    # 4. Create Pool objects
    train_pool = Pool(X_train, y_train)
    test_pool = Pool(X_test, y_test)


    # 5. Train regressor
    model = CatBoostRegressor(
        iterations=100,
        learning_rate=0.1,
        depth=6,
        loss_function='RMSE',
        verbose=False,
        random_seed=42
    )
    model.fit(train_pool)

    # 6. Make predictions
    y_pred = model.predict(test_pool)
    print(" Predictions generated")

    # 7. Evaluate
    print(" Evaluating model...")
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f" MSE: {mse:.4f}")
    print(f" R² Score: {r2:.4f}")

    # 8. Feature importance
    feature_importance = model.get_feature_importance()
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': feature_importance
    }).sort_values('importance', ascending=False)
    print("Top 3 features:")
    print(importance_df.head(3))

    print("✅ CatBoost regression test passed successfully!")

if __name__ == "__main__":
    test_catboost_regression()