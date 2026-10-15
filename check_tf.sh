#!/bin/bash
source /opt/ros/humble/setup.bash
OUT=/home/abcdefg/fusion_verify.txt
{
echo "===TF_ODOM_UTM==="
timeout 5 ros2 run tf2_ros tf2_echo odom utm 2>&1 | head -5
echo "===FILTERED_4FRAMES==="
timeout 15 ros2 topic echo /odometry/filtered --field pose.pose.position 2>&1 | grep -E 'x:|y:' | head -10
} > "$OUT" 2>&1
echo DONE