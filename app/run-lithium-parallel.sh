#!/bin/sh

if $1 == '0'; then
    for BUG in $(seq 1 $1); do 
        bash runner.sh $2 $i &
    done
elif $1 == '1'; then
    IFS=',' read -ra ADDR <<< "$3"
    for i in "${ADDR[@]}"; do
        bash runner.sh $2 $i &
    done
fi

wait
echo all processes complete