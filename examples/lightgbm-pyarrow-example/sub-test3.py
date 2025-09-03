from sklearn.datasets import make_classification, make_regression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.svm import SVC
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error

def classification_random_forest():
    print("\nTest: RandomForest Classification")
    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Accuracy: {acc:.4f}")
    assert acc > 0.8, "RandomForest classification accuracy too low"
    print("RandomForest classification passed.")

def regression_gradient_boosting():
    print("\nTest: GradientBoosting Regression")
    X, y = make_regression(n_samples=1000, n_features=10, noise=20.0, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    print(f"MSE: {mse:.4f}")
    assert mse < 2000, "GradientBoosting regression MSE too high"
    print("GradientBoosting regression passed.")

def classification_svm():
    print("\nTest: SVM Classification")
    X, y = make_classification(n_samples=1000, n_features=15, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = SVC(kernel='rbf', gamma='scale', random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Accuracy: {acc:.4f}")
    assert acc > 0.75, "SVM classification accuracy too low"
    print("SVM classification passed.")

def regression_ridge():
    print("\nTest: Ridge Regression")
    X, y = make_regression(n_samples=1000, n_features=8, noise=15.0, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('ridge', Ridge(alpha=1.0))
    ])

    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    print(f"MSE: {mse:.4f}")
    assert mse < 2000, "Ridge regression MSE too high"
    print("Ridge regression passed.")

def pipeline_rf_with_scaler():
    print("\nTest: Pipeline (Scaler + RandomForest)")
    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42))
    ])
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Accuracy: {acc:.4f}")
    assert acc > 0.8, "Pipeline classification accuracy too low"
    print("Pipeline test passed.")

if __name__ == "__main__":
    print("Starting scikit-learn comprehensive tests...\n")
    try:
        classification_random_forest()
        regression_gradient_boosting()
        classification_svm()
        regression_ridge()
        pipeline_rf_with_scaler()
        print("\nAll tests completed successfully.")
    except AssertionError as e:
        print(f"\nTest failed: {e}")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
