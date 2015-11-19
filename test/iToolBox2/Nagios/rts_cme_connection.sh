#!/bin/bash

VAR=$(/opt/rts/rtd/bin/rtdsrvutil -i | grep -c "CME FAST Market")

if [ $VAR -eq 1 ];
then
  echo "OK"
  exit 0
else
  echo "CME Market Down!"
  exit 2
fi
