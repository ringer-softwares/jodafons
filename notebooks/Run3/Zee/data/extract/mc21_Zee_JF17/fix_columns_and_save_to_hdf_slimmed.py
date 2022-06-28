

from kepler import load, save_hdf
from pandarallel import pandarallel
pandarallel.initialize(progress_bar=False)

path='mc21_13p6TeV.801272.P8B_A14_CTEQ6L1_Zee.Py8EG_A14NNPDF23LO_perf_JF17.25bins_et{ET}_eta{ETA}.npz'


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

col_names = ['avgmu']
col_names += presample+em1+em2+em3+had1+had2+had3
col_names += ['trig_L2_cl_et', 'trig_L2_cl_eta','mc_isTruthElectronFromZ', 'mc_isTruthElectronAny','mc_isTruthElectronFromJpsi', 'target']

print(col_names)
#colnames = [
#       'trig_L2_el_hastrack', 
#       'trig_L2_el_pt',
#       'trig_L2_el_eta', 
#       'trig_L2_el_phi', 
#       'trig_L2_el_caloEta',
#       'trig_L2_el_trkClusDeta', 
#       'trig_L2_el_trkClusDphi',
#       'trig_L2_el_etOverPt', 
#       'trig_L2_el_d0', 
#       'trig_EF_cl_hascluster',
#       'trig_EF_cl_et', 
#       'trig_EF_cl_eta', 
#       'trig_EF_cl_etaBE2',
#       'trig_EF_cl_phi', 
#       'trig_EF_el_hascand', 
#       'trig_EF_el_et',
#       'trig_EF_el_eta', 
#       'trig_EF_el_etaBE2', 
#       'trig_EF_el_phi',
#       'trig_EF_el_rhad1', 
#       'trig_EF_el_rhad', 
#       'trig_EF_el_f3',
#       'trig_EF_el_weta2', 
#       'trig_EF_el_rphi', 
#       'trig_EF_el_reta',
#       'trig_EF_el_wtots1', 
#       'trig_EF_el_eratio', 
#       'trig_EF_el_f1',
#       'trig_EF_el_hastrack',
#       'trig_EF_el_deltaEta1',
#       'trig_EF_el_deltaPhi2', 
#       'trig_EF_el_deltaPhi2Rescaled',
#       'trig_EF_el_lhtight', 
#       'trig_EF_el_lhmedium', 
#       'trig_EF_el_lhloose',
#       'trig_EF_el_lhvloose', 
#       'el_et', 
#       'el_eta', 
#       'el_etaBE2', 
#       'el_phi',
#       'el_rhad1', 
#       'el_rhad', 
#       'el_f3', 
#       'el_weta2', 
#       'el_rphi', 
#       'el_reta',
#       'el_wtots1', 
#       'el_eratio', 
#       'el_f1', 
#       'el_hastrack',
#       'el_numberOfBLayerHits', 
#       'el_numberOfPixelHits',
#       'el_numberOfTRTHits', 
#       'el_d0', 
#       'el_d0significance',
#       'el_eProbabilityHT', 
#       'el_trans_TRT_PID', 
#       'el_deltaEta1',
#       'el_deltaPhi2', 
#       'el_deltaPhi2Rescaled', 
#       'el_deltaPOverP',
#       'el_lhtight', 
#       'el_lhmedium', 
#       'el_lhloose', 
#       'el_lhvloose',
#       'mc_isTruthElectronFromZ', 
#       'mc_isTruthElectronAny',
#       'mc_isTruthElectronFromJpsi', 
#       'L1_EM3', 
#       'L1_EM7', 
#       'L1_EM15VH',
#       'L1_EM15VHI', 
#       'L1_EM20VH', 
#       'L1_EM20VHI', 
#       'L1_EM22VH', 
#       'L1_EM22VHI',
#       'L1_EM24VHI', 
#       'trig_L2_cl_lhvloose_et0to12',
#       'trig_L2_cl_lhvloose_et12to22', 
#       'trig_L2_cl_lhvloose_et22toInf',
#       'trig_L2_cl_lhloose_et0to12', 
#       'trig_L2_cl_lhloose_et12to22',
#       'trig_L2_cl_lhloose_et22toInf', 
#       'trig_L2_cl_lhmedium_et0to12',
#       'trig_L2_cl_lhmedium_et12to22', 
#       'trig_L2_cl_lhmedium_et22toInf',
#       'trig_L2_cl_lhtight_et0to12', 
#       'trig_L2_cl_lhtight_et12to22',
#       'trig_L2_cl_lhtight_et22toInf', 
#       'trig_L2_el_cut_pt0to15',
#       'trig_L2_el_cut_pt15to20', 
#       'trig_L2_el_cut_pt20to50',
#       'trig_L2_el_cut_pt50toInf',
#]



for et in range(3, 8):
    for eta in range(5):
        d = path.format(ET=et, ETA=eta)
        dd = d.split('/')[-1].replace('.npz','_slimmed.h5')
        df = load(d)
        print('saving... %s'%dd)
        save_hdf(df[col_names], dd)





