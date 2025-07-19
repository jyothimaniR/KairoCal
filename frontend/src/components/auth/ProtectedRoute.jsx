import { Navigate } from 'react-router-dom';
import { isAuthenticated } from '../../services/authService';

const ProtectedRoute = ({ children }) => {
  // Only check local session storage, not Cognito SSO
  if (!isAuthenticated()) {
    return <Navigate to="/" replace />;
  }

  return children;
};

export default ProtectedRoute;