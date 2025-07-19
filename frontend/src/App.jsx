import React, { useEffect } from "react";
import { Routes, Route, useNavigate, useLocation } from "react-router-dom";
import { handleAuthRedirect, isAuthenticated, login } from "./services/authService";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import Dashboard from "./pages/Dashboard";

const App = () => {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    // Handles Cognito redirect after login
    handleAuthRedirect().then(() => {
      if (isAuthenticated()) {
        // Always land on /dashboard after login, unless already there
        if (location.pathname !== "/dashboard") {
          navigate("/dashboard", { replace: true });
        }
      }
    });
    // eslint-disable-next-line
  }, []);

  return (
    <Routes>
      <Route
        path="/"
        element={
          <div className="text-center mt-10">
            <h2 className="text-2xl font-bold mb-4">🚀 KairoCal Frontend is Live!</h2>
            <button
              onClick={login}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Login with Cognito
            </button>
          </div>
        }
      />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
};

export default App;
