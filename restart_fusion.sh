#!/bin/bash
for p in $(pgrep -f 'robot_localization|gps_static_tf|static_transform'); do
  [ "$p" != "$$" ] && kill "$p" 2>/dev/null
done
sleep 1
source /opt/ros/humble/setup.bash
nohup ros2 launch /home/abcdefg/gps_imu_fusion/fusion.launch.py > /home/abcdefg/fusion_node.log 2>&1 &
sleep 8
echo DONE