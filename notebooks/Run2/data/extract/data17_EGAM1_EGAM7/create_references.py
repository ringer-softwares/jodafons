#!/usr/bin/env python

import numpy as np
from kepler.pandas import load_hdf
from Gaugi import expand_folders
from saphyra import Reference_v1


path='/home/jodafons/public/cern_data/new_files/data17_13TeV.AllPeriods.sgn.probes_lhvloose_EGAM1.bkg.vprobes_vlhvloose_EGAM7.GRL_v97.25bins/data17_13TeV.AllPeriods.sgn.probes_lhvloose_EGAM1.bkg.vprobes_vlhvloose_EGAM7.GRL_v97.25bins_et{ET}_eta{ETA}.h5'

pidname = 'el_lhmedium'

# references used
ref_target = [
              ('tight' , 'trig_L2_cl_tight'        ),
              ('medium', 'trig_L2_cl_medium'       ),
              ('loose' , 'trig_L2_cl_loose'        ),
              ('vloose', 'trig_L2_cl_vloose'       ),
             ]

el_ref_target = [

             ('loosetrk', 'trig_L2_el_accept'      ),
            ]


for et_bin in range(5):

  for eta_bin in range(5):

    f = path.format(ET=et_bin, ETA=eta_bin)
    ff = f.split('/')[-1].replace('.h5','')+'.ref'

    ff = ff.replace('probes_lhvloose','probes_lhmedium')    
    obj = Reference_v1()
  
    df = load_hdf(f)
    df = df.loc[ ((df[pidname]==True) & (df.target==1.0)) | ((df.target!=1) & (df['el_lhvloose']==False) ) ]
  
    key = 'et%d_eta%d'%(et_bin,eta_bin)
    obj.setEtBins( [] )
    obj.setEtaBins( [] )
    obj.setEtBinIdx( et_bin )
    obj.setEtaBinIdx( eta_bin )
    
    ds_tot = df.loc[df.target==1].shape[0]
    db_tot = df.loc[df.target!=1].shape[0]

    for ref in ref_target:
      ds_passed = df.loc[(df.target==1) & (df[ref[1]]==True)].shape[0]
      db_passed = df.loc[(df.target!=1) & (df[ref[1]]==True)].shape[0]
      print( 'ref %s , pd = %1.2f, fa = %1.2f'%(ref[0], ds_passed/ds_tot * 100, db_passed/db_tot * 100))
      obj.addSgn( ref[0], ref[1], ds_passed, ds_tot )
      obj.addBkg( ref[0], ref[1], db_passed, db_tot )



    # fill fast electron eff
    df = df.loc[df.trig_L2_el_hastrack==True]

    for ref in el_ref_target:
      ds_passed = df.loc[(df.target==1) & (df[ref[1]]==True)].shape[0]
      db_passed = df.loc[(df.target!=1) & (df[ref[1]]==True)].shape[0]
      print( 'ref %s , pd = %1.2f, fa = %1.2f'%(ref[0], ds_passed/ds_tot * 100, db_passed/db_tot * 100))
      obj.addSgn( ref[0], ref[1], ds_passed, ds_tot )
      obj.addBkg( ref[0], ref[1], db_passed, db_tot )




    print(ff)
    obj.save(ff)



