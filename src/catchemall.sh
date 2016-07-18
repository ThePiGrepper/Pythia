#!/bin/bash

rm -f ${1}
touch ${1}
cont=0
MAXERRCNT=20
for id in $(seq $2 $3);do
  wget -P ./dump -q http://myfigurecollection.net/item/${id}
  if test $? -eq 0; then
    class=$(cat dump/${id} | sed 's#</[^>]*>#&\n#g' | sed -n '/item-category/ p' | cut -d'?' -f2 | cut -d'=' -f2 | cut -d'"' -f1)
    echo ${id}:${class} >> ${1}
    rm ./dump/${id}
  else
    ((cont++))
    echo ${id} >> $(dirname ${1})/error.log
    if test $cont -eq $MAXERRCNT; then
      echo "MAXERRORCNT($MAXERRCNT) reached."
      exit 1
    fi
  fi
done
