import { login, logout, isAuthenticated } from '../services/authService';

const useAuth = () => {
  return {
    login,
    logout,
    isAuthenticated
  };
};

export default useAuth;
