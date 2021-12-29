

# create the new model
from saphyra import *
import tensorflow as tf
from tensorflow.keras import layers



def create_model( c1, c2, d1, kernel_size=2, use_l2=False ):
    # expect an input with 100 domensions (features)
    input = layers.Input(shape=(100,), name = 'Input') # 0
    input_reshape = layers.Reshape((100,1), name='Reshape_layer')(input)
    conv = layers.Conv1D(c1, kernel_size = kernel_size, activation='relu', name = 'conv1d_layer_1')(input_reshape) # 1
    conv = layers.Conv1D(c2, kernel_size = kernel_size, activation='relu', name = 'conv1d_layer_2')(conv) # 2
    conv = layers.Flatten(name='flatten')(conv) # 3
    dense = layers.Dense(d1, activation='relu', name='dense_layer')(conv) # 4
    if use_l2:
        dense = layers.Dense(1,activation='linear', name='output_for_inference', kernel_regularizer='l2', bias_regularizer='l2')(dense) # 5
    else:
        dense = layers.Dense(1,activation='linear', name='output_for_inference')(dense) # 5
    output = layers.Activation('sigmoid', name='output_for_training')(dense) # 6
    model = tf.keras.Model(input, output, name = "model")
    return model




models = [
            create_model(4 ,8 ,16, 2, False),
         ]


create_jobs( models        = models,
             nInits        = 5,
             nInitsPerJob  = 1,
             sortBounds    = 10,
             nSortsPerJob  = 1,
             nModelsPerJob = 1,
             outputFolder  = 'job_config.Zee_v10.10sorts.5inits',
             )


