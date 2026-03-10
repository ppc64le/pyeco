import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "1"          # INFO/WARN only
os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"  # Avoids full GPU memory grab
os.environ["TF_CPP_MIN_VLOG_LEVEL"] = "1"

import tensorflow as tf
import numpy as np

def print_section(title):
    print("\n" + "="*80)
    print(title)
    print("="*80)

def main():
    print_section("TensorFlow Version")
    print("tf version:", tf.__version__)
    print("Built with CUDA:", tf.test.is_built_with_cuda())
    print("XLA available:", tf.config.optimizer.get_jit())

    print_section("Devices")
    print("Physical devices:", tf.config.list_physical_devices())
    print("GPUs:", tf.config.list_physical_devices("GPU"))
    print("CPUs:", tf.config.list_physical_devices("CPU"))

    # Device placement logging
    tf.debugging.set_log_device_placement(True)

    print_section("Basic Tensor Ops and Device Placement")
    with tf.device("/GPU:0" if tf.config.list_physical_devices("GPU") else "/CPU:0"):
        a = tf.random.uniform((1024, 1024))
        b = tf.random.uniform((1024, 1024))
        c = tf.matmul(a, b)
        print("matmul result shape:", c.shape, "mean:", tf.reduce_mean(c).numpy())

    print_section("Small Keras Model Train")
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation="relu", input_shape=(32,)),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer="adam", loss="mse")
    x = np.random.rand(512, 32).astype("float32")
    y = np.random.rand(512, 1).astype("float32")
    hist = model.fit(x, y, epochs=3, batch_size=32, verbose=1)
    print("Final loss:", hist.history["loss"][-1])

    print_section("Save/Load Model Smoke Test")
    model.save("tf_test_model.keras")
    reloaded = tf.keras.models.load_model("tf_test_model.keras")
    print("Reloaded model predicts shape:", reloaded.predict(x[:5]).shape)

    print_section("SUCCESS")
    print("Diagnostics completed successfully.")

if __name__ == "__main__":
    main()