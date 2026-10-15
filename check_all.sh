#!/bin/bash
source /opt/ros/humble/setup.bash
OUT=/home/abcdefg/fusion_verify.txt
{
echo "===FIX==="
timeout 6 ros2 topic echo /fix --once 2>&1 | grep -E 'status:|latitude|longitude|altitude'
echo "===GPS_ODOM_POS==="
timeout 6 ros2 topic echo /odometry/gps --field pose.pose.position 2>&1 | head -8
echo "===TF_MAP_ODOM==="
timeout 5 ros2 run tf2_ros tf2_echo map odom 2>&1 | head -5
echo "===FILTERED_POS==="
timeout 6 ros2 topic echo /odometry/filtered --field pose.pose 2>&1 | head -10
} > "$OUT" 2>&1
echo DONE