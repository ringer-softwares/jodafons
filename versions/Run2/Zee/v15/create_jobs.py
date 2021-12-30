

# create the new model
from saphyra import *
import tensorflow as tf
from tensorflow.keras import layers



def create_model( c1, c2, d1, kernel_size=(3,3) ):
    # expect an input with 100 domensions (features)
    input = layers.Input(shape=(10,10,1), name = 'Input') # 0
    conv = layers.Conv2D(c1, kernel_size = kernel_size, activation='relu', name = 'conv2d_layer_1')(input) # 1
    conv = layers.Conv2D(c2, kernel_size = kernel_size, activation='relu', name = 'conv2d_layer_2')(conv) # 2
    conv = layers.Flatten(name='flatten')(conv) # 3
    dense = layers.Dense(d1, activation='relu', name='dense_layer')(conv) # 4
    dense = layers.Dense(1,activation='linear', name='output_for_inference')(dense) # 5
    output = layers.Activation('sigmoid', name='output_for_training')(dense) # 6
    model = tf.keras.Model(input, output, name = "model")
    return model




models = [
            create_model(4 ,8 ,16, (3,3)),
         ]


create_jobs( models        = models,
             nInits        = 5,
             nInitsPerJob  = 1,
             sortBounds    = 10,
             nSortsPerJob  = 1,
             nModelsPerJob = 1,
             outputFolder  = 'job_config.Zee_v15.10sorts.5inits',
             )


