import keras
print("===== SUBTEST 1: Architecture Validation =====")
model = keras.models.load_model("trained_model.h5")
layer_count = len(model.layers)
print("Layer count:", layer_count)
assert layer_count >= 6, "Model architecture too shallow"
