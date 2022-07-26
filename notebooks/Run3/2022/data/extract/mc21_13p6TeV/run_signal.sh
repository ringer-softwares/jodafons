

BASEPATH=/home/jodafons/public/cern_data/mc21_13p6TeV/ntuple/user.jodafons.*


command='python dump_electrons.py -p "*/HLT/EgammaMon/summary/events" --level FATAL'
echo $command
prun_jobs.py -i $BASEPATH -c "$command" -mt 40 -o output


mkdir signal
rm *.root
mv output* signal





