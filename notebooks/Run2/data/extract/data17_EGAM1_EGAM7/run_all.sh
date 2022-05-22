source run_data17_13TeV_EGAM1_collector.sh
source run_data17_13TeV_EGAM7_collector.sh
mkdir data
mv data17_* data
python merge.py
