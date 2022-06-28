

from Gaugi import expand_folders
from kepler.dumper import MergeNpzPool
import re

output = 'mc21_13p6TeV.601189.PhPy8EG_AZNLO_Zee.Py8EG_A14NNPDF23LO_perf_JF17.25bins'
path = 'data'

pat = re.compile(r'.+(?P<ID>et(?P<etBinIdx>\d+).eta(?P<etaBinIdx>\d+))\..+$')

paths = expand_folders( path )
bins = sorted(list(set([pat.match(f).group('ID')  for f in paths if pat.match(f) is not None])))

print (bins)

for key in bins:

    files = [ f for f in paths if key in f ]
    merger  = MergeNpzPool(files, output + '_' + key , 30, 30)
    merger.run()

   
 


