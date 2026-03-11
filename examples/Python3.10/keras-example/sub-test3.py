import numpy as np
import keras

print("===== SUBTEST 3: Save/Load Consistency =====")

model = keras.models.load_model("trained_model.h5")
sample = np.load("sample_input.npy")

pred1 = model.predict(sample)

model.save("reloaded_model.h5")
model2 = keras.models.load_model("reloaded_model.h5")

pred2 = model2.predict(sample)

diff = float(np.mean(np.abs(pred1 - pred2)))
print("Prediction difference:", diff)

assert diff < 1e-6, "Save/Load inconsistency detected"

print("Save/Load test passed.")
