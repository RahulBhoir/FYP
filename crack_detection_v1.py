# -*- coding: utf-8 -*-
"""crack_detection_v1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14W0IYCGYiWRHZ4ibWh2B9yHDb6PD8sZd
"""

import os
import zipfile
from google.colab import drive
drive.mount('/content/drive/')

test_data= zipfile.ZipFile('/content/drive/My Drive/Study/FYP/datasets/crack_test_data.zip','r')
test_data.extractall('/tmp/crack_test/')

validation_data = zipfile.ZipFile('/content/drive/My Drive/Study/FYP/datasets/crack_validation_data.zip','r')
validation_data.extractall('/tmp/')

# !pip install pyunpack
# !pip install patool
# from pyunpack import Archive
# Archive('/content/drive/My Drive/Study/FYP/datasets/crack.rar').extractall('/tmp')

train_crack_positive_path = '/tmp/crack_test/Positive/'

train_crack_negative_path = '/tmp/crack_test/Negative/'

validation_crack_positive_path = '/tmp/validation/positive/'

validation_crack_negative_path = '/tmp/validation/negative/'

train_crack_positive = os.listdir(train_crack_positive_path)
print(train_crack_positive[:10])

train_crack_negative = os.listdir(train_crack_negative_path)
print(train_crack_negative[:10])

validation_crack_positive = os.listdir(validation_crack_positive_path)

validation_crack_negative = os.listdir(validation_crack_negative_path)

print('total training crack positive images:', len(train_crack_positive))
print('total training crack negative images:', len(train_crack_negative))
print('total validation crack positive images:', len(validation_crack_positive))
print('total validation crack negative images:', len(validation_crack_negative))

import tensorflow as tf

model = tf.keras.models.Sequential([tf.keras.layers.Conv2D(16,(3,3),activation='relu',input_shape=(227,227,3)),
                                    tf.keras.layers.MaxPooling2D(2,2),

                                    tf.keras.layers.Conv2D(32,(3,3),activation='relu'),
                                    tf.keras.layers.MaxPooling2D(2,2),
                                    
                                    tf.keras.layers.Conv2D(64,(3,3),activation='relu'),
                                    tf.keras.layers.MaxPooling2D(2,2),
                                    
                                    tf.keras.layers.Conv2D(64,(3,3),activation='relu'),
                                    tf.keras.layers.MaxPooling2D(2,2),

                                    tf.keras.layers.Flatten(),
                                    tf.keras.layers.Dense(128,activation='relu'),
                                    tf.keras.layers.Dense(1,activation='sigmoid')
                                    ])

model.summary()

from keras.utils.np_utils import to_categorical
label = to_categorical(label)

model = tf.keras.models.Sequential([tf.keras.layers.Conv2D(16, (3,3), activation='relu', input_shape=(256,256,3)),
                                    tf.keras.layers.MaxPooling2D(2,2),

                                    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
                                    tf.keras.layers.MaxPooling2D(2,2),

                                    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
                                    tf.keras.layers.MaxPooling2D(2,2),

                                    tf.keras.layers.Flatten(),
                                    tf.keras.layers.Dense(128,activation='relu'),
                                    tf.keras.layers.Dense(1,activation='sigmoid')])

model.summary()

from tensorflow.keras.optimizers import RMSprop
model.compile(loss='binary_crossentropy',
              optimizer=RMSprop(lr=0.001),
              metrics=['accuracy'])

from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale=1/255)
validation_datagen = ImageDataGenerator(rescale=1/255)

train_generator = train_datagen.flow_from_directory(
    '/tmp/crack_test/',
    target_size= (227,227),
    batch_size=128,
    class_mode='binary')

validation_generator = validation_datagen.flow_from_directory(
    '/tmp/validation/',
    target_size=(227,227),
    batch_size=128,
    class_mode='binary')

# on 20 epoch 16 img out of 20 were correctly classified
# on 30 epoch 11 img out of 20 were correctly classified 
history = model.fit(
    train_generator,
    steps_per_epoch=13,
    epoch=20,
    verbose=1,
    validation_data=validation_generator,
    validation_steps=13
)

import numpy as np
from google.colab import files
from keras.preprocessing import image
count = 0
uploaded = files.upload()

for file in uploaded.keys():
  path = '/content/' + file
  img = image.load_img(path,target_size=(227,227))
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)

  images = np.vstack([x])
  classes = model.predict(images,batch_size=10)
  print(classes[0])
  if classes[0]>0.5:
    print(file +' has crack')
    count+=1
  else:
    print(fn+' has no crack')
print(count)