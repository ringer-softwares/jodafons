
from Gaugi import expand_folders, mkdir_p, load, save
from tqdm import tqdm

basepath = '/home/jodafons/public/cern_data/tunings/Run3/Zee/v1'


files = expand_folders(basepath)

for path in tqdm(files):

    taskname = path.split('/')[9].replace('.r1', '.r2')
    jobname = path.split('/')[10]
    dirname = taskname + '/' + jobname
    mkdir_p(dirname)
    d = load(path)

    for tuned in d['tunedData']:
        del tuned['history']['summary']['rocs']
        del tuned['history']['summary']['hists']
    del d['protocol']
    del d['allow_pickle']
    ofile = dirname + '/tunedDiscr'
    save( d, ofile)

