import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { DashboardProvider } from './context/DashboardContext';
import Layout from './components/Layout';
import ErrorBoundary from './components/Common/ErrorBoundary';
import Dashboard from './pages/Dashboard';
import Predictions from './pages/Predictions';
import Recommendations from './pages/Recommendations';
import Alerts from './pages/Alerts';
import Profile from './pages/Profile';

const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <AuthProvider>
          <DashboardProvider>
            <Layout>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/predictions" element={<Predictions />} />
                <Route path="/recommendations" element={<Recommendations />} />
                <Route path="/alerts" element={<Alerts />} />
                <Route path="/profile" element={<Profile />} />
              </Routes>
            </Layout>
          </DashboardProvider>
        </AuthProvider>
      </BrowserRouter>
    </ErrorBoundary>
  );
};

export default App;
