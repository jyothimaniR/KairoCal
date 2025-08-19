import React, { createContext, useContext, useEffect, useState } from 'react';
import type { ReactNode } from 'react';
import type { User } from 'firebase/auth';
import { useAuthState } from 'react-firebase-hooks/auth';
import { auth } from '../lib/firebase';

interface AuthContextType {
  user: User | null | undefined;
  loading: boolean;
  error: Error | undefined;
  isDemoMode: boolean;
  demoUser: {
    email: string;
    sub: string;
  } | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, loading, error] = useAuthState(auth);
  const [isDemoMode, setIsDemoMode] = useState(false);
  const [demoUser, setDemoUser] = useState<{ email: string; sub: string } | null>(null);

  // Check for demo mode on mount and storage changes
  useEffect(() => {
    const checkDemoMode = () => {
      const demoMode = localStorage.getItem('demoMode') === 'true';
      const userEmail = localStorage.getItem('userEmail');
      const userCognitoSub = localStorage.getItem('userCognitoSub');
      
      if (demoMode && userEmail && userCognitoSub) {
        setIsDemoMode(true);
        setDemoUser({
          email: userEmail,
          sub: userCognitoSub
        });
      } else {
        setIsDemoMode(false);
        setDemoUser(null);
      }
    };

    checkDemoMode();

    // Listen for storage changes (in case demo mode is set from another tab/component)
    const handleStorageChange = () => {
      checkDemoMode();
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  const value = {
    user: isDemoMode ? ({
      email: demoUser?.email,
      uid: demoUser?.sub
    } as User) : user,
    loading: isDemoMode ? false : loading,
    error: isDemoMode ? undefined : error,
    isDemoMode,
    demoUser
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
