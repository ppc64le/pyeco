import numpy as np
import pandas as pd
import xgboost as xgb
from scipy.stats import mode

print("✅ Sub-test 1: Numeric + XGBoost + SciPy")

# Generate numeric data
X = np.random.rand(40, 4)
y = np.random.randint(0, 2, size=40)
df = pd.DataFrame(X, columns=[f"f{i}" for i in range(X.shape[1])])
df['target'] = y

# Train XGBoost
dtrain = xgb.DMatrix(X, label=y)
params = {"objective": "binary:logistic", "eval_metric": "logloss"}
model = xgb.train(params, dtrain, num_boost_round=3)

# Make predictions and compute mode
preds = model.predict(dtrain)
most_common = mode(np.round(preds), keepdims=True).mode.item()
