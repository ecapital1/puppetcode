#!/bin/bash

VAR=$(/opt/rts/rtd/bin/rtdsrvutil -i | grep -c "CME Trading")

if [ $VAR -eq 1 ];
then
  echo "OK"
  exit 0
else
  echo "CME Trading interface down!"
  exit 2
fi
