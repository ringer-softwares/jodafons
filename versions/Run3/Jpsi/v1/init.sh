

rm -rf Gaugi || true
rm -rf neuralnet || true
rm -rf kepler || true
rm -rf rootplotlib || true

#rm -rf pybeamer|| true

export WANDB_API_KEY=$WANDB_API_KEY

#git clone ssh://git@gitlab.cern.ch:7999/atlas-trig-egamma/ringer/gaugi.git
#git clone ssh://git@gitlab.cern.ch:7999/atlas-trig-egamma/ringer/neuralnet.git
#git clone ssh://git@gitlab.cern.ch:7999/atlas-trig-egamma/ringer/kepler.git

cp -r /home/jodafons/git_repos/run3_ringer/jodafons/build/gaugi/Gaugi .
cp -r /home/jodafons/git_repos/run3_ringer/jodafons/build/neuralnet/neuralnet .
cp -r /home/jodafons/git_repos/run3_ringer/jodafons/build/kepler/kepler .
cp -r /home/jodafons/git_repos/run3_ringer/jodafons/build/rootplotlib/rootplotlib .

#git clone ssh://git@gitlab.cern.ch:7999/atlas-trig-egamma/ringer/pybeamer.git

# setup into the python path
export PYTHONPATH=$PYTHONPATH:$PWD
#export PYTHONPATH=$PYTHONPATH:$PWD/neuralnet
#export PYTHONPATH=$PYTHONPATH:$PWD/kepler
#export PYTHONPATH=$PYTHONPATH:$PWD/rootplotlib
#export PYTHONPATH=$PYTHONPATH:$PWD/pybeamer

echo $PYTHONPATH
ls -lisah