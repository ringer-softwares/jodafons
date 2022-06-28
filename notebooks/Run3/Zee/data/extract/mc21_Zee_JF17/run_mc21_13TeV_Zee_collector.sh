

BASEPATH=~/public/cern_data/mc21_13TeV/zee/*


command='python dump_electrons.py -p "*/HLT/EgammaMon/summary/events" --et_min 15 --et_max 13000 -t 1 --level FATAL --mute --is_zee'
echo $command
prun_jobs.py -i $BASEPATH -c "$command" -mt 40 -o output


mkdir zee
rm *.root
mv output* zee





