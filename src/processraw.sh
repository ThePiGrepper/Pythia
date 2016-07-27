#!/bin/bash

rm -rf ../doc/collecteddata.t
rm -rf ../data/index
mkdir -p ../doc
mkdir -p ../data/index

#create report
echo "Data Collected" >> ../doc/collecteddata.t
p=$(cat ../data/raw/* | wc -l)
echo "Overall Samples: $p">> ../doc/collecteddata.t
p=$(cat ../data/raw/* | sed -n "/:1$/ p" | wc -l)
echo "prepainted: $p" >> ../doc/collecteddata.t
p=$(cat ../data/raw/* | sed -n "/:2$/ p" | wc -l)
echo "action/dolls: $p" >> ../doc/collecteddata.t
p=$(cat ../data/raw/* | sed -n "/:$/ p" | wc -l)
echo "null: $p" >> ../doc/collecteddata.t

#dump data
cat ../data/raw/* | sed -n "/:1$/ p" | cut -d':' -f1 | sort -g >> ../data/index/prepainted.t
cat ../data/raw/* | sed -n "/:2$/ p" | cut -d':' -f1 | sort -g >> ../data/index/action.t
cat ../data/raw/* | sed -n "/:$/ p" | cut -d':' -f1 | sort -g >> ../data/index/null.t
