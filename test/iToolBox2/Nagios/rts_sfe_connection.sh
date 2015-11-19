#!/bin/bash

VAR=$(/opt/rts/rtd/bin/rtdsrvutil -i | grep -c "SFE Interface")

if [ $VAR -eq 1 ];
then
 echo "OK"
 exit 0
else
  echo "No SFE Connection" 
  exit 2
fi
