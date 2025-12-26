import React from 'react';
import clsx from 'clsx';
import styles from './CardsSection.module.css'; // Import CSS module
import ModuleCard from './ModuleCard';
import { FaRobot, FaCogs, FaBrain, FaEye } from 'react-icons/fa';

const CardsSection = () => {
  const modules = [
    {
      id: 1,
      title: "The Robotic Nervous System (ROS 2)",
      description: "Explore the Robot Operating System 2, the middleware that enables communication between robotic components and provides essential services like hardware abstraction, device drivers, and package management.",
      icon: FaRobot,
      link: "/docs/module1"
    },
    {
      id: 2,
      title: "The Digital Twin (Gazebo & Unity)",
      description: "Learn how to create accurate digital replicas of physical robots using simulation environments like Gazebo and Unity for testing, development, and training AI models in safe virtual environments.",
      icon: FaCogs,
      link: "/docs/module2"
    },
    {
      id: 3,
      title: "The AI-Robot Brain (NVIDIA Isaac™)",
      description: "Discover NVIDIA's Isaac platform for developing AI-powered robots with advanced perception, navigation, and manipulation capabilities using deep learning and reinforcement learning techniques.",
      icon: FaBrain,
      link: "/docs/module3"
    },
    {
      id: 4,
      title: "Vision-Language-Action (VLA)",
      description: "Understand how robots integrate visual perception, language understanding, and physical action to perform complex tasks in human environments and respond to natural language commands.",
      icon: FaEye,
      link: "/docs/module4"
    }
  ];

  return (
    <section className={styles['cards-section']}>
      <div className="container">
        <h2 className={styles['section-title']}>Book Modules</h2>
        <p className={styles['section-description']}>
          Explore the comprehensive modules of the Physical AI & Humanoid Robotics book
        </p>
        <div className={styles['cards-grid']}>
          {modules.map((module) => (
            <ModuleCard
              key={module.id}
              title={module.title}
              description={module.description}
              icon={module.icon}
              link={module.link}
            />
          ))}
        </div>
      </div>
    </section>
  );
};

export default CardsSection;