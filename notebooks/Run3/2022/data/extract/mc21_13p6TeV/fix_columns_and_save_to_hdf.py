

from kepler import load, save_hdf
from pandarallel import pandarallel
import glob
pandarallel.initialize(progress_bar=False)

path='mc21_13p6TeV.601189.PhPy8EG_AZNLO_Zee.Py8EG_A14NNPDF23LO_perf_JF17.25bins_et{ET}_eta{ETA}.npz'


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
    

paths = glob.glob('*.npz')
print(paths)

for d in paths:

        dd = d.split('/')[-1].replace('npz','h5')
        df = load(d)

        print('before')
        print(df.shape)
        df = df.loc[(df.trig_EF_el_hascand==True) & (df.trig_L2_el_hastrack==True) & 
                    (df.trig_EF_cl_hascluster==True) & (df.el_hastrack==True)]
        print('after')
        df.shape

        # fix some columns
        for wp in ['tight', 'medium','loose','vloose']:
            df.rename({'trig_L2_cl_lh%s_et0to12'%wp    : 'trig_L2_cl_%s_et0to12'%wp}  , axis='columns' , inplace=True)
            df.rename({'trig_L2_cl_lh%s_et12to22'%wp   : 'trig_L2_cl_%s_et12to22'%wp} , axis='columns' , inplace=True)
            df.rename({'trig_L2_cl_lh%s_et22toInf'%wp  : 'trig_L2_cl_%s_et22toInf'%wp}, axis='columns' , inplace=True)


        # add new columns
        df['trig_L2_cl_tight']  = df.parallel_apply(apply_tight,axis=1)
        df['trig_L2_cl_medium'] = df.parallel_apply(apply_medium,axis=1)
        df['trig_L2_cl_loose']  = df.parallel_apply(apply_loose,axis=1)
        df['trig_L2_cl_vloose'] = df.parallel_apply(apply_vloose,axis=1)
        df['trig_L2_el_accept'] = df.parallel_apply(apply_fast_track_cuts, axis=1)
 

   
        for wp in ['tight', 'medium','loose','vloose']:
            df.drop( columns=['trig_L2_cl_%s_et0to12'%wp],  inplace=True)

        df.drop(columns=['trig_L2_el_cut_pt0to15','trig_L2_el_cut_pt15to20', 'trig_L2_el_cut_pt20to50', 'trig_L2_el_cut_pt50toInf'], inplace=True)

        sig_size = df.loc[df.target==1].shape[0]
        bkg_size = df.loc[df.target==0].shape[0]


        print('Signal: %d, Background: %d'%(sig_size, bkg_size))

        save_hdf(df, dd)





