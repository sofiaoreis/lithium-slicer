#!/bin/sh

IFS=',' read -ra ADDR <<< "$2"
for i in "${ADDR[@]}"; do
    bash runner.sh $1 $i &
done

wait
echo all processes complete