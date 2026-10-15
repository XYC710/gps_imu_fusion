#!/bin/bash
source /opt/ros/humble/setup.bash
OUT=/home/abcdefg/fusion_verify.txt
{
echo "===FIX==="
timeout 6 ros2 topic echo /fix --once 2>&1 | grep -E 'status:|latitude|longitude'
echo "===NAVSAT_LOG==="
tail -4 /home/abcdefg/fusion_node.log
echo "===GPS_ODOM_3FRAMES==="
timeout 15 ros2 topic echo /odometry/gps --field pose.pose.position 2>&1 | grep -E 'x:|y:' | head -8
echo "===FILTERED_3FRAMES==="
timeout 15 ros2 topic echo /odometry/filtered --field pose.pose.position 2>&1 | grep -E 'x:|y:' | head -8
echo "===TF_ODOM_UTM==="
timeout 5 ros2 run tf2_ros tf2_echo odom utm 2>&1 | grep -E 'Translation|Invalid' | head -3
echo "===TF_ODOM_BASE==="
timeout 5 ros2 run tf2_ros tf2_echo odom base_link 2>&1 | grep -E 'Translation|Invalid' | head -3
} > "$OUT" 2>&1
echo DONE