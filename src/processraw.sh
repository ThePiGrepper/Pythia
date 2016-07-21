#!/bin/bash

rm -rf ../doc/collecteddata.t
rm -rf ../data/index
mkdir -p ../doc
mkdir -p ../data/index
echo "Data Collected" >> ../doc/collecteddata.t
p=$(cat ../data/raw/* | wc -l)
echo "Overall Samples: $p">> ../doc/collecteddata.t
p=$(cat ../data/raw/* | sed -n "/:1$/ p" | wc -l)
cat ../data/raw/* | sed -n "/:1$/ p" | cut -d':' -f1 >> ../data/index/prepainted.t
echo "prepainted: $p" >> ../doc/collecteddata.t
p=$(cat ../data/raw/* | sed -n "/:2$/ p" | wc -l)
cat ../data/raw/* | sed -n "/:2$/ p" | cut -d':' -f1 >> ../data/index/action.t
echo "action/dolls: $p" >> ../doc/collecteddata.t
p=$(cat ../data/raw/* | sed -n "/:$/ p" | wc -l)
cat ../data/raw/* | sed -n "/:$/ p" | cut -d':' -f1 >> ../data/index/null.t
echo "null: $p" >> ../doc/collecteddata.t
