#!/bin/sh

PROJECT=$1
BUGS=$2

IFS="," read -ra ADDR <<< "$BUGS"

if [[ ${#ADDR[@]} > 1 ]]; then BUGS_LIST="${ADDR[@]}"; else BUGS_LIST=$(seq 1 $BUGS); fi

for BUG in $BUGS_LIST; do
	bash runner.sh $PROJECT $BUG &
done

wait
echo all processes complete