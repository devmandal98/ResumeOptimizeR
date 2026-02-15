import React from 'react';
import { Outlet } from 'react-router-dom';

import Navigation from './Navigation';

const Layout: React.FC = () => {
  return (
    <>
   
      <Navigation />
      
      <main className="pt-16 md:pt-20">
      
        <Outlet />
      </main>
    </>
  );
};

export default Layout;