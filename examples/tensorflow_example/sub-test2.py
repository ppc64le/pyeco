import time
import tensorflow as tf

BATCH_SIZE = 256
FEATURES = 128
STEPS = 200

def make_dataset():
    ds = tf.data.Dataset.from_tensor_slices((
        tf.random.uniform([BATCH_SIZE * STEPS, FEATURES]),
        tf.random.uniform([BATCH_SIZE * STEPS, 1])
    ))
    ds = ds.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    return ds

def main():
    print("tf version:", tf.__version__)
    ds = make_dataset()

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(512, activation="relu", input_shape=(FEATURES,)),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer="adam", loss="mse")

    # Measure steps/sec
    start = time.time()
    hist = model.fit(ds, epochs=1, steps_per_epoch=STEPS, verbose=1)
    dur = time.time() - start
    steps_per_sec = STEPS / dur
    print(f"Throughput: {steps_per_sec:.2f} steps/sec (batch={BATCH_SIZE}, features={FEATURES})")
    print("Final loss:", hist.history["loss"][-1])

if __name__ == "__main__":
    main()