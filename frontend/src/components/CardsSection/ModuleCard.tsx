import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import styles from './ModuleCard.module.css'; // Import CSS module
import { IconType } from 'react-icons';

interface ModuleCardProps {
  title: string;
  description: string;
  image?: string;
  icon?: IconType;
  link?: string;
}

const ModuleCard: React.FC<ModuleCardProps> = ({ title, description, image, icon: Icon, link }) => {
  const cardContent = (
    <div className={clsx(styles['card'], styles['card-hover'], styles['hover-scale'])}>
      <div className={styles['card-content']}>
        {Icon ? (
          <div className={styles['icon-content-layout']}>
            <div className={styles['card-icon']}>
              <Icon size={64} />
            </div>
            <div className={styles['text-content']}>
              <h3 className={styles['card-title']}>{title}</h3>
              <p className={styles['card-description']}>{description}</p>
            </div>
          </div>
        ) : image ? (
          <div className={styles['card-image']}>
            <img
              src={image}
              alt={title}
              className={styles['card-img']}
            />
          </div>
        ) : null}
        {!Icon && !image && (
          <>
            <h3 className={styles['card-title']}>{title}</h3>
            <p className={styles['card-description']}>{description}</p>
          </>
        )}
      </div>
    </div>
  );

  return link ? (
    <Link to={link} className={styles['card-link']}>
      {cardContent}
    </Link>
  ) : (
    <div className={styles['card-wrapper']}>
      {cardContent}
    </div>
  );
};

export default ModuleCard;