#!/usr/bin/env python


#
# Get shower shapes patterns from file
#
def getPatterns( path, cv, sort):

  pidname = 'el_lhmedium'
  from kepler.pandas import load_hdf
  import numpy as np
  df = load_hdf(path)
  df = df.loc[ ((df[pidname]==True) & (df.target==1.0)) | ((df.target==0) & (df['el_lhvloose']==False) ) ]

  target      = df['target'].values.astype(np.int16)


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

  print(data_eratio.shape)

  # This is mandatory
  splits = [(train_index, val_index) for train_index, val_index in cv.split(data_reta,target)]

  data_shower = np.concatenate( (data_reta,data_eratio,data_f1,data_f3,data_weta2, data_wstot), axis=1)

  # split for this sort
  x_train = [ data_shower[splits[sort][0]] ]
  x_val   = [ data_shower[splits[sort][1]] ]
  y_train = target [ splits[sort][0] ]
  y_val   = target [ splits[sort][1] ]

  avgmu = df.avgmu.values
  avgmu_train = avgmu[splits[sort][0]]
  avgmu_val = avgmu[splits[sort][1]]

  return x_train, x_val, y_train, y_val, avgmu_train, avgmu_val, splits


import argparse
import sys,os,traceback


parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()


parser.add_argument('-t','--tunedFile', action='store',
        dest='tunedFile', required = True,
            help = "The tuned file to be reprocess.")

parser.add_argument('-v','--volume', action='store',
        dest='volume', required = True, default = None,
            help = "The volume.")

parser.add_argument('-d','--dataFile', action='store',
        dest='dataFile', required = True, default = None,
            help = "The data file used to train the model.")

parser.add_argument('-r','--refFile', action='store',
        dest='refFile', required = True, default = None,
            help = "The reference file.")


if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()



try:


  targets = [
                # cutbased!
                ('tight' , 'trig_L2_cl_tight'       ),
                ('medium', 'trig_L2_cl_medium'      ),
                ('loose' , 'trig_L2_cl_loose'       ),
                ('vloose', 'trig_L2_cl_vloose'      ),
                ]


  
  from saphyra.decorators import Summary, Reference,LinearFit



  fit = LinearFit(args.refFile, targets, 
                  xbin_size=0.05, 
                  ybin_size=0.5, 
                  ymin=16, 
                  ymax=60,  
                  min_avgmu=16, 
                  max_avgmu=100, 
                  false_alarm_limit=0.5)



  decorators = [Summary(), Reference(args.refFile, targets), fit]
  
  from sklearn.model_selection import StratifiedKFold
  from saphyra.applications import BinaryClassificationJob
  
  cv = StratifiedKFold(n_splits=10, random_state=512, shuffle=True)
  
  from saphyra import PatternGenerator
  from saphyra.utils import reprocess
  
  reprocess( PatternGenerator( args.dataFile, getPatterns), args.tunedFile, args.volume, cv, decorators )


  # necessary to work on orchestra
  from saphyra import lock_as_completed_job
  lock_as_completed_job(args.volume if args.volume else '.')

  sys.exit(0)

except  Exception as e:
  print(e)
  traceback.print_exc()

  # necessary to work on orchestra
  from saphyra import lock_as_failed_job
  lock_as_failed_job(args.volume if args.volume else '.')

  sys.exit(1)





