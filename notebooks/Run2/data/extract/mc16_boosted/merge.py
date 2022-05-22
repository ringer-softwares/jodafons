

from Gaugi import expand_folders
from kepler.dumper import MergeNpzPool
import re

output = 'mc16_13TeV.309995.sgn.boosted_probes.GGF_radion_ZZ_llqq.merge.25bins.v3'
path = 'data'

pat = re.compile(r'.+(?P<ID>et(?P<etBinIdx>\d+).eta(?P<etaBinIdx>\d+))\..+$')

paths = expand_folders( path )
bins = sorted(list(set([pat.match(f).group('ID')  for f in paths if pat.match(f) is not None])))

print (bins)

for key in bins:

    files = [ f for f in paths if key in f ]
    merger  = MergeNpzPool(files, output + '_' + key , 10, 10)
    merger.run()
 


