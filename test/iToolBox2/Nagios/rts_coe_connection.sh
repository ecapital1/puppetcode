#!/bin/bash

VAR=$(/opt/rts/rtd/bin/rtdsrvutil -i | grep -c "COE FAST Market")

if [ $VAR -eq 1 ];
then
  echo "OK"
  exit 0
else
  echo "COE Market Interface Down!"
  exit 2
fi
