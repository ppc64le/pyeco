import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from scipy.stats import mode
import numpy as np
import pandas as pd
import psutil

# --- 1. Create synthetic classification data ---
X, y = make_classification(n_samples=300, n_features=10, n_classes=3, n_informative=5, random_state=42)
X = StandardScaler().fit_transform(X)  # Normalize using sklearn

# Convert to torch tensors
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train_t = torch.tensor(X_train, dtype=torch.float32)
y_train_t = torch.tensor(y_train, dtype=torch.long)
X_test_t = torch.tensor(X_test, dtype=torch.float32)
y_test_t = torch.tensor(y_test, dtype=torch.long)

# --- 2. Define PyTorch model ---
class SimpleNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(10, 64)
        self.fc2 = nn.Linear(64, 3)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        return self.fc2(x)

model = SimpleNN()
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# --- 3. Train model ---
for epoch in range(10):
    optimizer.zero_grad()
    outputs = model(X_train_t)
    loss = loss_fn(outputs, y_train_t)
    loss.backward()
    optimizer.step()

print(f"Final training loss: {loss.item():.4f}")

# --- 4. Evaluate accuracy manually ---
with torch.no_grad():
    logits = model(X_test_t)
    preds = torch.argmax(logits, dim=1).numpy()
    acc = np.mean(preds == y_test)
    print(f" Model accuracy: {acc:.2%}")

# --- 5. Scipy stats: Check mode of predictions ---
most_common_class = mode(preds, keepdims=True).mode[0]
print(f" Most common prediction class: {most_common_class}")

# --- 6. Pandas analysis ---
df = pd.DataFrame(X_test, columns=[f"f{i}" for i in range(X.shape[1])])
df['pred'] = preds
df['true'] = y_test
print("First few predictions:\n", df.head())

# --- 7. System resource usage ---
cpu = psutil.cpu_percent(interval=1)
mem = psutil.virtual_memory().percent
print(f" CPU Usage: {cpu}% | Memory Usage: {mem}%")

# --- 8. Torch version checks ---
print(f" PyTorch: {torch.__version__}")
