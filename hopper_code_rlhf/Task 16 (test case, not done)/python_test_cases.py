import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras import layers, preprocessing
from tensorflow.keras import mixed_precision
import subprocess
import numpy as np
from helper_functions import create_tensorboard_callback, plot_loss_curves, compare_historys

# Procesar Datos:
mixed_precision.set_global_policy("mixed_float16")
datasets_list = tfds.list_builders()
print("food101" in datasets_list)

(train_data, test_data), ds_info = tfds.load(name="food101",
                                            split=["train", "validation"],
                                            shuffle_files=True,
                                            as_supervised=True, 
                                            with_info=True)

class_names = ds_info.features["label"].names

def preprocess_img(image, label, img_shape=224):
    image = tf.image.resize(image, [img_shape, img_shape])
    return tf.cast(image, tf.float32), label

train_data = train_data.map(map_func=preprocess_img, num_parallel_calls=tf.data.AUTOTUNE)
train_data = train_data.shuffle(buffer_size=1000).batch(batch_size=32).prefetch(buffer_size=tf.data.AUTOTUNE)
test_data = test_data.map(map_func=preprocess_img, num_parallel_calls=tf.data.AUTOTUNE).batch(32).prefetch(buffer_size=tf.data.AUTOTUNE)

# Crear callback
checkpoint_path = "model/checkpoints/cp.weights.h5"
model_checkpoint = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
                                                      monitor="val_acc",
                                                      save_best_only=True,
                                                      save_weights_only=True,
                                                      verbose=0)

# Crear el modelo base
input_shape = (224, 224, 3)
base_model = tf.keras.applications.EfficientNetB0(include_top=False)
base_model.trainable = False

# Crear el modelo funcional
inputs = tf.keras.Input(shape=input_shape, name="input_shape")
x = base_model(inputs, training=False)
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.Dense(len(class_names))(x)
outputs = tf.keras.layers.Activation("softmax", dtype=tf.float32, name="softmax_float32")(x)
model = tf.keras.Model(inputs, outputs)

# Compilar el modelo
model.compile(loss="sparse_categorical_crossentropy",  
              optimizer=tf.keras.optimizers.Adam(),
              metrics=["accuracy"])

# Entrenar el modelo
history_101_extraction_model = model.fit(train_data,
                                         validation_data=test_data,
                                         epochs=3,
                                         steps_per_epoch=len(train_data),
                                         callbacks=[create_tensorboard_callback(dir_name="training_logs",
                                                                                  experiment_name="efficientnetb0_101_classes_all_data_feature_extraction"),
                                                    model_checkpoint])

# Evaluar el modelo
results_feature_extract_model = model.evaluate(test_data)

# Crear y compilar el modelo original
def create_model():
    input_shape = (224, 224, 3)
    base_model = tf.keras.applications.EfficientNetB0(include_top=False)
    base_model.trainable = False

    inputs = tf.keras.Input(shape=input_shape, name="input_layer")
    x = base_model(inputs, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D(name="pooling_layer")(x)
    x = tf.keras.layers.Dense(len(class_names))(x)
    outputs = tf.keras.layers.Activation("softmax", dtype=tf.float32, name="softmax_float32")(x)
    model = tf.keras.Model(inputs, outputs)
    return model

# Cargar el modelo con los pesos guardados
created_model = create_model()
created_model.compile(loss="sparse_categorical_crossentropy",
              optimizer=tf.keras.optimizers.Adam(),
              metrics=["accuracy"])
created_model.load_weights(checkpoint_path)

results_with_loaded_weigths = created_model.evaluate(test_data)

save_dir = "./models/milestone1/07_efficientnetb0_feature_extract_model_mixed_precision.keras"
created_model.save(save_dir)

# Cargar el modelo previamente guardado
loaded_saved_model = tf.keras.models.load_model(save_dir)
results_loaded_saved_model = loaded_saved_model.evaluate(test_data)

# Verificar si los resultados son iguales
np.isclose(results_feature_extract_model, results_loaded_saved_model).all()

# Configurar callbacks para "fine tuning"
early_stopping = tf.keras.callbacks.EarlyStopping(monitor="val_accuracy", patience=3)
checkpoint_path_fine_tune = "fine_tune_checkpoints/cp.keras"
model_checkpoint_fine_tune = tf.keras.callbacks.ModelCheckpoint(checkpoint_path_fine_tune,
                                                               save_best_only=True,
                                                               monitor="val_accuracy")
reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor="val_loss",  
                                                 factor=0.2,  
                                                 patience=2,
                                                 verbose=1,  
                                                 min_lr=1e-7)

# Compilar el modelo (fine tuning)
loaded_saved_model.compile(loss="sparse_categorical_crossentropy",
                           optimizer=tf.keras.optimizers.Adam(),
                           metrics=["accuracy"])

# Entrenar el modelo (fine tuning)
history_101_fine_tune = loaded_saved_model.fit(train_data,
                                               validation_data=test_data,
                                               epochs=100,
                                               steps_per_epoch=len(train_data),
                                               callbacks=[create_tensorboard_callback("training_logs", "efficientb0_101_classes_all_data_fine_tuning"),
                                                          model_checkpoint_fine_tune,
                                                          early_stopping,
                                                          reduce_lr])
