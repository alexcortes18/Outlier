# This code is for a task that i though would appeared next (code refactoring) but the one which appeared was
# bug fixing. So use this code later for another code refactoring task.

# Now i refactored it myself so i can ask for Code Generation task by myself.

import tensorflow as tf
from tensorflow.keras import layers
import helper_functions as hp
import matplotlib.pyplot as plt
import datetime

# Directorios
train_dir_10_percent = "../Datasets/10_food_classes_10_percent/train/"
test_dir = "../Datasets/10_food_classes_10_percent/test/"

# Constantes
IMG_SIZE = (224, 224)
INPUT_SHAPE = (224, 224, 3)

# Cargar datos
def load_data():
    # Cargar datos de entrenamiento y prueba
    train_data = tf.keras.preprocessing.image_dataset_from_directory(
        train_dir_10_percent,
        label_mode="categorical",
        image_size=IMG_SIZE
    )
    test_data = tf.keras.preprocessing.image_dataset_from_directory(
        test_dir,
        label_mode="categorical",
        image_size=IMG_SIZE
    )
    return train_data, test_data

# Aumento de datos
def create_data_augmentation():
    # Aplicar transformaciones aleatorias para aumentar los datos
    return tf.keras.Sequential([
        layers.RandomRotation(0.2),
        layers.RandomFlip("horizontal"),
        layers.RandomHeight(0.2),
        layers.RandomWidth(0.2),
        layers.RandomZoom(0.2),
    ], name="data_augmentation")

# Construir el modelo
def build_model(data_augmentation):
    # Construir el modelo con EfficientNetV2 como base
    base_model = tf.keras.applications.efficientnet_v2.EfficientNetV2B0(include_top=False)
    base_model.trainable = False

    inputs = tf.keras.Input(shape=INPUT_SHAPE, name="input_shape")
    x = data_augmentation(inputs)
    x = base_model(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D(name="global_average_pooling_2D")(x)
    outputs = tf.keras.layers.Dense(10, activation="softmax", name="output_layer")(x)

    model = tf.keras.Model(inputs, outputs)
    model.compile(
        loss="categorical_crossentropy",
        optimizer="Adam",
        metrics=["accuracy"]
    )
    return model

# Crear un callback usando Tensorflow Callback
def create_tensorboard_callback(dir_name, experiment_name):
  log_dir = dir_name + "/" + experiment_name + "/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  tensorboard_callback = tf.keras.callbacks.TensorBoard(
      log_dir=log_dir
  )
  print(f"Saving TensorBoard log files to: {log_dir}")
  return tensorboard_callback

# Entrenar el modelo
def train_model(model, train_data, test_data):
    # Definir el callback de checkpoint
    checkpoint_path = "ten_percent_model_checkpoints_weighs/checkpoint.weights.h5"
    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_path,
        save_weights_only=True,
        save_best_only=False,
        save_freq="epoch",
        verbose=1
    )

    # Entrenar el modelo y guardar el historial
    history = model.fit(
        train_data,
        epochs=5,
        steps_per_epoch=len(train_data),
        validation_data=test_data,
        validation_steps=int(0.25 * len(test_data)),
        callbacks=[create_tensorboard_callback(
                dir_name="transfer_learning",
                experiment_name="10_percent_data_aug"
            ),
            checkpoint_callback
        ]
    )
    return history, checkpoint_path

# Graficar los resultados
def plot_results(history):
    # Graficar las pérdidas y la precisión
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    accuracy = history.history['accuracy']
    val_accuracy = history.history['val_accuracy']
    epochs = range(len(history.history['loss']))

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

# Función principal
def main():
    # Cargar datos
    train_data, test_data = load_data()
    data_augmentation = create_data_augmentation()

    # Construir y compilar el modelo
    model = build_model(data_augmentation)
    
    model.summary()
    
    # Entrenar el modelo
    history, checkpoint_path = train_model(model, train_data, test_data)
    
    # Graficar los resultados
    plot_results(history)

    # Recargar pesos y evaluar
    model.load_weights(checkpoint_path)
    loaded_weights_model_results = model.evaluate(test_data)
    results_10_percent_data_aug = model.evaluate(test_data)
    
    # Verificar si los resultados son iguales
    print("Comparación de resultados:", results_10_percent_data_aug == loaded_weights_model_results)

if __name__ == "__main__":
    main()




# BEFORE REFACTORING:
# train_dir_10_percent = "../Datasets/10_food_classes_10_percent/train/"
# test_dir = "../Datasets/10_food_classes_10_percent/test/"

# import tensorflow as tf
# import helper_functions as hp

# IMG_SIZE = (224, 224)
# train_data_10_percent = tf.keras.preprocessing.image_dataset_from_directory(
#     train_dir_10_percent,
#     label_mode="categorical",
#     image_size=IMG_SIZE
# )
# test_data = tf.keras.preprocessing.image_dataset_from_directory(
#     test_dir,
#     label_mode="categorical",
#     image_size=IMG_SIZE
# )

# import tensorflow as tf
# from tensorflow.keras import layers

# data_augmentation = tf.keras.Sequential([
#     layers.RandomRotation(0.2),
#     layers.RandomFlip("horizontal"),
#     layers.RandomHeight(0.2),
#     layers.RandomWidth(0.2),
#     layers.RandomZoom(0.2),
# ], name="data_augmentation")

# input_shape = (224, 224, 3)

# base_model = tf.keras.applications.efficientnet_v2.EfficientNetV2B0(include_top=False)
# base_model.trainable = False

# inputs = tf.keras.Input(shape=input_shape, name="input_shape")
# x = data_augmentation(inputs)
# x = base_model(x, training=False)
# x = tf.keras.layers.GlobalAveragePooling2D(name="global_average_pooling_2D")(x)
# outputs = tf.keras.layers.Dense(10, activation="softmax", name="output_layer")(x)

# model_2 = tf.keras.Model(inputs, outputs)

# model_2.compile(
#     loss="categorical_crossentropy",
#     optimizer="Adam",
#     metrics=["accuracy"]
# )
# model_2.summary()

# checkpoint_path = "ten_percent_model_checkpoints_weighs/checkpoint.weights.h5"

# checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
#     filepath=checkpoint_path,
#     save_weights_only=True,
#     save_best_only=False,
#     save_freq="epoch",
#     verbose=1
# )

# history_2 = model_2.fit(
#     train_data_10_percent,
#     epochs=5,
#     steps_per_epoch=len(train_data_10_percent),
#     validation_data=test_data,
#     validation_steps=int(0.25 * len(test_data)),
#     callbacks=[
#         hp.create_tensorboard_callback(
#             dir_name="transfer_learning",
#             experiment_name="10_percent_data_aug"
#         ),
#         checkpoint_callback
#     ]
# )

# results_10_percent_data_aug = model_2.evaluate(test_data)

# loss = history_2.history['loss']
# val_loss = history_2.history['val_loss']
# accuracy = history_2.history['accuracy']
# val_accuracy = history_2.history['val_accuracy']
# epochs = range(len(history_2.history['loss']))

# import matplotlib.pyplot as plt

# plt.plot(epochs, loss, label='training_loss')
# plt.plot(epochs, val_loss, label='val_loss')
# plt.title('Loss')
# plt.xlabel('Epochs')
# plt.legend()

# plt.figure()
# plt.plot(epochs, accuracy, label='training_accuracy')
# plt.plot(epochs, val_accuracy, label='val_accuracy')
# plt.title('Accuracy')
# plt.xlabel('Epochs')
# plt.legend()

# model_2.load_weights(checkpoint_path)
# loaded_weights_model_results = model_2.evaluate(test_data)
# results_10_percent_data_aug == loaded_weights_model_results