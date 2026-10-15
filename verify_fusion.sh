#!/bin/bash
source /opt/ros/humble/setup.bash
OUT=/home/abcdefg/fusion_verify.txt
{
echo "===NODES==="
timeout 5 ros2 node list
echo "===GPS_ODOM_POS==="
timeout 8 ros2 topic echo /odometry/gps --field pose.pose.position
echo "===TF_MAP_ODOM==="
timeout 5 ros2 run tf2_ros tf2_echo map odom 2>&1 | head -5
} > "$OUT" 2>&1
echo DONE