#!/bin/bash
source /opt/ros/humble/setup.bash
OUT=/home/abcdefg/fusion_verify.txt
{
echo "===FILTERED==="
timeout 6 ros2 topic echo /odometry/filtered --once 2>&1 | head -20
} > "$OUT" 2>&1
echo DONE