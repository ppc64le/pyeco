## ✅ Program : CatBoost Machine Learning Integration Test

### Purpose:
Tests the interoperability of CatBoost gradient boosting library with NumPy, Pandas, and Scikit-learn by running a complete machine learning pipeline including data generation, model training, prediction, and evaluation.

### Packages used:
catboost numpy pandas scikit-learn

### Functionality:
- Generates a synthetic classification dataset using scikit-learn.
- Converts data to pandas DataFrame for structured data handling.
- Splits data into training and test sets using scikit-learn.
- Creates CatBoost Pool objects for efficient data handling.
- Trains a CatBoost classifier with custom hyperparameters.
- Makes predictions on test data.
- Evaluates model performance using accuracy and AUC-ROC metrics.
- Analyzes and displays feature importance rankings.
- Confirms successful execution of all steps in a single integrated script.

### How to run the example :
```
chmod +x install_test_example.sh
./install_test_example.sh
```
### License: 
It's covered under Apache 2.0 licenses