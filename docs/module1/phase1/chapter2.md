# ROS 2 Nodes, Topics, and Services

This chapter provides a clear explanation of fundamental ROS 2 concepts: Nodes, Topics, and Services, tailored for educators.

## 1. ROS 2 Nodes

In ROS 2, a **Node** is an executable process that performs computation. Nodes are designed to be modular, with each node responsible for a specific task (e.g., controlling a motor, reading sensor data, or performing a complex algorithm).

- **Purpose**: Encapsulate functionality.
- **Communication**: Nodes communicate with each other using ROS 2 communication mechanisms (Topics, Services, Actions).
- **Lifecycle**: Nodes have a managed lifecycle, allowing for deterministic startup and shutdown.

## 2. ROS 2 Topics

**Topics** are a crucial communication mechanism in ROS 2 for **asynchronous, many-to-many messaging**. They are used for continuous data streams where information is published by one or more nodes and subscribed to by one or more nodes.

- **Publishers**: Nodes that send data to a topic.
- **Subscribers**: Nodes that receive data from a topic.
- **Messages**: Data transmitted over topics are strongly typed ROS 2 messages.
- **Use Cases**: Sensor data (e.g., camera feeds, LiDAR scans), robot odometry, joint states.

## 3. ROS 2 Services

**Services** in ROS 2 provide a **synchronous request-response communication** paradigm. They are used for calls that are expected to complete and return a response, typically for operations that are not continuous or state-dependent.

- **Service Server**: A node that provides a service and responds to requests.
- **Service Client**: A node that sends a request to a service server and waits for a response.
- **Request/Response**: Services define a request message and a response message.
- **Use Cases**: Triggering an action (e.g., "take a picture", "move to a specific pose"), querying a parameter.

## Coding Exercises

### Exercise 1: ROS 2 Publisher Node in Python

**Objective**: Create a simple ROS 2 publisher node that continuously publishes a "Hello ROS 2" message to a topic.

1.  **Setup**: Create a new Python file (e.g., `minimal_publisher.py`) in your ROS 2 package.
2.  **Code**: Write a Python script that:
    *   Imports `rclpy` and `Node` from `rclpy.node`.
    *   Imports `String` message type from `std_msgs.msg`.
    *   Defines a class `MinimalPublisher` that inherits from `Node`.
    *   In the `__init__` method:
        *   Calls `super().__init__('minimal_publisher')`.
        *   Creates a publisher for a `String` message type on a topic named `'chatter'` with a queue size of 10.
        *   Creates a timer that calls a `timer_callback` function every 0.5 seconds.
    *   In the `timer_callback` method:
        *   Creates a `String` message.
        *   Sets the `data` field of the message to "Hello ROS 2: " followed by an incrementing counter.
        *   Publishes the message.
        *   Logs the published message using `self.get_logger().info()`.
    *   Implements a `main` function to initialize `rclpy`, create and spin the node, and then shut down `rclpy`.
3.  **Run**: Execute your publisher node.
    ```bash
    ros2 run your_package_name minimal_publisher
    ```
4.  **Verify**: Open another terminal and use `ros2 topic echo /chatter` to verify that your messages are being published.

### Exercise 2: ROS 2 Subscriber Node in Python

**Objective**: Create a simple ROS 2 subscriber node that receives and prints messages from the `'chatter'` topic created in Exercise 1.

1.  **Setup**: Create a new Python file (e.g., `minimal_subscriber.py`) in the same ROS 2 package.
2.  **Code**: Write a Python script that:
    *   Imports `rclpy` and `Node` from `rclpy.node`.
    *   Imports `String` message type from `std_msgs.msg`.
    *   Defines a class `MinimalSubscriber` that inherits from `Node`.
    *   In the `__init__` method:
        *   Calls `super().__init__('minimal_subscriber')`.
        *   Creates a subscriber for a `String` message type on the topic named `'chatter'` with a queue size of 10. It should call a `listener_callback` function when a message is received.
    *   In the `listener_callback` method:
        *   Logs the received message data using `self.get_logger().info()`.
    *   Implements a `main` function to initialize `rclpy`, create and spin the node, and then shut down `rclpy`.
3.  **Run**:
    *   In one terminal, run your publisher node from Exercise 1.
    *   In a second terminal, execute your subscriber node.
    ```bash
    ros2 run your_package_name minimal_subscriber
    ```
4.  **Observe**: Verify that the subscriber terminal is printing the messages published by the `minimal_publisher`.

### Exercise 3: ROS 2 Service Server and Client (Conceptual)

**Objective**: Design a conceptual ROS 2 service for a robot arm that can be commanded to move to a specific joint angle, and then query if the movement was successful.

1.  **Service Definition**: Define a custom ROS 2 service (e.g., `MoveArm.srv`) that takes a `joint_angle` (float) as a request and returns a `success` (boolean) and a `message` (string) as a response.
    ```
    # Request
    float32 joint_angle
    ---
    # Response
    bool success
    string message
    ```
2.  **Service Server Node**: Describe the conceptual Python node (`arm_controller_server`) that:
    *   Advertises the `MoveArm` service.
    *   Implements a callback function that receives the `joint_angle`, simulates the movement (e.g., adds a delay), and then returns `success: True` and an appropriate `message`.
3.  **Service Client Node**: Describe the conceptual Python node (`arm_commander_client`) that:
    *   Creates a client for the `MoveArm` service.
    *   Creates a `MoveArm` request with a target `joint_angle`.
    *   Calls the service and waits for the response.
    *   Prints the `success` status and `message` from the service response.

Explain how this synchronous communication differs from topic-based communication and in what scenarios a service would be preferred over a topic.
