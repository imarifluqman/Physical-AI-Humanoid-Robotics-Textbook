# Bridging Python Agents to ROS Controllers (rclpy)

This chapter explores how to bridge Python-based AI agents with ROS 2 robotic controllers using `rclpy`, the Python client library for ROS 2. The focus is on simplified integration patterns suitable for educational purposes.

## 1. Introduction to `rclpy`

`rclpy` enables Python programs to interface with the ROS 2 ecosystem. It provides functionalities to create nodes, publish to topics, subscribe to topics, create services, and interact with parameters.

## 2. Setting up a Python ROS 2 Node

To bridge a Python agent, the first step is to create a ROS 2 node in Python.

```python
import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## 3. Publishing Data from a Python Agent

Python agents can send commands or data to ROS 2 controllers by publishing messages to relevant topics. This is a one-way, asynchronous communication suitable for control signals, status updates, or sensor data emulation.

## 4. Subscribing to Robot Feedback

To receive feedback from ROS 2 controllers (e.g., current joint angles, odometry, or sensor readings), a Python agent can subscribe to ROS 2 topics. This allows the agent to perceive the robot's state and environment.

## 5. Using ROS 2 Services for Coordinated Actions

For actions that require a direct response or coordinated execution, Python agents can act as service clients to call ROS 2 services exposed by the robot controllers. This is useful for triggering specific behaviors or querying states.

## 6. Simplified Integration Patterns

For teaching, focus on:
- **Direct Topic Publishing**: Simple commands from Python to robot.
- **Feedback Subscription**: Python agent reads robot state.
- **Basic Service Calls**: Triggering predefined robot behaviors.

Avoid complex multi-threading or advanced synchronization for initial lessons. Emphasize clear message definitions and straightforward data flow.

## Hands-on Labs

### Lab 1: Python Publisher-Subscriber Communication

**Objective**: Implement a Python ROS 2 publisher and subscriber to exchange simple string messages.

1.  **Create a ROS 2 Package**: If you haven't already, create a new ROS 2 package (e.g., `python_ros_comm`) in your `src` directory:
    ```bash
    cd ~/ros2_ws/src
    ros2 pkg create --build-type ament_python python_ros_comm
    cd python_ros_comm
    mkdir python_ros_comm
    touch python_ros_comm/__init__.py
    ```
2.  **Publisher Node (`publisher_member_function.py`)**:
    *   Inside `python_ros_comm/python_ros_comm/`, create a file named `publisher_member_function.py`.
    *   Copy the `MinimalPublisher` code from Section 2 into this file. Ensure the imports (`rclpy`, `Node`, `String`) are correct.
    *   Modify the `setup.py` in your package root to include your publisher executable:
        ```python
        from setuptools import setup

        package_name = 'python_ros_comm'

        setup(
            name=package_name,
            version='0.0.0',
            packages=[package_name],
            data_files=[
                ('share/' + package_name, ['package.xml']),
                ('share/' + package_name + '/resource', ['resource/' + package_name]),
            ],
            install_requires=['setuptools'],
            zip_safe=True,
            maintainer='your_name',
            maintainer_email='your_email@example.com',
            description='TODO: Package description',
            license='TODO: License declaration',
            tests_require=['pytest'],
            entry_points={
                'console_scripts': [
                    'talker = python_ros_comm.publisher_member_function:main',
                ],
            },
        )
        ```
3.  **Subscriber Node (`subscriber_member_function.py`)**:
    *   Inside `python_ros_comm/python_ros_comm/`, create a file named `subscriber_member_function.py`.
    *   Write a Python script for a `MinimalSubscriber` similar to the conceptual example in Chapter 1 or Section 4, but make it functional with `rclpy`.
    *   Add this subscriber executable to your `setup.py` under `entry_points`:
        ```python
        # ... existing setup.py content ...
        entry_points={
            'console_scripts': [
                'talker = python_ros_comm.publisher_member_function:main',
                'listener = python_ros_comm.subscriber_member_function:main',
            ],
        },
        )
        ```
4.  **Build and Run**:
    *   Navigate to your ROS 2 workspace root (`~/ros2_ws`) and build your package:
        ```bash
        colcon build --packages-select python_ros_comm
        ```
    *   Source your workspace setup files:
        ```bash
        source install/setup.bash
        ```
    *   Run the publisher in one terminal:
        ```bash
        ros2 run python_ros_comm talker
        ```
    *   Run the subscriber in another terminal:
        ```bash
        ros2 run python_ros_comm listener
        ```
5.  **Observe**: Verify that the subscriber is receiving and printing messages from the publisher.

### Lab 2: Python ROS 2 Service (Conceptual Design)

**Objective**: Design the service definition and conceptual Python service server and client nodes for a simple number addition service.

1.  **Service Definition (`AddTwoInts.srv`)**:
    *   Inside your `python_ros_comm` package, create a directory `srv` (if it doesn't exist).
    *   Create a file `srv/AddTwoInts.srv` with the following content:
        ```
        int64 a
        int64 b
        ---
        int64 sum
        ```
2.  **`package.xml` Modification**: Add the following to your `package.xml`:
    ```xml
    <build_depend>rosidl_default_generators</build_depend>
    <exec_depend>rosidl_default_runtime</exec_depend>
    <member_of_group>rosidl_interface_packages</member_of_group>
    ```
3.  **`CMakeLists.txt` Modification**: Add directives to build your service. (Note: This is a Python chapter, but service generation requires CMake).
    ```cmake
    find_package(rosidl_default_generators REQUIRED)
    rosidl_generate_interfaces(${PROJECT_NAME}
      "srv/AddTwoInts.srv"
    )
    ```
4.  **Conceptual Server Node (`add_two_ints_server.py`)**:
    *   Describe how you would implement a Python node that advertises the `AddTwoInts` service and responds to requests by summing `a` and `b`.
5.  **Conceptual Client Node (`add_two_ints_client.py`)**:
    *   Describe how you would implement a Python node that creates a client for `AddTwoInts` and sends a request with two numbers.

Explain the necessary modifications to `setup.py` for including service executables (if they were implemented).