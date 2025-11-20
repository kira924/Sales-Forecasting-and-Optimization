import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ToastProvider } from './components/common/Toast';
import Header from './components/common/Header';
import Footer from './components/common/Footer';
import SignIn from './components/auth/SignIn';
import SignUp from './components/auth/SignUp';
import HomePage from './components/home/HomePage';
import SalesForecastPage from './components/forecast/SalesForecastPage';
import PriorityRankingPage from './components/ranking/PriorityRankingPage';
import Settings from './components/settings/Settings';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
  
  if (!isAuthenticated) {
    return <Navigate to="/signin" replace />;
  }
  
  return children;
};

// Layout Component
const Layout = ({ children }) => {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <main className="flex-1">
        {children}
      </main>
      <Footer />
    </div>
  );
};

function App() {
  return (
    <ToastProvider>
      <Router>
        <Routes>
          {/* Auth Routes (No Layout) */}
          <Route path="/signin" element={<SignIn />} />
          <Route path="/signup" element={<SignUp />} />

          {/* Protected Routes (With Layout) */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Layout>
                  <HomePage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/sales-forecast"
            element={
              <ProtectedRoute>
                <Layout>
                  <SalesForecastPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/priority-ranking"
            element={
              <ProtectedRoute>
                <Layout>
                  <PriorityRankingPage />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* Catch all - redirect to home */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </ToastProvider>
  );
}

export default App;