#!/usr/bin/env python

try:
  from tensorflow.compat.v1 import ConfigProto
  from tensorflow.compat.v1 import InteractiveSession
  config = ConfigProto()
  config.gpu_options.allow_growth = True
  session = InteractiveSession(config=config)
except Exception as e:
  print(e)
  print("Not possible to set gpu allow growth")


from Gaugi import load
from Gaugi.macros import *
from saphyra.utils import model_generator_base
import numpy as np
import argparse
import sys,os
import traceback

parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()


parser.add_argument('-c','--configFile', action='store',
        dest='configFile', required = True,
            help = "The job config file that will be used to configure the job (sort and init).")

parser.add_argument('-v','--volume', action='store',
        dest='volume', required = False, default = None,
            help = "The volume output.")

parser.add_argument('-d','--dataFile', action='store',
        dest='dataFile', required = True, default = None,
            help = "The data/target file used to train the model.")

parser.add_argument('-r','--refFile', action='store',
        dest='refFile', required = True, default = None,
            help = "The reference file.")


parser.add_argument('--pr', action='store',
        dest='path_to_rings', required = False, default = None,
            help = "The path to the ringer tuned files.")

parser.add_argument('--ps', action='store',
        dest='path_to_shower', required = False, default = None,
            help = "The path to the shower tuned files.")


if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)


args = parser.parse_args()



#
# Model generator
#
class Model( model_generator_base ):

  def __init__( self, rings_path, shower_path ):

    model_generator_base.__init__(self)
    import tensorflow as tf
    from tensorflow.keras import layers
    
    # rings
    input_rings = layers.Input(shape=(50,), name='Input_rings')
    dense_rings = layers.Dense(5, activation='relu', name='dense_rings_layer')(input_rings)

    # shower shapes
    input_shower_shapes = layers.Input(shape=(6,), name='Input_shower_shapes')
    dense_shower_shapes = layers.Dense(5, activation='relu', name='dense_shower_layer')(input_shower_shapes)
    
    
    # decision layer
    #input_concat = layers.Concatenate(axis=1)([dense_from_conv, dense_shower_shapes])
    input_concat = layers.Concatenate(axis=1)([dense_rings, dense_shower_shapes])

    dense = layers.Dense(5, activation='relu', name='dense_layer')(input_concat)
    dense = layers.Dense(1,activation='linear', name='output_for_inference')(dense)
    #dense = layers.Dense(1,activation='linear', name='output_for_inference', kernel_regularizer='l2', bias_regularizer='l2')(dense)
    output = layers.Activation('sigmoid', name='output_for_training')(dense)

    # Build the model
    self.__model = tf.keras.Model([input_rings, input_shower_shapes], output, name = "model")
    self.__tuned_rings_models = self.load_models(rings_path)
    self.__tuned_shower_models = self.load_models(shower_path)

 
    # Follow the strategy proposed by werner were we keep these weights free to do the fine tunings
    # since most part of these variables have an stronge relationship (correlation).
    self.__trainable=True


  def __call__( self, sort ):

    from tensorflow.keras.models import clone_model
    # create a new model
    model = clone_model( self.__model )
    MSG_INFO(self, "Target model:" )
    model.summary()
    
    rings_model = self.get_best_model( self.__tuned_rings_models, sort , 3) # five neurons in the hidden layer
    MSG_INFO( self, "rings model (right):")
    rings_model.summary()
    
    shower_model = self.get_best_model( self.__tuned_shower_models, sort , 0) # five neurons in the hidden layer
    MSG_INFO( self, "shower model (left):")
    shower_model.summary()

    self.transfer_weights( rings_model  , 'dense_layer'    , model, 'dense_rings_layer'   , trainable=self.__trainable)
    self.transfer_weights( shower_model , 'dense_layer'    , model, 'dense_shower_layer'  , trainable=self.__trainable)

    return model

#
# Get shower shapes patterns from file
#
def getPatterns( path, cv, sort):

  pidname = 'el_lhmedium'
  from kepler.pandas import load_hdf
  import numpy as np
  df = load_hdf(path)
  df = df.loc[ ((df[pidname]==True) & (df.target==1.0)) | ((df.target==0) & (df['el_lhvloose']==False) ) ]



  def norm1( data ):
      norms = np.abs( data.sum(axis=1) )
      norms[norms==0] = 1
      return data/norms[:,None]



  # for new training, we selected 1/2 of rings in each layer
  #pre-sample - 8 rings
  # EM1 - 64 rings
  # EM2 - 8 rings
  # EM3 - 8 rings
  # Had1 - 4 rings
  # Had2 - 4 rings
  # Had3 - 4 rings
  prefix = 'trig_L2_cl_ring_%i'

  # rings presmaple 
  presample = [prefix %iring for iring in range(8//2)]

  # EM1 list
  sum_rings = 8
  em1 = [prefix %iring for iring in range(sum_rings, sum_rings+(64//2))]

  # EM2 list
  sum_rings = 8+64
  em2 = [prefix %iring for iring in range(sum_rings, sum_rings+(8//2))]

  # EM3 list
  sum_rings = 8+64+8
  em3 = [prefix %iring for iring in range(sum_rings, sum_rings+(8//2))]

  # HAD1 list
  sum_rings = 8+64+8+8
  had1 = [prefix %iring for iring in range(sum_rings, sum_rings+(4//2))]

  # HAD2 list
  sum_rings = 8+64+8+8+4
  had2 = [prefix %iring for iring in range(sum_rings, sum_rings+(4//2))]

  # HAD3 list
  sum_rings = 8+64+8+8+4+4
  had3 = [prefix %iring for iring in range(sum_rings, sum_rings+(4//2))]

  col_names = presample+em1+em2+em3+had1+had2+had3
  print(col_names)
  rings = df[col_names].values.astype(np.float32)
  data_rings = norm1(rings)


  target = df['target'].values.astype(np.int16)


  n = target.shape[0]
  data_reta   = df['trig_L2_cl_reta'].astype(np.float32).to_numpy().reshape((n,1))  / 1.
  data_eratio = df['trig_L2_cl_eratio'].astype(np.float32).to_numpy().reshape((n,1))  / 1.
  data_f1     = df['trig_L2_cl_f1'].astype(np.float32).to_numpy().reshape((n,1))  / 0.6
  data_f3     = df['trig_L2_cl_f3'].astype(np.float32).to_numpy().reshape((n,1))  / 0.04
  data_weta2  = df['trig_L2_cl_weta2'].astype(np.float32).to_numpy().reshape((n,1))  / 0.02
  data_wstot  = df['trig_L2_cl_wstot'].astype(np.float32).to_numpy().reshape((n,1))  / 1.

 
  # Fix all shower shapes variables
  data_eratio[data_eratio>10.0]=0
  data_eratio[data_eratio>1.]=1.0
  data_wstot[data_wstot<-99]=0

  # This is mandatory
  splits = [(train_index, val_index) for train_index, val_index in cv.split(data_reta,target)]

  data_shower = np.concatenate( (data_reta,data_eratio,data_f1,data_f3,data_weta2, data_wstot), axis=1)

  # split for this sort
  x_train = [ data_rings[splits[sort][0]], data_shower[splits[sort][0]] ]
  x_val   = [ data_rings[splits[sort][1]], data_shower[splits[sort][1]] ]
  y_train = target [ splits[sort][0] ]
  y_val   = target [ splits[sort][1] ]

  avgmu = df.avgmu.values
  avgmu_train = avgmu[splits[sort][0]]
  avgmu_val = avgmu[splits[sort][1]]

  return x_train, x_val, y_train, y_val, avgmu_train, avgmu_val, splits



#
# Get configuration file
#
def getJobConfigId( path ):
  return dict(load(path))['id']




try:


  
  job_id = getJobConfigId( args.configFile )

  outputFile = args.volume+'/tunedDiscr.jobID_%s'%str(job_id).zfill(4) if args.volume else 'test.jobId_%s'%str(job_id).zfill(4)

  targets = [
                # cutbased!
                ('tight' , 'trig_L2_cl_tight'       ),
                ('medium', 'trig_L2_cl_medium'      ),
                ('loose' , 'trig_L2_cl_loose'       ),
                ('vloose', 'trig_L2_cl_vloose'      ),
                ]



  from saphyra.callbacks import sp
  from saphyra import PatternGenerator
  from sklearn.model_selection import StratifiedKFold
  from saphyra.applications import BinaryClassificationJob
  from saphyra.decorators import Summary, Reference




  # create decorators
  decorators = [Summary(), Reference(args.refFile, targets)]
  model = Model( args.path_to_rings, args.path_to_shower )
  #
  # Create the binary job
  #
  job = BinaryClassificationJob(  PatternGenerator( args.dataFile, getPatterns ),
                                  StratifiedKFold(n_splits=10, random_state=512, shuffle=True),
                                  job               = args.configFile,
                                  loss              = 'binary_crossentropy',
                                  metrics           = ['accuracy'],
                                  callbacks         = [sp(patience=25, verbose=True, save_the_best=True)],
                                  epochs            = 5000,
                                  class_weight      = True,
                                  model_generator   = model, # Force to work with model generator (Hack)
                                  models            = [None], # Force to work with model generator (Hack)
                                  outputFile        = outputFile )

  job.decorators += decorators


  #
  # Run it!
  #
  job.run()


  # necessary to work on orchestra
  from saphyra import lock_as_completed_job
  lock_as_completed_job(args.volume if args.volume else '.')
  sys.exit(0)



except Exception as e:
  traceback.print_exc()
  print(e)
  # necessary to work on orchestra
  from saphyra import lock_as_failed_job
  lock_as_failed_job(args.volume if args.volume else '.')
  sys.exit(1)



