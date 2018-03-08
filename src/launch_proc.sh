# Usage:
#
# ./launch_proc.sh  <site src>  <accounts CSV file>


# Get Command line arguments
ARGS=("$@")
SITE=${ARGS[0]}
ACCOUNTS=${ARGS[1]}

# Save environment variable
OLDIFS=$IFS
IFS=,

# Initialize variables
count=0

# Make sure CSV file
[ ! -f $ACCOUNTS ] && { echo "ERROR: $ACCOUNTS file not found"; exit 99; }

# Read CSV file and spawn process for each account
while read username password launch_time size_id
do

	# Launch python process using CSV row data
	python3 $SNEAKER_SITES/$SITE.py $username $password $launch_time $size_id &
	((count++))

done < $ACCOUNTS

# Restore environment variable
IFS=$OLDIFS
