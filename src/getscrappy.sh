#!/bin/bash

#$1: minval
#$2: maxval
#$3: filename

#if test -z ${3}; then
#  file="default.t"
#else
#  file="$3"
#fi
./catchemall.sh $3 $1 $2 &
./showprogress.sh $3 $1 $2
