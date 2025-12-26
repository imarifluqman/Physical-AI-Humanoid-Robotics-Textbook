# Understanding URDF for Humanoids

This chapter introduces the Unified Robot Description Format (URDF), explaining its structure and how it's used to describe humanoid robots within ROS 2. It includes student activities to build and visualize robot descriptions.

## 1. Introduction to URDF

**URDF (Unified Robot Description Format)** is an XML format used in ROS 2 to describe all elements of a robot. This includes its kinematic and dynamic properties, visual appearance, and collision characteristics. URDF files are essential for simulating robots in environments like Gazebo and visualizing them in tools like RViz.

- **Kinematic Description**: Defines the robot's links (rigid bodies) and joints (connections between links) and their hierarchical structure.
- **Dynamic Description**: Specifies mass, inertia, and friction properties for each link.
- **Visual Description**: Describes the 3D models and colors used to render the robot.
- **Collision Description**: Defines simplified geometric shapes for collision detection.

## 2. URDF Structure for Humanoid Robots

Humanoid robots have complex kinematic chains and many degrees of freedom. A URDF for a humanoid typically includes:

- **Root Link**: Often a `base_link` or `pelvis` from which the entire robot structure originates.
- **Torso and Head**: Links and joints for the upper body.
- **Arms**: Multiple links (shoulder, upper arm, forearm, hand) and joints (revolute, prismatic) for each arm.
- **Legs**: Complex chains of links (hip, thigh, shank, foot) and joints for bipedal locomotion.
- **Sensors**: Description of sensors (e.g., cameras, IMUs, force sensors) attached to various links.

```xml
<robot name="humanoid_robot">

  <link name="base_link">
    <visual>
      <geometry><box size="0.1 0.2 0.3"/></geometry>
    </visual>
    <collision>
      <geometry><box size="0.1 0.2 0.3"/></geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
  </link>

  <joint name="hip_joint" type="revolute">
    <parent link="base_link"/>
    <child link="thigh_link"/>
    <origin xyz="0 0 -0.15" rpy="0 0 0"/>
    <axis xyz="1 0 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1.0"/>
  </joint>

  <!-- More links and joints for legs, arms, head -->

</robot>
```

## 3. Visualizing URDF in RViz

**RViz** is a 3D visualization tool for ROS 2. It can load URDF models and display the robot's kinematic structure, visual models, and even collision shapes. This is invaluable for debugging robot descriptions.

- **`robot_state_publisher`**: A ROS 2 node that reads the URDF and the current joint states (from sensor readings or simulated data) and publishes the robot's 3D pose.
- **`joint_state_publisher`**: A GUI tool or node that allows you to manually control joint values to pose the robot.

## 4. Student Activities for Robot Description

### Activity 1: Simple Link and Joint

**Objective**: Create a URDF file for a single link connected to a base by a revolute joint.

1.  **Create `my_robot.urdf`**: Start with a minimal XML structure.
2.  **Define a `base_link`**: Add a simple box geometry for visual and collision properties. Give it an inertial tag.
3.  **Define a `second_link`**: Similar to `base_link` but perhaps smaller.
4.  **Connect with a `joint`**: Create a `revolute` joint connecting `base_link` (parent) to `second_link` (child). Define its `origin` (position and orientation) and `axis` of rotation.
5.  **Visualize**: Use `ros2 launch urdf_tutorial display.launch.py model:=my_robot.urdf` (assuming `urdf_tutorial` package is installed) to view your robot.

### Activity 2: Adding a Humanoid Leg Segment

**Objective**: Extend your `my_robot.urdf` to include a more complex segment, like a thigh and shank connected by a knee joint.

1.  **Thigh Link**: Add a new link representing a thigh with appropriate dimensions.
2.  **Knee Joint**: Create a `revolute` joint connecting the `thigh_link` to a `shank_link` (lower leg). Pay attention to the `origin` and `axis` to make it bend realistically.
3.  **Shank Link**: Add a link for the lower leg.
4.  **Visualize and Refine**: Load in RViz and adjust joint origins/axes until the leg segment moves as expected.

### Activity 3: Conceptual Humanoid Sensor Placement

**Objective**: Think about where sensors would be placed on a humanoid robot and how they would be represented in URDF.

1.  **Identify Sensors**: List common sensors on a humanoid (e.g., head camera, IMU in torso, force sensors in feet).
2.  **URDF Integration**: For each sensor, describe conceptually:
    *   Which existing link it would be attached to.
    *   What kind of `joint` (fixed) would connect it.
    *   How its `origin` (position/orientation relative to the parent link) would be determined.
    *   (Optional) How its properties might be extended using `<gazebo>` tags (not part of core URDF but common for simulation).
