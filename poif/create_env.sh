cd "$(dirname "$0")"

yes | conda env remove -n poif
yes | conda create -n poif python=3.6
conda develop -n poif .