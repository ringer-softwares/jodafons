

#BASEPATH_EGAM1=/afs/cern.ch/work/j/jodafons/public/data17_13TeV/PhysVal_v2/EGAM1/*
BASEPATH_EGAM1=~jodafons/public/cern_data/data17_13TeV/PhysVal_v2/EGAM2/*


command='dump_electron.py -p "*/HLT/Egamma/Egamma/probes" --et_min 4 --et_max 15 --pidname "el_lhvloose" -t 1 --level FATAL --et_bins "[0.0,7.0,10.0,15.0]"'
echo $command
prun_jobs.py -i $BASEPATH_EGAM1 -c "$command" -mt 40 -o output


mkdir data17_EGAM2
rm *.root
mv output* data17_EGAM2





