

from kepler import load, save_hdf
from pandarallel import pandarallel
pandarallel.initialize(progress_bar=False)

path='data17_13TeV.AllPeriods.sgn.probes_lhvloose_EGAM2.bkg.vprobes_vlhvloose_EGAM7.GRL_v97.15bins_et{ET}_eta{ETA}.npz'


def apply_cutbased(row,pid):
    if 0 <= row.trig_L2_cl_et/1000 < 12:
        #setattr(row, 'trig_L2_cl_%s'%pid, getattr(row, 'trig_L2_cl_%s_et0to12'%pid) )
        return getattr(row, 'trig_L2_cl_%s_et0to12'%pid) 
    elif 12 <= row.trig_L2_cl_et/1000 < 22:
        #setattr(row, 'trig_L2_cl_%s'%pid, getattr(row, 'trig_L2_cl_%s_et12to22'%pid) )
        return getattr(row, 'trig_L2_cl_%s_et12to22'%pid)
    else:
        #setattr(row, 'trig_L2_cl_%s'%pid, getattr(row, 'trig_L2_cl_%s_et22toInf'%pid) )
        return getattr(row, 'trig_L2_cl_%s_et22toInf'%pid) 

def apply_tight(row):
    return apply_cutbased(row, 'tight')
def apply_medium(row):
    return apply_cutbased(row, 'medium')
def apply_loose(row):
    return apply_cutbased(row, 'loose')
def apply_vloose(row):
    return apply_cutbased(row, 'vloose')



def apply_fast_track_cuts(row):
    
    if row.trig_L2_el_hastrack == False:
        return False
    
    
    if row.trig_L2_el_pt/1000 < 15:
        return row.trig_L2_el_cut_pt0to15
    if 15 <= row.trig_L2_el_pt/1000 < 20 :
        return row.trig_L2_el_cut_pt15to20
    if 20 <= row.trig_L2_el_pt/1000 < 50:
        return row.trig_L2_el_cut_pt20to50
    else: # 50 to inf
        return row.trig_L2_el_cut_pt50toInf
    



for et in range(3):

    for eta in range(5):

        d = path.format(ET=et, ETA=eta)
        dd = d.split('/')[-1].replace('npz','h5')
        df = load(d)
        

        # fix some columns
        for wp in ['tight', 'medium','loose','vloose']:
            df.rename({'trig_L2_cl_lh%s_et0to12'%wp    : 'trig_L2_cl_%s_et0to12'%wp}  , axis='columns' , inplace=True)
            df.rename({'trig_L2_cl_lh%s_et12to20'%wp   : 'trig_L2_cl_%s_et12to22'%wp} , axis='columns' , inplace=True)
            df.rename({'trig_L2_cl_lh%s_et22toInf'%wp  : 'trig_L2_cl_%s_et22toInf'%wp}, axis='columns' , inplace=True)


        # add new columns
        df['trig_L2_cl_tight']  = df.parallel_apply(apply_tight,axis=1)
        df['trig_L2_cl_medium'] = df.parallel_apply(apply_medium,axis=1)
        df['trig_L2_cl_loose']  = df.parallel_apply(apply_loose,axis=1)
        df['trig_L2_cl_vloose'] = df.parallel_apply(apply_vloose,axis=1)
        
        df['trig_L2_el_accept'] = df.parallel_apply(apply_fast_track_cuts, axis=1)
        #print(df.columns.values)
        
        #df.parallel_apply(apply_tight,axis=1)
        #df.parallel_apply(apply_medium,axis=1)
        #df.parallel_apply(apply_loose,axis=1)
        #df.parallel_apply(apply_vloose,axis=1)
            
        print(df['trig_L2_cl_tight'].unique())

        print(dd)
        save_hdf(df, dd)
        #print(tot)





