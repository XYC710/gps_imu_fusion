#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from geometry_msgs.msg import TransformStamped
import serial, struct, math
from tf2_ros import TransformBroadcaster

def euler_to_quaternion(roll, pitch, yaw):
    """欧拉角(弧度)转四元数"""
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)
    qw = cr * cp * cy + sr * sp * sy
    qx = sr * cp * cy - cr * sp * sy
    qy = cr * sp * cy + sr * cp * sy
    qz = cr * cp * sy - sr * sp * cy
    return qx, qy, qz, qw

class WitmotionIMU(Node):
    def __init__(self):
        super().__init__('witmotion_imu')
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.1)
        self.pub = self.create_publisher(Imu, '/imu/data', 10)
        self.tf_broadcaster = TransformBroadcaster(self)
        self.acc = [0.0, 0.0, 0.0]
        self.gyro = [0.0, 0.0, 0.0]
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        self.buf = b''
        self.create_timer(0.01, self.read_loop)
        self.get_logger().info('IMU reader started on /dev/ttyUSB0@9600')

    def read_loop(self):
        n = self.ser.in_waiting
        if n:
            self.buf += self.ser.read(n)
        while len(self.buf) >= 11:
            i = self.buf.find(b'\x55')
            if i < 0:
                self.buf = b''
                break
            self.buf = self.buf[i:]
            if len(self.buf) < 11:
                break
            f = self.buf[:11]
            if (sum(f[:10]) & 0xFF) != f[10]:
                self.buf = self.buf[1:]
                continue
            t = f[1]
            if t == 0x51:  # 加速度 ±16g
                ax = struct.unpack('<h', f[2:4])[0] / 32768.0 * 16.0
                ay = struct.unpack('<h', f[4:6])[0] / 32768.0 * 16.0
                az = struct.unpack('<h', f[6:8])[0] / 32768.0 * 16.0
                self.acc = [ax*9.8, ay*9.8, az*9.8]
            elif t == 0x52:  # 角速度 ±2000dps
                gx = struct.unpack('<h', f[2:4])[0] / 32768.0 * 2000.0
                gy = struct.unpack('<h', f[4:6])[0] / 32768.0 * 2000.0
                gz = struct.unpack('<h', f[6:8])[0] / 32768.0 * 2000.0
                self.gyro = [math.radians(gx), math.radians(gy), math.radians(gz)]
            elif t == 0x53:  # 角度 ±180°
                self.roll = struct.unpack('<h', f[2:4])[0] / 32768.0 * 180.0
                self.pitch = struct.unpack('<h', f[4:6])[0] / 32768.0 * 180.0
                self.yaw = struct.unpack('<h', f[6:8])[0] / 32768.0 * 180.0
            self.buf = self.buf[11:]
            
            # 发布 TF（带姿态）
            qx, qy, qz, qw = euler_to_quaternion(
                math.radians(self.roll), 
                math.radians(self.pitch), 
                math.radians(self.yaw)
            )
            t = TransformStamped()
            t.header.stamp = self.get_clock().now().to_msg()
            t.header.frame_id = 'map'
            t.child_frame_id = 'imu_link'
            t.transform.translation.x = 0.0
            t.transform.translation.y = 0.0
            t.transform.translation.z = 0.0
            t.transform.rotation.x = qx
            t.transform.rotation.y = qy
            t.transform.rotation.z = qz
            t.transform.rotation.w = qw
            self.tf_broadcaster.sendTransform(t)
            
            # 发布 Imu 话题
            msg = Imu()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = 'imu_link'
            msg.linear_acceleration.x = self.acc[0]
            msg.linear_acceleration.y = self.acc[1]
            msg.linear_acceleration.z = self.acc[2]
            msg.angular_velocity.x = self.gyro[0]
            msg.angular_velocity.y = self.gyro[1]
            msg.angular_velocity.z = self.gyro[2]
            self.pub.publish(msg)

def main():
    rclpy.init()
    node = WitmotionIMU()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
