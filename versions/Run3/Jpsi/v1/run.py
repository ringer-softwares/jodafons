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


#
from neuralnet.decorators import Summary, Reference
from neuralnet.callbacks import sp, wandb_app
from neuralnet import PatternGenerator
from sklearn.model_selection import StratifiedKFold
from neuralnet.apps import BinaryClassificationJob

import traceback
import argparse
import sys,os


def getPatterns( path, cv, sort):

  from kepler.pandas import load_hdf
  import numpy as np
  df = load_hdf(path)

  df = df.loc[ ((df['el_lhmedium']==True) & (df.target==1)) | ((df.target==0) & (df['el_lhvloose']==False) ) ]

  col_names =  ['trig_L2_cl_ring_%i'%r for r in range(100)] 
  rings = df[col_names].values.astype(np.float32)

  def norm1( data ):
    norms = np.abs( data.sum(axis=1) )
    norms[norms==0] = 1
    return data/norms[:,None]

  data = norm1(rings)
  target = df['target'].values.astype(np.int16)
  target[target!=1]=0
  avgmu = df.avgmu.values

  del df

  splits = [(train_index, val_index) for train_index, val_index in cv.split(data,target)]
  x_train = data [ splits[sort][0]]
  y_train = target [ splits[sort][0] ]
  x_val = data [ splits[sort][1]]
  y_val = target [ splits[sort][1] ]

  avgmu_train = avgmu[splits[sort][0]]
  avgmu_val = avgmu[splits[sort][1]]

  return x_train, x_val, y_train, y_val, avgmu_train, avgmu_val, splits




parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()


parser.add_argument('-c','--configFile', action='store',
    dest='configFile', required = True,
    help = "The job config file that will be used to configure the job (sort and init).")

parser.add_argument('-v','--volume', action='store', 
    dest='volume', required = False, default=os.getcwd(),
    help = "volume path")

parser.add_argument('-d','--dataFile', action='store',
    dest='dataFile', required = True, default = None,
    help = "The data/target file used to train the model.")

parser.add_argument('-r','--refFile', action='store',
    dest='refFile', required = True, default = None,
    help = "The reference file.")


parser.add_argument('--use_wandb', action='store_true',
    dest='use_wandb', 
    help = "Use wandb.")
parser.add_argument('--wandb_username', action='store',
    dest='wandb_username', 
    help = "Wandb username.")
parser.add_argument('--wandb_taskname', action='store',
    dest='wandb_taskname', 
    help = "Wandb taskname.")   

if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()

# NOTE: for orchestra 
is_test = True if 'LOCAL_TEST' in os.environ.keys() else False


try:

  outputFile = args.volume+'/tunedDiscr'


  targets = [
                # cutbased!
                ('tight' , 'trig_L2_cl_tight'       ),
                ('medium', 'trig_L2_cl_medium'      ),
                ('loose' , 'trig_L2_cl_loose'       ),
                ('vloose', 'trig_L2_cl_vloose'      ),
                ]

  decorators = [Summary(), Reference(args.refFile, targets)]


  callbacks = [sp(patience=25, verbose=True, save_the_best=True)]

  if not is_test and args.use_wandb:
    app = wandb_app( args.wandb_username, args.wandb_taskname )
    jobname = args.volume.split('/')[-1].replace('.npz','')
    app.init(jobname)
    callbacks.append(app)


  job = BinaryClassificationJob(  PatternGenerator( args.dataFile, getPatterns ),
                                  StratifiedKFold(n_splits=10, random_state=512, shuffle=True),
                                  job               = args.configFile,
                                  loss              = 'binary_crossentropy',
                                  metrics           = ['accuracy'],
                                  callbacks         = callbacks,
                                  epochs            = 1 if is_test else 5000,
                                  class_weight      = True,
                                  outputFile        = outputFile )

  job.decorators += decorators

  # Run it!
  job.run()

  sys.exit(0)

except Exception as e:
  traceback.print_exc()
  print(e)
  sys.exit(1)



