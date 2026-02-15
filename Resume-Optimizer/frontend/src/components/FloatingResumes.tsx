import React from 'react';
import { motion } from 'framer-motion';

const FloatingResumes: React.FC = () => {
  // Resume images
  const resumeImages = [
    'https://images.pexels.com/photos/590016/pexels-photo-590016.jpeg?auto=compress&cs=tinysrgb&w=600',
    'https://images.pexels.com/photos/590022/pexels-photo-590022.jpeg?auto=compress&cs=tinysrgb&w=600',
    'https://images.pexels.com/photos/5673488/pexels-photo-5673488.jpeg?auto=compress&cs=tinysrgb&w=600',
  ];

  const getRandomPosition = () => {
    return {
      x: Math.random() * 80 - 40,
      y: Math.random() * 80 - 40,
      rotate: Math.random() * 20 - 10,
    };
  };

  const getRandomDuration = () => {
    return 20 + Math.random() * 10;
  };

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none z-0">
      {resumeImages.map((img, index) => (
        <motion.div
          key={index}
          className="absolute opacity-20 rounded-lg shadow-xl overflow-hidden"
          style={{
            width: '300px',
            height: '400px',
            top: `${20 + index * 25}%`,
            left: `${10 + index * 30}%`,
          }}
          initial={getRandomPosition()}
          animate={{
            ...getRandomPosition(),
            transition: {
              duration: getRandomDuration(),
              repeat: Infinity,
              repeatType: 'reverse',
              ease: 'easeInOut',
            },
          }}
        >
          <img
            src={img}
            alt="Resume template"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-blue-500/30 to-purple-500/30" />
        </motion.div>
      ))}
    </div>
  );
};

export default FloatingResumes;