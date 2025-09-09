import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler

# --- Scikit-learn: Generate and scale data ---
X, y = make_classification(n_samples=100, n_features=5, n_classes=2, random_state=42)
print("Scikit-learn generated data shape:", X.shape)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("Scaled features mean (approx 0):", X_scaled.mean(axis=0))

# --- PyTorch: Convert data to tensors ---
X_t = torch.tensor(X_scaled, dtype=torch.float32)
y_t = torch.tensor(y, dtype=torch.long)
print("Torch tensor shape:", X_t.shape)

# --- PyTorch: Define simple model ---
class SimpleNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(5, 2)

    def forward(self, x):
        return self.fc(x)

model = SimpleNN()

# --- PyTorch: Forward pass ---
with torch.no_grad():
    logits = model(X_t)
print("Model output shape:", logits.shape)
print("Model output (first 5 rows):", logits[:5])
