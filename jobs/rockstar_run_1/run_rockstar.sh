#!/bin/bash

ROCKSTAR="$HOME/software/rockstar"
OUTPUT_DIR="rockstar"
ROCKSTAR_CFG="my_rockstar.cfg"
#ROCKSTAR_CFG="$OUTPUT_DIR/restart.cfg"

AUTO_ROCKSTAR_CFG="$OUTPUT_DIR/auto-rockstar.cfg"
rm $AUTO_ROCKSTAR_CFG
$ROCKSTAR -c $ROCKSTAR_CFG &> rs_server.out &
while [ ! -f $AUTO_ROCKSTAR_CFG ]; do sleep 1; done
mpirun $ROCKSTAR -c $AUTO_ROCKSTAR_CFG &> rs_client.out
