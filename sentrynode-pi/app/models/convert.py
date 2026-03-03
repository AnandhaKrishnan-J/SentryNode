import tensorflow as tf
from tensorflow.keras.models import load_model

# Step 1: Load the legacy .h5 model without compiling
model = load_model("autoencoder.h5", compile=False)

# Step 2: Re-compile with modern Keras objects
model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss=tf.keras.losses.MeanSquaredError(),
    metrics=[tf.keras.metrics.MeanSquaredError()]
)

# Step 3: Save in the recommended SavedModel format (directory-based)
model.export("autoencoder_saved")

print("Model successfully converted to SavedModel format.")

# Step 4: Reload