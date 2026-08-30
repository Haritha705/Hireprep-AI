'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { getMe, signUpUser, loginUser } from '@/lib/api';

interface User {
  id: string;
  full_name: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (data: { email: string; password: string }) => Promise<void>;
  signup: (data: { full_name: string; email: string; password: string }) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const savedToken = localStorage.getItem('hireprep_token');
    if (savedToken) {
      setToken(savedToken);
      getMe()
        .then((res) => {
          setUser(res.data.user);
        })
        .catch(() => {
          localStorage.removeItem('hireprep_token');
          setToken(null);
          setUser(null);
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (data: { email: string; password: string }) => {
    const res = await loginUser(data);
    const newToken = res.data.access_token;
    const userData = res.data.user;
    localStorage.setItem('hireprep_token', newToken);
    setToken(newToken);
    setUser(userData);
  };

  const signup = async (data: { full_name: string; email: string; password: string }) => {
    const res = await signUpUser(data);
    const newToken = res.data.access_token;
    const userData = res.data.user;
    localStorage.setItem('hireprep_token', newToken);
    setToken(newToken);
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem('hireprep_token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
