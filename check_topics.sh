#!/bin/bash
source /opt/ros/humble/setup.bash
OUT=/home/abcdefg/fusion_verify.txt
{
echo "===FIX==="
timeout 6 ros2 topic echo /fix --once 2>&1 | grep -E 'status:|latitude|longitude'
echo "===FIX_SUBSCRIBERS==="
timeout 5 ros2 topic info /fix -v 2>&1 | grep -A3 'Subscription count'
echo "===IMU_INFO==="
timeout 5 ros2 topic info /witmotion/imu -v 2>&1 | grep -A3 'Subscription count'
} > "$OUT" 2>&1
echo DONE