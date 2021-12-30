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



def getPatterns( path, cv, sort):

  def norm1( data ):
      norms = np.abs( data.sum(axis=1) )
      norms[norms==0] = 1
      return data/norms[:,None]

  def reshape_to_vortex( input_data):
    print("Applying spiral ringer shape...")
   
    # NOTE: Do not change this if you dont know what are you doing
    frame =     [ [72,73,74,75,76,77,78,79,80,81],
                  [71,42,43,44,45,46,47,48,49,82],
                  [70,41,20,21,22,23,24,25,50,83],
                  [69,40,19,6 ,7 ,8 ,9 ,26,51,84],
                  [68,39,18,5 ,0 ,1 ,10,27,52,85],
                  [67,38,17,4 ,3 ,2 ,11,28,53,86],
                  [66,37,16,15,14,13,12,29,54,87],
                  [65,36,35,34,33,32,31,30,55,88],
                  [64,63,62,61,60,59,58,57,56,89],
                  [99,98,97,96,95,94,93,92,91,90],
                ]
    from copy import deepcopy
    zeros_to_complete = np.zeros((input_data.shape[0],100-input_data.shape[1]))
    data = deepcopy(np.hstack([input_data, zeros_to_complete]))
    d = deepcopy(data.reshape( 1,10,10,data.shape[0] ))
    data=data.T
    for i in range(10):
        for j in range(10):
            d[0][i][j][::] = data[ frame[i][j] ][::]
    d=d.T
    return d

  pidname = 'el_lhmedium'
  from kepler.pandas import load_hdf
  import numpy as np
  df = load_hdf(path)
  df = df.loc[ ((df[pidname]==True) & (df.target==1.0)) | ((df.target==0) & (df['el_lhvloose']==False) ) ]
  col_names= ['trig_L2_cl_ring_%d'%i for i in range(100)]
  rings = df[col_names].values.astype(np.float32)

  data = norm1(rings)
  data = reshape_to_vortex(data)

  print(data.shape)


  target = df['target'].values.astype(np.int16)

  splits = [(train_index, val_index) for train_index, val_index in cv.split(data,target)]
  x_train = data [ splits[sort][0]]
  y_train = target [ splits[sort][0] ]
  x_val = data [ splits[sort][1]]
  y_val = target [ splits[sort][1] ]

  return x_train, x_val, y_train, y_val, splits, []


def getPileup( path ):
  from Gaugi import load
  return load(path)['data'][:,0]


def getJobConfigId( path ):
  from Gaugi import load
  return dict(load(path))['id']


import argparse
import sys,os


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


if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()


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


  from saphyra.decorators import Summary, Reference
  decorators = [Summary(), Reference(args.refFile, targets)]

  from saphyra.callbacks import sp


  from saphyra import PatternGenerator
  from sklearn.model_selection import StratifiedKFold
  from saphyra.applications import BinaryClassificationJob


  job = BinaryClassificationJob(  PatternGenerator( args.dataFile, getPatterns ),
                                  StratifiedKFold(n_splits=10, random_state=512, shuffle=True),
                                  job               = args.configFile,
                                  loss              = 'binary_crossentropy',
                                  metrics           = ['accuracy'],
                                  callbacks         = [sp(patience=25, verbose=True, save_the_best=True)],
                                  epochs            = 5000,
                                  class_weight      = True,
                                  outputFile        = outputFile )

  job.decorators += decorators

  # Run it!
  job.run()


  # necessary to work on orchestra
  from saphyra import lock_as_completed_job
  lock_as_completed_job(args.volume if args.volume else '.')

  sys.exit(0)

except  Exception as e:
  print(e)

  # necessary to work on orchestra
  from saphyra import lock_as_failed_job
  lock_as_failed_job(args.volume if args.volume else '.')

  sys.exit(1)



