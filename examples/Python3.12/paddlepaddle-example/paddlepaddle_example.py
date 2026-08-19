import paddle
import paddle.nn as nn
import numpy as np
import pandas as pd
import psutil
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from scipy.stats import mode

# --- 1. Create synthetic classification data ---
X, y = make_classification(n_samples=300, n_features=10, n_classes=3,
                           n_informative=5, random_state=42)
X = StandardScaler().fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train_t = paddle.to_tensor(X_train, dtype='float32')
y_train_t = paddle.to_tensor(y_train, dtype='int64')
X_test_t  = paddle.to_tensor(X_test,  dtype='float32')

# --- 2. Define PaddlePaddle model ---
class SimpleNet(nn.Layer):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(10, 64)
        self.fc2 = nn.Linear(64, 3)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        return self.fc2(x)

model = SimpleNet()
loss_fn   = nn.CrossEntropyLoss()
optimizer = paddle.optimizer.Adam(parameters=model.parameters(), learning_rate=0.01)

# --- 3. Train model ---
for epoch in range(10):
    model.train()
    logits = model(X_train_t)
    loss   = loss_fn(logits, y_train_t)
    loss.backward()
    optimizer.step()
    optimizer.clear_grad()

print(f"Final training loss: {loss.item():.4f}")

# --- 4. Evaluate accuracy ---
model.eval()
with paddle.no_grad():
    logits = model(X_test_t)
    preds  = paddle.argmax(logits, axis=1).numpy()
    acc    = np.mean(preds == y_test)
    print(f"Model accuracy: {acc:.2%}")

# --- 5. SciPy: mode of predictions ---
most_common_class = mode(preds, keepdims=True).mode[0]
print(f"Most common prediction class: {most_common_class}")

# --- 6. Pandas analysis ---
df = pd.DataFrame(X_test, columns=[f"f{i}" for i in range(X_test.shape[1])])
df['pred'] = preds
df['true'] = y_test
print("First few predictions:\n", df.head())

# --- 7. System resource usage ---
cpu = psutil.cpu_percent(interval=1)
mem = psutil.virtual_memory().percent
print(f"CPU Usage: {cpu}% | Memory Usage: {mem}%")

# --- 8. PaddlePaddle version ---
print(f"PaddlePaddle version: {paddle.__version__}")
