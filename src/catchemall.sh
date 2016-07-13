#!/bin/bash

rm -f ${1}
touch ${1}
for id in $(seq $2 $3);do
  wget -P ./dump -q http://myfigurecollection.net/item/${id}
  class=$(cat dump/${id} | sed 's#</[^>]*>#&\n#g' | sed -n '/item-category/ p' | cut -d'?' -f2 | cut -d'=' -f2 | cut -d'"' -f1)
  echo ${id}:${class} >> ${1}
  rm ./dump/${id}
done
