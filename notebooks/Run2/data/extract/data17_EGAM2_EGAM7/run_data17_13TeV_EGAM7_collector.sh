

#BASEPATH_EGAM1=/afs/cern.ch/work/j/jodafons/public/data17_13TeV/PhysVal_v2/EGAM7/*
BASEPATH_EGAM7=~jodafons/public/cern_data/data17_13TeV/PhysVal_v2/EGAM7/*


command='dump_electron.py -p "*/HLT/Physval/Egamma/fakes" --et_min 4 --et_max 15 -t 0 --pidname "!el_lhvloose" --level FATAL --et_bins "[0.0,7.0,10.0,15.0]"'
echo $command
prun_jobs.py -i $BASEPATH_EGAM7 -c "$command" -mt 40 -o output


mkdir data17_EGAM7
rm *.root
mv output* data17_EGAM7











