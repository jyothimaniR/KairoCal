import { Navigate } from 'react-router-dom';
import { isAuthenticated } from '../../services/authService';

const ProtectedRoute = ({ children }) => {
  console.log('ProtectedRoute: Auth check =', isAuthenticated());
  
  if (!isAuthenticated()) {
    console.log('ProtectedRoute: User not authenticated, redirecting to home');
    return <Navigate to="/" replace />;
  }

  console.log('ProtectedRoute: User authenticated, rendering protected content');
  return children;
};

export default ProtectedRoute;