import tensorflow as tf

def main():
    print("TensorFlow version:", tf.__version__)
    
    # Check GPU availability
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print("GPU is available:")
        for gpu in gpus:
            print("  -", gpu)
    else:
        print("No GPU detected — running on CPU.")

    # Simple tensor operation
    print("\nTesting basic tensor operation:")
    a = tf.constant([[1, 2], [3, 4]])
    b = tf.constant([[5, 6], [7, 8]])
    c = tf.matmul(a, b)
    print("Result of matrix multiplication:\n", c.numpy())

    # Tiny model test
    print("\nTesting a simple neural network training step:")
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(4, activation='relu', input_shape=(4,)),
        tf.keras.layers.Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')

    import numpy as np
    x = np.random.rand(10, 4)
    y = np.random.rand(10, 1)

    history = model.fit(x, y, epochs=3, verbose=1)

    print("\nModel test completed successfully.")

if __name__ == "__main__":
    main()