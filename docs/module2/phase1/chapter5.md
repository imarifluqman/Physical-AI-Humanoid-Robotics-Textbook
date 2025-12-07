# Simulating Physics, Gravity, and Collisions in Gazebo

This chapter guides educators through setting up practical robotic simulations in Gazebo, focusing on the fundamental principles of physics, gravity, and collision detection.

## 1. Introduction to Gazebo Physics Engine

Gazebo utilizes powerful physics engines (like ODE, Bullet, DART, Simbody) to accurately simulate rigid body dynamics. Understanding how these engines work is crucial for creating realistic robot behaviors and interactions.

## 2. Configuring Gravity

Gravity is a fundamental force in any realistic simulation. Gazebo allows you to configure the gravitational vector, typically set to `0 0 -9.8 m/s^2` for Earth's gravity in the Z-direction.

- **SDF Configuration**: Gravity is usually defined in the `world` section of a Simulation Description Format (SDF) file.

```xml
<world name="default">
  <gravity>0 0 -9.8</gravity>
  ...
</world>
```

## 3. Defining Collisions

**Collision shapes** define the physical boundaries of a robot or object for interaction with other objects in the simulated environment. Accurate collision models are vital for preventing interpenetration and simulating physical contact.

- **Primitive Shapes**: Box, cylinder, sphere are common collision primitives.
- **Mesh Collisions**: For more complex shapes, mesh files (e.g., `.dae`, `.stl`) can be used, often simplified for computational efficiency.
- **SDF Configuration**: Collision elements are defined within a `<link>` in the SDF, nested under a `<collision>` tag.

```xml
<link name="robot_base">
  <collision name="base_collision">
    <geometry>
      <box>
        <size>0.2 0.2 0.1</size>
      </box>
    </geometry>
  </collision>
  ...
</link>
```

## 4. Understanding Contact and Friction

When collision shapes make contact, the physics engine calculates forces based on material properties like friction and restitution. These properties influence how objects slide, grip, or bounce off each other.

- **Friction**: Resistance to motion between surfaces in contact.
- **Restitution**: Bounciness or elasticity of a collision.

## 5. Practical Simulation Setup for Teachers

- **Simple Scenarios**: Start with basic shapes (cubes, spheres) interacting on a flat plane to demonstrate gravity and collisions.
- **Robot-Environment Interaction**: Introduce a simple robot (e.g., a differential drive robot) navigating an environment with obstacles.
- **Debugging Physics**: Teach students how to visualize collision shapes and debug unexpected physical behaviors in Gazebo.

## Student Exercises

### Exercise 1: Configuring Gravity in a Gazebo World

**Objective**: Create a simple Gazebo world and modify its gravity settings to observe the effect on simulated objects.

1.  **Create a World File (`gravity_test.world`)**:
    *   Create a new `.world` file (XML format) for Gazebo.
    *   Define a basic `<world>` element with a `<light>` and a flat `<model name="ground_plane">`.
    *   Initially, set the gravity to Earth's standard: `<gravity>0 0 -9.8</gravity>`.
    *   Add a simple box model: `<model name="my_box">` with a `<link>` containing `<visual>` and `<collision>` (e.g., a simple box shape) and `<pose>0 0 5 0 0 0</pose>` so it starts above the ground.
2.  **Launch Gazebo**: Launch Gazebo with your custom world file:
    ```bash
    gazebo --verbose gravity_test.world
    ```
3.  **Observe**: Note how the box falls under gravity.
4.  **Modify Gravity**: Edit your `gravity_test.world` file to change the gravity vector (e.g., `<gravity>0 0 -1.0</gravity>` for weaker gravity, or `<gravity>0 0 0</gravity>` to remove gravity, or even `<gravity>0 0 9.8</gravity>` for inverted gravity).
5.  **Relaunch and Observe**: Relaunch Gazebo with the modified world and observe the different behaviors of the box. Document your observations for each gravity setting.

### Exercise 2: Defining Collision Shapes

**Objective**: Create a URDF/SDF model with explicit visual and collision geometries and observe their impact in Gazebo.

1.  **Create a Robot Model (`collision_robot.urdf` or `.sdf`)**:
    *   Create a robot description file. Define a `base_link`.
    *   Add a `<visual>` element with a simple geometry (e.g., a large sphere or box) and a distinct color.
    *   Add a `<collision>` element with a *different* geometry or size than the visual (e.g., a smaller box inside a large visual sphere, or vice-versa).
    *   Ensure the `<inertial>` properties are defined.
2.  **Spawn in Gazebo**: Spawn your robot model in Gazebo. If using URDF, you might use `ros2 launch gazebo_ros spawn_entity.launch.py entity:=collision_robot -file collision_robot.urdf`.
3.  **Visualize Collisions**: In the Gazebo GUI, go to `View -> Collisions` to visualize the collision shapes. Observe how they differ from the visual shapes.
4.  **Experiment**: Add another simple object (e.g., a static box) to your world. Push your robot into the static object in Gazebo. Observe how the robot interacts with the static object based on its collision geometry, not its visual geometry.
5.  **Documentation**: Describe the difference between visual and collision geometries and why they are often different. Explain how observing collision shapes helps debug robot interactions.

### Exercise 3: Simulating Simple Object Interactions

**Objective**: Set up a scenario in Gazebo to demonstrate contact, friction, and restitution between multiple objects.

1.  **Create a World (`interaction_test.world`)**:
    *   Define a world with gravity set to `0 0 -9.8`.
    *   Add a `ground_plane`.
    *   Add two distinct `box` models. Give them different material properties if you know how (e.g., by defining `<surface>` properties in SDF, but for simplicity, default properties are fine for a start).
    *   Position one box slightly above the other, or one sliding towards another.
2.  **Simulate Falling/Sliding**: Release the simulation and observe the interaction:
    *   Do they bounce? (Restitution)
    *   Do they slide easily or resist motion? (Friction)
    *   Do they interpenetrate or collide realistically?
3.  **Introduce an Inclined Plane (Optional)**: Replace the flat ground plane with a simple ramp to observe how friction affects sliding down an incline.
4.  **Analysis**: Discuss how different material properties (friction, restitution) would affect the observed interactions. Research how to define these properties in SDF/URDF and suggest modifications to create, for example, a very bouncy rubber ball versus a sticky, high-friction block.

