import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score
from catboost import CatBoostClassifier

def test_catboost_cross_validation():
    print("🚀 Starting CatBoost cross-validation test...")

    # 1. Load iris dataset
    print("🌸 Loading Iris dataset...")
    iris = load_iris()
    X = iris.data
    y = iris.target
    print(f"✅ Dataset loaded: {X.shape[0]} samples, {X.shape[1]} features, {len(np.unique(y))} classes")

    # 2. Convert to DataFrame
    print("🐼 Converting to pandas DataFrame...")
    df = pd.DataFrame(X, columns=iris.feature_names)
    df['target'] = y
    print("✅ DataFrame created with shape:", df.shape)

    # 3. Create CatBoost classifier
    print("🤖 Creating CatBoost classifier...")
    model = CatBoostClassifier(
        iterations=50,
        learning_rate=0.1,
        depth=4,
        loss_function='MultiClass',
        verbose=False,
        random_seed=42
    )
    print("✅ Classifier created")

    # 4. Perform cross-validation
    print("🔄 Performing 5-fold cross-validation...")
    cv_scores = cross_val_score(
        model, 
        df[iris.feature_names], 
        df['target'],
        cv=5,
        scoring='accuracy'
    )
    print("✅ Cross-validation completed")

    # 5. Display results
    print("📊 Cross-validation results:")
    print(f"   Scores: {cv_scores}")
    print(f"   Mean accuracy: {cv_scores.mean():.4f}")
    print(f"   Std deviation: {cv_scores.std():.4f}")

    # 6. Train on full dataset
    print("🚀 Training on full dataset...")
    model.fit(df[iris.feature_names], df['target'])
    print("✅ Model trained")

    # 7. Get feature importance
    print("🔍 Feature importance:")
    feature_importance = model.get_feature_importance()
    for name, importance in zip(iris.feature_names, feature_importance):
        print(f"   {name}: {importance:.4f}")

    # 8. Test prediction
    print("🔮 Testing prediction on sample data...")
    sample = df[iris.feature_names].iloc[0:1]
    prediction = model.predict(sample)
    print(f"✅ Sample prediction: {prediction[0]} (actual: {df['target'].iloc[0]})")

    print("✅ CatBoost cross-validation test passed successfully!")

if __name__ == "__main__":
    test_catboost_cross_validation()

# Made with Bob
