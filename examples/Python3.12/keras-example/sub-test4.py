import numpy as np
import keras

print("===== SUBTEST 4: Inference Stability =====")

model = keras.models.load_model("trained_model.h5")
sample = np.load("sample_input.npy")

p1 = model.predict(sample)
p2 = model.predict(sample)

diff = float(np.mean(np.abs(p1 - p2)))
print("Inference difference:", diff)

assert diff < 1e-7, "Inference instability detected"

print("Inference stability test passed.")
