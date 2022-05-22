import os

old = 'data17_13TeV.AllPeriods.sgn.probes_lhvloose_EGAM1.bkg.vprobes_vlhvloose_EGAM7.GRL_v97.25bins.pandas_et%d_eta%d.npz'
new = 'data17_13TeV.AllPeriods.sgn.probes_lhvloose_EGAM1.bkg.vprobes_vlhvloose_EGAM7.GRL_v97.25bins_et%d_eta%d.npz'
for et in range(5):
    for eta in range(5):
        b_old = old%(et,eta)
        b_new = new%(et,eta)
        os.system( 'mv %s %s'%(b_old,b_new) )
