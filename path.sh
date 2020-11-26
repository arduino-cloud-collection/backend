file=$(readlink -f ./path.sh)
dir=$(dirname $file)
export PYTHONPATH=$PYTHONPATH:$dir