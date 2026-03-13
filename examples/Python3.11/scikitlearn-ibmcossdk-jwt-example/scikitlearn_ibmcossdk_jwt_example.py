import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import msgpack
import psutil
from PIL import Image, ImageDraw

# Generate synthetic data
np.random.seed(42)
X = np.random.rand(100, 1) * 10  # Feature
y = 2.5 * X.squeeze() + np.random.randn(100) * 2  # Target

# Create DataFrame
df = pd.DataFrame({'Feature': X.squeeze(), 'Target': y})

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(df[['Feature']], df['Target'], test_size=0.2)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict and evaluate
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)

# Serialize model coefficients using msgpack
packed = msgpack.packb({'coef': model.coef_.tolist(), 'intercept': model.intercept_})
unpacked = msgpack.unpackb(packed)

# System info using psutil
cpu_percent = psutil.cpu_percent(interval=1)
mem_info = psutil.virtual_memory()

# Create a simple image with Pillow
img = Image.new('RGB', (300, 100), color='white')
draw = ImageDraw.Draw(img)
draw.text((10, 10), f"MSE: {mse:.2f}", fill='black')
draw.text((10, 40), f"CPU: {cpu_percent}%", fill='black')
draw.text((10, 70), f"Mem: {mem_info.percent}%", fill='black')
img.show()

# Output unpacked model info
print("Model Coefficients:", unpacked)
