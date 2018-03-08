# This file sets up environment variables to allow scripts to be run
# from any directory.

BASE_DIR="$PWD"

export SNEAKER_SRC="$BASE_DIR/src"
export SNEAKER_SITES="$SNEAKER_SRC/sites"

function sneakers()
{
	$SNEAKER_SRC/launch_proc.sh $1 $2
}