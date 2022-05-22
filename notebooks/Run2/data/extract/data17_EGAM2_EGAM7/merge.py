

from Gaugi import expand_folders
from kepler.dumper import MergeNpzPool
import re

output = 'data17_13TeV.AllPeriods.sgn.probes_lhvloose_EGAM2.bkg.vprobes_vlhvloose_EGAM7.GRL_v97.15bins'
path = 'data'

pat = re.compile(r'.+(?P<ID>et(?P<etBinIdx>\d+).eta(?P<etaBinIdx>\d+))\..+$')

paths = expand_folders( path )
bins = sorted(list(set([pat.match(f).group('ID')  for f in paths if pat.match(f) is not None])))

print (bins)

for key in bins:

    files = [ f for f in paths if key in f ]
    merger  = MergeNpzPool(files, output + '_' + key , 30, 30)
    merger.run()
 


