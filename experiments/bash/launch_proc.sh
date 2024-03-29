# Usage:
#
# ./launch_proc.sh  <accounts CSV file>


# Get Command line arguments
ARGS=("$@")
INPUT=${ARGS[0]}

# Save environment variable
OLDIFS=$IFS
IFS=,

# Initialize variables
count=0

# Make sure CSV file
[ ! -f $INPUT ] && { echo "ERROR: $INPUT file not found"; exit 99; }

# Read CSV file and spawn process for each account
while read username password launch_time size_id
do

	# Launch python process using CSV row data
	python test.py $count $username $password $launch_time $size_id &
	((count++))
	
done < $INPUT

# Restore environment variable
IFS=$OLDIFS
