from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Declare launch arguments
    port_arg = DeclareLaunchArgument(
        'port', default_value='/dev/ttyACM0', description='Port for the IMU'
    )
    time_out_arg = DeclareLaunchArgument(
        'time_out', default_value='0.5', description='Timeout for the IMU'
    )
    baudrate_arg = DeclareLaunchArgument(
        'baudrate', default_value='115200', description='Baud rate for the IMU'
    )
    imu_topic_arg = DeclareLaunchArgument(
        'imu_topic', default_value='imu', description='IMU topic name'
    )
    frame_id_arg = DeclareLaunchArgument(
        'frame_id', default_value='imu_link', description='Frame ID for the IMU'
    )
    debug_arg = DeclareLaunchArgument(
        'debug', default_value='false', description='Enable debug nodes'
    )

    # Get the path to the RViz config file
    rviz_config_default = os.path.join(
        get_package_share_directory('icm_20948'), 'rviz2', 'imu.rviz'
    )
    rviz_config_arg = DeclareLaunchArgument(
        'rviz_config', default_value=rviz_config_default, description='RViz config file'
    )

    # Define the IMU node
    imu_node = Node(
        package='icm_20948',
        executable='imu_node',
        output='screen',
        parameters=[{
            'port': LaunchConfiguration('port'),
            'time_out': LaunchConfiguration('time_out'),
            'baudrate': LaunchConfiguration('baudrate'),
            'imu_topic': LaunchConfiguration('imu_topic'),
            'frame_id': LaunchConfiguration('frame_id'),
        }]
    )

    # Define the debug group
    debug_group = GroupAction(
        condition=IfCondition(LaunchConfiguration('debug')),
        actions=[
            # RViz node
            Node(
                package='rviz2',
                executable='rviz2',
                arguments=['-d', LaunchConfiguration('rviz_config')],
            ),
            # rqt_plot nodes
            Node(
                package='rqt_plot',
                executable='rqt_plot',
                arguments=[[
                    '/', LaunchConfiguration('imu_topic'), '/linear_acceleration/x:y:z'
                ]],
            ),
            Node(
                package='rqt_plot',
                executable='rqt_plot',
                arguments=[[
                    '/', LaunchConfiguration('imu_topic'), '/angular_velocity/x:y:z'
                ]],
            ),
            Node(
                package='rqt_plot',
                executable='rqt_plot',
                arguments=[[
                    '/', LaunchConfiguration('imu_topic'), '/orientation/x:y:z:w'
                ]],
            ),
        ]
    )

    # Create and return the launch description
    return LaunchDescription([
        port_arg,
        time_out_arg,
        baudrate_arg,
        imu_topic_arg,
        frame_id_arg,
        debug_arg,
        rviz_config_arg,
        imu_node,
        debug_group,
    ])
