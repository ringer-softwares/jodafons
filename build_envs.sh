
virtualenv -p python .ringer-env
source .ringer-env/bin/activate
pip install -r requirements.txt


mkdir build
cd build

git clone https://github.com/ringer-softwares/neuralnet.git
git clone https://github.com/ringer-softwares/kepler.git
git clone https://github.com/ringer-softwares/pybeamer.git
git clone https://github.com/ringer-softwares/rootplotlib.git
git clone https://github.com/ringer-softwares/gaugi.git

cd ..
