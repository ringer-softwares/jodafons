#!/usr/bin/env python





def getPatterns( path, cv, sort):

  pidname = 'el_lhmedium'
  from kepler.pandas import load_hdf
  import numpy as np
  df = load_hdf(path)
  df = df.loc[ ((df[pidname]==True) & (df.target==1.0)) | ((df.target==0) & (df['el_lhvloose']==False) ) ]

  # for new training, we selected 1/2 of rings in each layer
  # pre-sample - 8 rings
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


    
  def norm1( data ):
      norms = np.abs( data.sum(axis=1) )
      norms[norms==0] = 1
      return data/norms[:,None]
    
  target = df['target'].values.astype(np.int16)

  data = norm1(rings)
  splits = [(train_index, val_index) for train_index, val_index in cv.split(data,target)]
  x_train = data [ splits[sort][0]]
  y_train = target [ splits[sort][0] ]
  x_val = data [ splits[sort][1]]
  y_val = target [ splits[sort][1] ]

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





