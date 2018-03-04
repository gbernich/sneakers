# Usage:
#
# ./launch_proc.sh  <# of python proc>


# Get Command line arguments
args=("$@")

NUM_PROC=${args[0]}

# Read account information for each python process to be launched


# Spawn multiple instances of Python with account info
for n in `seq 1 $NUM_PROC`;
do
	echo $n
	python test.py $n &
done
