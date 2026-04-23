import numpy as np
import pandas as pd
from catboost import CatBoostClassifier, Pool

def test_catboost_with_categorical_features():
    print("🧪 Starting CatBoost categorical features test...")

    # 1. Create dataset with categorical features
    print("📊 Creating dataset with categorical features...")
    np.random.seed(42)
    n_samples = 200
    
    data = {
        'age': np.random.randint(18, 70, n_samples),
        'income': np.random.randint(20000, 100000, n_samples),
        'city': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston'], n_samples),
        'education': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], n_samples),
        'employment': np.random.choice(['Full-time', 'Part-time', 'Self-employed'], n_samples)
    }
    
    # Create target based on some logic
    df = pd.DataFrame(data)
    df['target'] = ((df['age'] > 40) & (df['income'] > 50000)).astype(int)
    
    print(f"✅ Dataset created: {df.shape[0]} samples, {df.shape[1]-1} features")
    print(f"   Categorical features: city, education, employment")
    print(f"   Target distribution: {df['target'].value_counts().to_dict()}")

    # 2. Split data manually
    print("✂️ Splitting data...")
    train_size = int(0.8 * len(df))
    train_df = df.iloc[:train_size]
    test_df = df.iloc[train_size:]
    print(f"✅ Train: {len(train_df)}, Test: {len(test_df)}")

    # 3. Prepare features and target
    feature_cols = ['age', 'income', 'city', 'education', 'employment']
    cat_features = ['city', 'education', 'employment']
    
    X_train = train_df[feature_cols]
    y_train = train_df['target']
    X_test = test_df[feature_cols]
    y_test = test_df['target']

    # 4. Create Pool with categorical features
    print("🏊 Creating CatBoost Pool with categorical features...")
    train_pool = Pool(
        data=X_train,
        label=y_train,
        cat_features=cat_features
    )
    test_pool = Pool(
        data=X_test,
        label=y_test,
        cat_features=cat_features
    )
    print("✅ Pool objects created with categorical features")

    # 5. Train model
    print("🚀 Training CatBoost with categorical features...")
    model = CatBoostClassifier(
        iterations=100,
        learning_rate=0.1,
        depth=6,
        loss_function='Logloss',
        verbose=False,
        random_seed=42
    )
    model.fit(train_pool)
    print("✅ Model trained")

    # 6. Make predictions
    print("🔮 Making predictions...")
    y_pred = model.predict(test_pool)
    y_pred_proba = model.predict_proba(test_pool)[:, 1]
    print("✅ Predictions generated")

    # 7. Evaluate
    print("📈 Evaluating model...")
    from sklearn.metrics import accuracy_score, classification_report
    accuracy = accuracy_score(y_test, y_pred)
    print(f"✅ Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # 8. Feature importance
    print("🔍 Feature importance (including categorical):")
    feature_importance = model.get_feature_importance()
    importance_df = pd.DataFrame({
        'feature': feature_cols,
        'importance': feature_importance
    }).sort_values('importance', ascending=False)
    print(importance_df)

    # 9. Test with new categorical data
    print("🧪 Testing with new sample data...")
    new_sample = pd.DataFrame({
        'age': [45],
        'income': [75000],
        'city': ['Chicago'],
        'education': ['Master'],
        'employment': ['Full-time']
    })
    prediction = model.predict(new_sample)
    proba = model.predict_proba(new_sample)
    print(f"✅ New sample prediction: {prediction[0]}")
    print(f"   Probability: {proba[0]}")

    print("✅ CatBoost categorical features test passed successfully!")

if __name__ == "__main__":
    test_catboost_with_categorical_features()

# Made with Bob
