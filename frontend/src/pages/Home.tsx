import React from 'react';
import { motion } from 'framer-motion';
import { FileCheck, FileText, Award } from 'lucide-react';
import FloatingResumes from '../components/FloatingResumes';

const Home: React.FC = () => {
  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.5 }}
      className="container mx-auto px-4 py-16 relative z-10"
    >
      <div className="relative min-h-[calc(100vh-16rem)]">
        <FloatingResumes />
        
        <motion.div 
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.8 }}
          className="max-w-3xl mx-auto text-center pt-16 md:pt-24"
        >
          <h1 className="text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-500 text-transparent bg-clip-text">
            Craft Your Perfect Resume
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 mb-8">
            Get AI-optimized resumes for any job role
          </p>
          
          <motion.div 
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="inline-block"
          >
            <a 
              href="#features" 
              className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 rounded-full font-medium text-lg shadow-lg hover:shadow-xl transition-all duration-300"
            >
              Get Started
            </a>
          </motion.div>
        </motion.div>
        
        <motion.div 
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.8 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-24" 
          id="features"
        >
          <div className="bg-gray-800 bg-opacity-70 p-8 rounded-xl backdrop-blur-sm border border-gray-700">
            <div className="bg-blue-500 bg-opacity-20 p-4 rounded-full w-16 h-16 flex items-center justify-center mb-6">
              <FileCheck className="w-8 h-8 text-blue-400" />
            </div>
            <h3 className="text-xl font-semibold mb-3">AI-Powered Templates</h3>
            <p className="text-gray-400">Our AI analyzes successful resumes to create optimized templates for your specific industry and role.</p>
          </div>
          
          <div className="bg-gray-800 bg-opacity-70 p-8 rounded-xl backdrop-blur-sm border border-gray-700">
            <div className="bg-purple-500 bg-opacity-20 p-4 rounded-full w-16 h-16 flex items-center justify-center mb-6">
              <FileText className="w-8 h-8 text-purple-400" />
            </div>
            <h3 className="text-xl font-semibold mb-3">Custom Formatting</h3>
            <p className="text-gray-400">Customize colors, fonts, and layouts to match your personal style while maintaining professional standards.</p>
          </div>
          
          <div className="bg-gray-800 bg-opacity-70 p-8 rounded-xl backdrop-blur-sm border border-gray-700">
            <div className="bg-pink-500 bg-opacity-20 p-4 rounded-full w-16 h-16 flex items-center justify-center mb-6">
              <Award className="w-8 h-8 text-pink-400" />
            </div>
            <h3 className="text-xl font-semibold mb-3">ATS Optimization</h3>
            <p className="text-gray-400">Get your resume past applicant tracking systems with our keyword optimization technology.</p>
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default Home;