#!/bin/bash
source /opt/ros/humble/setup.bash
OUT=/home/abcdefg/fusion_verify.txt
{
echo "===NAVSAT_LOG==="
tail -6 /home/abcdefg/fusion_node.log
echo "===GPS_ODOM==="
timeout 6 ros2 topic echo /odometry/gps --field pose.pose.position 2>&1 | head -6
echo "===TF_ODOM_UTM==="
timeout 5 ros2 run tf2_ros tf2_echo odom utm 2>&1 | head -5
echo "===TF_TREE==="
timeout 6 ros2 run tf2_ros tf2_echo map base_link 2>&1 | head -3
} > "$OUT" 2>&1
echo DONE