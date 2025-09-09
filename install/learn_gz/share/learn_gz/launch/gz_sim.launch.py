import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    ros_gz_sim_share = get_package_share_directory("ros_gz_sim")
    this_share = get_package_share_directory("learn_gz")

    default_world = os.path.join(this_share, "worlds", "minimal_empty.sdf")
    world = LaunchConfiguration("world")
    bridge_config = LaunchConfiguration("bridge_config")

    return LaunchDescription ([
        DeclareLaunchArgument(
            "world", 
            default_value=default_world
        ),

        DeclareLaunchArgument(
            "bridge_config", 
            default_value=os.path.join(this_share, "config", "bridge_config.yaml")
        ),
        
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(ros_gz_sim_share, "launch", "gz_sim.launch.py")
            ),
            launch_arguments={"gz_args": world}.items(),
        ),

        # ROS2 Gazebo Bridge (Topics configured in /config/bridge_config.yaml)
        Node(
            package="ros_gz_bridge",
            executable="parameter_bridge",
            output="screen",
            parameters=[{"config_file": bridge_config}],
        ),
    ])