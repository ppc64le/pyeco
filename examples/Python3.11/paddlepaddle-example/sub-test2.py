import paddle
import paddle.nn as nn
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler

print("✅ Sub-test 2: PaddlePaddle model training")

# Generate and scale data
X, y = make_classification(n_samples=100, n_features=5, n_classes=2, random_state=42)
X = StandardScaler().fit_transform(X)

X_t = paddle.to_tensor(X, dtype='float32')
y_t = paddle.to_tensor(y, dtype='int64')

# Simple 2-layer model
class TinyNet(nn.Layer):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(5, 16)
        self.fc2 = nn.Linear(16, 2)
        self.relu = nn.ReLU()

    def forward(self, x):
        return self.fc2(self.relu(self.fc1(x)))

model     = TinyNet()
loss_fn   = nn.CrossEntropyLoss()
optimizer = paddle.optimizer.SGD(parameters=model.parameters(), learning_rate=0.05)

for epoch in range(5):
    model.train()
    logits = model(X_t)
    loss   = loss_fn(logits, y_t)
    loss.backward()
    optimizer.step()
    optimizer.clear_grad()

print(f"Training loss after 5 epochs: {loss.item():.4f}")

model.eval()
with paddle.no_grad():
    preds = paddle.argmax(model(X_t), axis=1).numpy()

import numpy as np
print(f"Training accuracy: {np.mean(preds == y):.2%}")
print("✅ Sub-test 2 completed successfully.")
