

from neuralnet import *


def get_model( ):
  modelCol = []
  from tensorflow.keras.models import Sequential
  from tensorflow.keras.layers import Dense, Dropout, Activation, Conv1D, Flatten
  for n in [5]:
    model = Sequential()
    model.add(Dense(n, input_shape=(50,), activation='relu', name='dense_layer'))
    model.add(Dense(1, activation='linear', name='output_for_inference'))
    model.add(Activation('sigmoid', name='output_for_training'))
    modelCol.append(model)
  return modelCol



create_jobs( models = get_model(),
        nInits        = 2,
        sortBounds    = 10,
        outputFolder  = 'jobs' )


