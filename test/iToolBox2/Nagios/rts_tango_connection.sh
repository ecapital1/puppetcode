#!/bin/bash

VAR=$(/opt/rts/rtd/bin/rtdsrvutil -i | grep -c "Tango Server")

if [ $VAR -eq 1 ];
then
  echo "OK"
  exit 0
else
  echo "Tango Server Down!"
  exit 2
fi
