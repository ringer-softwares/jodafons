

command = "maestro.py castor registry -d user.jodafons.data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.vprobes_vlhvloose_EGAM7.GRL_v97.25bins_et{ET}_eta{ETA}.ref.npz -p $PWD/data17_13TeV.AllPeriods.sgn.probes_lhmedium_EGAM1.bkg.vprobes_vlhvloose_EGAM7.GRL_v97.25bins_et{ET}_eta{ETA}.ref.npz"

import os

for et in range(5):
    for eta in range(5):
        os.system( command.format(ET=et, ETA=eta) )
