import numpy as np
import tensorflow as tf
import keras
from keras import layers
from scipy import signal

print("===== MAIN TEST: Training Pipeline =====")

def generate_data(samples=1500, length=128):
    X, y = [], []
    for _ in range(samples):
        freq = np.random.uniform(1, 10)
        t = np.linspace(0, 1, length)
        wave = np.sin(2*np.pi*freq*t)
        wave += np.random.normal(0, 0.1, length)

        b, a = signal.butter(3, 0.2)
        wave = signal.filtfilt(b, a, wave)

        X.append(wave)
        y.append(0 if freq < 5 else 1)

    return np.array(X)[..., np.newaxis], keras.utils.to_categorical(y, 2)

X, y = generate_data()

inputs = keras.Input(shape=(128,1))
x = layers.Conv1D(32,3,padding="same",activation="relu")(inputs)
x = layers.BatchNormalization()(x)
x = layers.Conv1D(32,3,padding="same",activation="relu")(x)
x = layers.GlobalAveragePooling1D()(x)
x = layers.Dense(64,activation="relu")(x)
outputs = layers.Dense(2,activation="softmax")(x)

model = keras.Model(inputs, outputs)

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

history = model.fit(X, y, epochs=5, batch_size=32)

model.save("trained_model.h5")
np.save("sample_input.npy", X[:20])

print("Main test completed successfully.")
