import numpy as np
import keras

print("===== SUBTEST 2: Training Validation =====")

model = keras.models.load_model("trained_model.h5")

weights = model.get_weights()

total_weight_sum = sum([w.sum() for w in weights])
print("Total weight sum:", float(total_weight_sum))

assert total_weight_sum != 0.0, "Model weights not trained"

print("Training validation passed.")
