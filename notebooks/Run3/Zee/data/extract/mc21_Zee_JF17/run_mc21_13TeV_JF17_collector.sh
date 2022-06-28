

#BASEPATH_EGAM1=/afs/cern.ch/work/j/jodafons/public/data17_13TeV/PhysVal_v2/EGAM7/*
BASEPATH=~/public/cern_data/mc21_13TeV/jf17/*



command='python dump_electrons.py -p "*/HLT/EgammaMon/summary/events" --et_min 15 --et_max 13000 -t 0 --level FATAL --mute'
echo $command
prun_jobs.py -i $BASEPATH -c "$command" -mt 40 -o output


mkdir jf17
rm *.root
mv output* jf17











