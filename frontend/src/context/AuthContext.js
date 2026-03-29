import React, { createContext, useContext, useState, useCallback } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem('token'));
  const [user, setUser] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('user'));
    } catch {
      return null;
    }
  });

  // Full farmer profile (includes district, local_area, notification prefs)
  const [userProfile, setUserProfile] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('userProfile')) || null;
    } catch {
      return null;
    }
  });

  // Sidebar collapsed state – persisted in localStorage
  const [sidebarCollapsed, setSidebarCollapsed] = useState(() => {
    return localStorage.getItem('sidebarCollapsed') === 'true';
  });

  const login = useCallback((newToken, userData) => {
    try {
      localStorage.setItem('token', newToken);
      if (userData) localStorage.setItem('user', JSON.stringify(userData));
    } catch { /* quota exceeded */ }
    setToken(newToken);
    setUser(userData);
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('userProfile');
    setToken(null);
    setUser(null);
    setUserProfile(null);
  }, []);

  const updateUser = useCallback((userData) => {
    try { localStorage.setItem('user', JSON.stringify(userData)); } catch { /* quota exceeded */ }
    setUser(userData);
  }, []);

  const saveUserProfile = useCallback((profileData) => {
    try { localStorage.setItem('userProfile', JSON.stringify(profileData)); } catch { /* quota exceeded */ }
    setUserProfile(profileData);
  }, []);

  const toggleSidebar = useCallback(() => {
    setSidebarCollapsed((prev) => {
      const next = !prev;
      localStorage.setItem('sidebarCollapsed', String(next));
      return next;
    });
  }, []);

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        userProfile,
        isAuthenticated: !!token,
        login,
        logout,
        updateUser,
        saveUserProfile,
        sidebarCollapsed,
        toggleSidebar,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}

export default AuthContext;
