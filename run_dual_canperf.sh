#!/bin/bash

CANPERF_SCRIPT="./my_canperf.sh"

IFACE1="can0"
LOG1="can_fd_12min.log"

IFACE2="can1"
LOG2="can_fd_20min.log"

$CANPERF_SCRIPT "$IFACE1" "$LOG1" > log_${IFACE1}.txt 2>&1 &
PID1=$!

$CANPERF_SCRIPT "$IFACE2" "$LOG2" > log_${IFACE2}.txt 2>&1 &
PID2=$!

wait $PID1
wait $PID2

echo "[INFO] Both CAN FD replays completed."
