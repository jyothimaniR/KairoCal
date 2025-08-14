import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/layout/Layout'
import LandingPage from './pages/landing/LandingPage'
import AuthPage from './pages/auth/AuthPage'
import DashboardPage from './pages/dashboard/DashboardPage'
import DebugDashboard from './pages/debug/DebugDashboard'
import SearchPage from './pages/search/SearchPage'
import './App.css'

function App() {
  console.log('🚀 App component rendering');
  
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/auth" element={<AuthPage />} />
        <Route path="/debug" element={<DebugDashboard />} />
        <Route path="/dashboard" element={
          <Layout>
            <DashboardPage />
          </Layout>
        } />
        <Route path="/search" element={
          <Layout>
            <SearchPage />
          </Layout>
        } />
        <Route path="/app" element={<Navigate to="/debug" replace />} />
      </Routes>
    </Router>
  )
}

export default App
