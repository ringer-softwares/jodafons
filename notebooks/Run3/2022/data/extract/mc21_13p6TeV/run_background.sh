

#BASEPATH_EGAM1=/afs/cern.ch/work/j/jodafons/public/data17_13TeV/PhysVal_v2/EGAM7/*
#BASEPATH=~/public/cern_data/mc21_13TeV/jf17/*
BASEPATH=/home/jodafons/public/cern_data/mc21_13p6TeV/ntuple/user.mverissi.*



command='python dump_electrons.py -p "*/HLT/EgammaMon/summary/events" --is_jf17 --level FATAL'
echo $command
prun_jobs.py -i $BASEPATH -c "$command" -mt 40 -o output


mkdir background
rm *.root
mv output* background











