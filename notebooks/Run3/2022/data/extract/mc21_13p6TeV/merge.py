

from Gaugi import expand_folders
from kepler.dumper import MergeNpzPool
import re

output1 = 'mc21_13p6TeV.80127X.P8B_A14_CTEQ6L1_Jpsie.Py8EG_A14NNPDF23LO_perf_JF17.40bins'
output2 = 'mc21_13p6TeV.601189.PhPy8EG_AZNLO_Zee.Py8EG_A14NNPDF23LO_perf_JF17.40bins'

path = 'data'

pat = re.compile(r'.+(?P<ID>et(?P<etBinIdx>\d+).eta(?P<etaBinIdx>\d+))\..+$')

paths = expand_folders( path )
bins = sorted(list(set([pat.match(f).group('ID')  for f in paths if pat.match(f) is not None])))

print (bins)

for key in bins:

    files = [ f for f in paths if key in f ]

    if ('et0' in key) or ('et1' in key) or ('et2' in key):
        output = output1
    else:
        output = output2

    merger  = MergeNpzPool(files, output + '_' + key , 30, 30)
    merger.run()

   
 


