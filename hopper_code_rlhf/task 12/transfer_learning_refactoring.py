import tensorflow as tf
import helper_functions as hp
train_dir = "../Datasets/10_food_classes_10_percent/train"
test_dir = "../Datasets/10_food_classes_10_percent/test"

IMG_SIZE = (224,224)
BATCH_SIZE = 32
train_data_10_percent = tf.keras.preprocessing.image_dataset_from_directory(directory= train_dir,
                                                                            image_size = IMG_SIZE,
                                                                            label_mode = "categorical",
                                                                            batch_size = BATCH_SIZE)
test_data = tf.keras.preprocessing.image_dataset_from_directory(directory= test_dir,
                                                                 image_size = IMG_SIZE,
                                                                 label_mode = "categorical",
                                                                 batch_size = BATCH_SIZE)

base_model = tf.keras.applications.efficientnet_v2.EfficientNetV2B0(include_top = False)
base_model.trainable = False

inputs = tf.keras.layers.Input(shape=(224,224,3), name = "input_layer")
x = base_model(inputs)
x = tf.keras.layers.GlobalAveragePooling2D(name = "global_average_pooling_layer")(x)
outputs = tf.keras.layers.Dense(10, activation="softmax", name="output_layer")(x)
model_0 = tf.keras.Model(inputs, outputs)

model_0.compile(loss = tf.keras.losses.CategoricalCrossentropy,
                optimizer = "Adam",
                metrics = ["accuracy"])

history_10_percent = model_0.fit(train_data_10_percent,
                                 epochs = 5,
                                 validation_data = test_data,
                                 validation_steps = int(0.25*len(test_data)),
                                 callbacks = [hp.create_tensorboard_callback(dir_name="transfer_learning",
                                                                             experiment_name= "10_percent_feature_extraction")])

model_0.evaluate(test_data)

for layer_number, layer in enumerate(base_model.layers):
    print(layer_number, layer.name)

import pandas as pd
pd.DataFrame(history_10_percent.history)

loss = history_10_percent.history['loss']
val_loss = history_10_percent.history['val_loss']
accuracy = history_10_percent.history['accuracy']
val_accuracy = history_10_percent.history['val_accuracy']
epochs = range(len(history_10_percent.history['loss']))

import matplotlib.pyplot as plt
plt.plot(epochs, loss, label='training_loss')
plt.plot(epochs, val_loss, label='val_loss')
plt.title('Loss')
plt.xlabel('Epochs')
plt.legend()

plt.figure()
plt.plot(epochs, accuracy, label='training_accuracy')
plt.plot(epochs, val_accuracy, label='val_accuracy')
plt.title('Accuracy')
plt.xlabel('Epochs')
plt.legend()