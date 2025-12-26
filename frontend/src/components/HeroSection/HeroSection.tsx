import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './HeroSection.module.css'; // Import CSS module
import robotImage from './robot.png'; // Import the image

const HeroSection = () => {
  const { siteConfig } = useDocusaurusContext();

  return (
    <section className={styles['hero-section']}>
      <div className="container">
        <div className={styles['hero-content']}>
          <div className={styles['hero-text']}>
            <h1 className={styles['hero-title']}>Physical AI & Humanoid Robotics</h1>
            <p className={styles['hero-description']}>
              A comprehensive guide to building intelligent, embodied systems that bridge the gap between
              artificial intelligence and physical reality. Explore the cutting-edge intersection of robotics,
              machine learning, and cognitive science.
            </p>
            <div className={styles['hero-buttons']}>
              <Link
                className={clsx('button button--primary button--lg', styles['hero-button'], 'button-hover')}
                to="/docs/intro"
              >
                Get Started
              </Link>
            </div>
          </div>
          <div className={styles['hero-image']}>
            <img
              src={robotImage}
              alt="Physical AI and Humanoid Robotics"
              className={styles['hero-img']}
            />
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;