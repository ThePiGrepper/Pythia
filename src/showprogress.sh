#!/bin/bash
export LC_NUMERIC="en_US.UTF-8"
last=0
range=$(expr $3 - $2)
while [[ $last -lt $3 ]];do
  sleep 4
  last=$(tail -1 $1 | cut -d':' -f1)
  curr=$(echo "100 * ( $last - $2 ) / $range" | bc -l)
  #curr=$(expr ${sc1}  / ${range} )
  printf "progress:%.2f%%\r" "$curr"
done
printf "\n"
