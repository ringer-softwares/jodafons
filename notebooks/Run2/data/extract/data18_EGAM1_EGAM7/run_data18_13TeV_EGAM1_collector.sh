

#BASEPATH_EGAM1=/afs/cern.ch/work/j/jodafons/public/data17_13TeV/PhysVal_v2/EGAM1/*
BASEPATH_EGAM1=~jodafons/public/cern_data/data18_13TeV/PhysVal_v2/EGAM1/*


command='dump_electron.py -p "*/HLT/Egamma/Egamma/probes" --et_min 15 --et_max 1000 -t 1 --pidname "el_lhvloose" --level FATAL --mute --add_tdt_triggers'
echo $command
prun_jobs.py -i $BASEPATH_EGAM1 -c "$command" -mt 40 -o output


mkdir data18_EGAM1
rm *.root
mv output* data18_EGAM1





