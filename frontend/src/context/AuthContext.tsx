import React, { createContext, useCallback, useEffect, useState } from 'react';
import { loginUser, logoutUser, registerUser } from '../services/authService';
import { LoginCredentials, RegisterCredentials, User } from '../types';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  register: (credentials: RegisterCredentials) => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const storedToken = localStorage.getItem('agripredict_token');
    const storedUser = localStorage.getItem('agripredict_user');
    if (storedToken && storedUser) {
      try {
        setToken(storedToken);
        setUser(JSON.parse(storedUser));
      } catch {
        localStorage.removeItem('agripredict_token');
        localStorage.removeItem('agripredict_user');
      }
    }
    setIsLoading(false);
  }, []);

  const login = useCallback(async (credentials: LoginCredentials) => {
    setIsLoading(true);
    try {
      const data = await loginUser(credentials);
      setUser(data.user);
      setToken(data.token);
      localStorage.setItem('agripredict_token', data.token);
      localStorage.setItem('agripredict_user', JSON.stringify(data.user));
    } finally {
      setIsLoading(false);
    }
  }, []);

  const register = useCallback(async (credentials: RegisterCredentials) => {
    setIsLoading(true);
    try {
      const data = await registerUser(credentials);
      setUser(data.user);
      setToken(data.token);
      localStorage.setItem('agripredict_token', data.token);
      localStorage.setItem('agripredict_user', JSON.stringify(data.user));
    } finally {
      setIsLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    logoutUser();
    setUser(null);
    setToken(null);
  }, []);

  return (
    <AuthContext.Provider value={{ user, token, isAuthenticated: !!token, isLoading, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
};
