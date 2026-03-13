import lightgbm as lgb
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, log_loss
import matplotlib.pyplot as plt
import numpy as np

# Load dataset
iris = load_iris()
X = iris.data
y = iris.target
num_class = len(np.unique(y))

# For demo: treat features 0 and 1 as categorical (Iris features are continuous though)
categorical_features = [0, 1]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create dataset for LightGBM
train_data = lgb.Dataset(X_train, label=y_train, categorical_feature=categorical_features)
test_data = lgb.Dataset(X_test, label=y_test, reference=train_data, categorical_feature=categorical_features)

# Custom eval metric (multi-class log loss)
def custom_logloss(preds, dataset):
    labels = dataset.get_label()
    # Reshape preds to (num_samples, num_class)
    preds = preds.reshape(num_class, -1).T
    # Normalize rows to sum to 1 (to avoid numerical instability)
    preds = preds / preds.sum(axis=1, keepdims=True)
    loss = log_loss(labels, preds)
    return 'custom_logloss', loss, False

params = {
    'objective': 'multiclass',
    'num_class': num_class,
    'metric': 'multi_logloss',
    'learning_rate': 0.1,
    'num_leaves': 31,
    'verbose': -1
}

callbacks = [
    lgb.early_stopping(stopping_rounds=10),
    lgb.log_evaluation(period=10)
]

bst = lgb.train(
    params,
    train_data,
    num_boost_round=100,
    valid_sets=[test_data],
    feval=custom_logloss,
    callbacks=callbacks
)

# Predict class probabilities
y_pred_probs = bst.predict(X_test)
# Get predicted classes
y_pred = np.argmax(y_pred_probs, axis=1)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.4f}')

# Feature importance
lgb.plot_importance(bst, max_num_features=10)
plt.show()
