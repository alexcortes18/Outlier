import pathlib, numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Activation
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import Sequential

train_dir = "../Datasets/10_food_classes_all_data/train"
test_dir = "../Datasets/10_food_classes_all_data/test"

data_dir = pathlib.Path(train_dir)
class_names_10 = np.array(sorted([item.name for item in data_dir.glob('*')]))

train_datagen = ImageDataGenerator(rescale=1/255.)
test_datagen = ImageDataGenerator(rescale=1/255.)

train_data = train_datagen.flow_from_directory(directory="../Datasets/10_food_classes_all_data/train/",
                                               target_size = (224,224),
                                               batch_size = 32,
                                               class_mode = "categorical",
                                               )
test_data = test_datagen.flow_from_directory(directory="../Datasets/10_food_classes_all_data/test/",
                                               target_size = (224,224),
                                               batch_size= 32,
                                               class_mode = "categorical",
                                               )
model_8 = Sequential([
    Conv2D(10,3,activation="relu", input_shape = (224,224,3)),
    Conv2D(10,3,activation="relu"),
    MaxPool2D(2),
    Conv2D(10,3,activation="relu"),
    Conv2D(10,3,activation="relu"),
    MaxPool2D(2),
    Flatten(),
    Dense(10, activation="softmax")
])
model_8.compile(loss = "categorical_crossentropy",
                optimizer = Adam(),
                metrics = ["accuracy"]
                )
history_8 = model_8.fit(train_data,
                        validation_data = test_data,
                        epochs = 5
                        )
model_8.evaluate(test_data)

train_datagen_augmented = ImageDataGenerator(rescale= 1/255.,
                                          rotation_range = 0.2,
                                          width_shift_range = 0.2,
                                          height_shift_range = 0.2,
                                          zoom_range = 0.2,
                                          horizontal_flip = True)
train_data_augmented = train_datagen_augmented.flow_from_directory(train_dir,
                                                                   target_size = (224,224),
                                                                   batch_size = 32,
                                                                   class_mode = 'categorical')
model_10 = tf.keras.models.clone_model(model_8)

model_10.compile(loss = "categorical_crossentropy",
                 optimizer = Adam(),
                 metrics = ["accuracy"])

history_10 = model_10.fit(train_data_augmented,
                          validation_data = test_data,
                          epochs = 5)
