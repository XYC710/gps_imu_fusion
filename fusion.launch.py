import os
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    params_file = os.path.join(os.path.expanduser('~'), 'gps_imu_fusion', 'fusion_params.yaml')

    return LaunchDescription([
        # GPS -> UTM 变换节点（订阅 /fix + IMU yaw，输出 /odometry/gps，发布 map->odom）
        Node(
            package='robot_localization',
            executable='navsat_transform_node',
            name='navsat_transform_node',
            parameters=[params_file],
            remappings=[
                ('imu', '/witmotion/imu'),
                ('gps/fix', '/fix'),
                ('gps/filtered', '/gps/filtered'),
            ],
        ),
        # EKF：融合 GPS 位置 + IMU 姿态，输出 /odometry/filtered，发布 odom->base_link
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            parameters=[params_file],
        ),
        # 静态 TF：GPS 天线相对 base_link 的位置（z=0.3m）
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='gps_static_tf',
            arguments=['0', '0', '0.3', '0', '0', '0', 'base_link', 'gps'],
        ),
    ])