

BASEPATH=~/public/cern_data/mc21_13TeV/jpsi/*


command='python dump_electrons.py -p "*/HLT/EgammaMon/summary/events" --et_min 4 --et_max 15 -t 1 --level FATAL --mute --is_jpsi'
echo $command
prun_jobs.py -i $BASEPATH -c "$command" -mt 40 -o output


mkdir jpsi
rm *.root
mv output* jpsi





