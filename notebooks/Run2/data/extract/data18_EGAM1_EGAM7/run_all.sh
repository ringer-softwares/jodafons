source run_data18_13TeV_EGAM1_collector.sh
source run_data18_13TeV_EGAM7_collector.sh
#python merge_data17_13TeV_EGAM1_and_EGAM7.py

mkdir data
mv data18_* data
python merge.py


