


from saphyra import *
import tensorflow as tf
from tensorflow.keras import layers



def get_model( ):
  modelCol = []
  from tensorflow.keras.models import Sequential
  from tensorflow.keras.layers import Dense, Dropout, Activation, Conv1D, Flatten
  for n in range(5,5+1):
    print(n)
    model = Sequential()
    model.add(Dense(n, input_shape=(3,), activation='relu', name='dense_layer'))
    model.add(Dense(1, activation='linear', name='output_for_inference'))
    model.add(Activation('sigmoid', name='output_for_training'))
    modelCol.append(model)
  return modelCol



create_jobs( models = get_model(),
        nInits        = 5,
        nInitsPerJob  = 1,
        sortBounds    = 10,
        nSortsPerJob  = 1,
        nModelsPerJob = 1,
        outputFolder  = 'job_config.Zee_v1_el.10sorts.5inits' )

