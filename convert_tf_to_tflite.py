import tensorflow as tf

model = tf.keras.models.load_model('./model/model.h5')

# Convert the model.
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the model.
with open('./model/model.tflite', 'wb') as f:
    f.write(tflite_model)