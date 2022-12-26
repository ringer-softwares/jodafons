
source .ringer-env/bin/activate


echo "=========================================================="
echo "setup all packages..."
cd build
cd gaugi && source scripts/setup.sh && cd ..
cd pybeamer && source scripts/setup.sh && cd ..
cd kepler && source scripts/setup.sh && cd ..
cd neuralnet && source scripts/setup.sh && cd ..
cd rootplotlib && source scripts/setup.sh && cd ..
cd ..
export PYTHONPATH=`pwd`:$PYTHONPATH
echo "=========================================================="

echo ""
echo "=========================================================="
echo "setup root..."
source /apt/root/buildthis/bin/thisroot.sh
echo "=========================================================="