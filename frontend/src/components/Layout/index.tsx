import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import Navbar from './Navbar';
import Sidebar from './Sidebar';
import styles from './Layout.module.css';

const PAGE_TITLES: Record<string, string> = {
  '/': 'Dashboard',
  '/predictions': 'Price Predictions',
  '/recommendations': 'Crop Recommendations',
  '/alerts': 'Alerts & Notifications',
  '/profile': 'My Profile',
};

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();
  const pageTitle = PAGE_TITLES[location.pathname] || 'AgripredictAI';

  return (
    <div className={styles.layout}>
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className={styles.main}>
        <Navbar
          pageTitle={pageTitle}
          onMenuToggle={() => setSidebarOpen(true)}
          alertCount={3}
        />
        <main className={`${styles.content} scrollbar-thin`}>
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;
