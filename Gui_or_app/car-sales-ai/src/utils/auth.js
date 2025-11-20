// src/utils/auth.js

/**
 * Clear all authentication data from localStorage
 */
export const clearAuthData = () => {
  // Remove auth tokens
  localStorage.removeItem('authToken');
  localStorage.removeItem('refreshToken');
  localStorage.removeItem('isAuthenticated');
  
  // Remove user data
  localStorage.removeItem('userName');
  localStorage.removeItem('userEmail');
  localStorage.removeItem('userCompany');
  localStorage.removeItem('userId');
  
  // Optional: Keep theme and language preferences
  // localStorage.removeItem('theme');
  // localStorage.removeItem('language');
};

/**
 * Check if user is authenticated
 */
export const isAuthenticated = () => {
  return localStorage.getItem('isAuthenticated') === 'true';
};

/**
 * Get current user data
 */
export const getCurrentUser = () => {
  if (!isAuthenticated()) return null;
  
  return {
    name: localStorage.getItem('userName'),
    email: localStorage.getItem('userEmail'),
    company: localStorage.getItem('userCompany'),
    id: localStorage.getItem('userId'),
  };
};

/**
 * Save user session
 */
export const saveUserSession = (userData) => {
  localStorage.setItem('isAuthenticated', 'true');
  localStorage.setItem('userName', userData.name || userData.email?.split('@')[0] || 'User');
  localStorage.setItem('userEmail', userData.email);
  if (userData.company) localStorage.setItem('userCompany', userData.company);
  if (userData.id) localStorage.setItem('userId', userData.id);
  if (userData.token) localStorage.setItem('authToken', userData.token);
};

/**
 * Logout user - Clear data and redirect
 */
export const logoutUser = (navigate, showToast) => {
  // Clear all auth data
  clearAuthData();
  
  // Show success message if toast function provided
  if (showToast) {
    showToast('Logged out successfully', 'success');
  }
  
  // Redirect to signin page
  if (navigate) {
    navigate('/signin', { replace: true });
  } else {
    window.location.href = '/signin';
  }
};

/**
 * Logout with API call (for production)
 */
export const logoutUserWithAPI = async (navigate, showToast) => {
  try {
    // In production, call logout API endpoint
    // await api.post('/auth/logout');
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 300));
    
    // Clear local data
    clearAuthData();
    
    // Show success message
    if (showToast) {
      showToast('Logged out successfully', 'success');
    }
    
    // Redirect
    if (navigate) {
      navigate('/signin', { replace: true });
    } else {
      window.location.href = '/signin';
    }
  } catch (error) {
    console.error('Logout error:', error);
    
    // Even if API fails, clear local data
    clearAuthData();
    
    if (showToast) {
      showToast('Logged out (with errors)', 'warning');
    }
    
    // Force redirect
    window.location.href = '/signin';
  }
};

/**
 * Auto-logout on token expiration
 */
export const setupAutoLogout = (navigate, showToast) => {
  // Check token expiration every minute
  const checkInterval = setInterval(() => {
    const token = localStorage.getItem('authToken');
    const tokenExpiry = localStorage.getItem('tokenExpiry');
    
    if (!token || !isAuthenticated()) {
      clearInterval(checkInterval);
      return;
    }
    
    // Check if token expired
    if (tokenExpiry && Date.now() > parseInt(tokenExpiry)) {
      clearInterval(checkInterval);
      clearAuthData();
      
      if (showToast) {
        showToast('Session expired. Please login again.', 'warning');
      }
      
      if (navigate) {
        navigate('/signin', { replace: true });
      } else {
        window.location.href = '/signin';
      }
    }
  }, 60000); // Check every minute
  
  return () => clearInterval(checkInterval);
};

/**
 * Logout from all devices (requires backend support)
 */
export const logoutAllDevices = async (navigate, showToast) => {
  try {
    // In production, call API to invalidate all tokens
    // await api.post('/auth/logout-all');
    
    await new Promise(resolve => setTimeout(resolve, 500));
    
    clearAuthData();
    
    if (showToast) {
      showToast('Logged out from all devices', 'success');
    }
    
    if (navigate) {
      navigate('/signin', { replace: true });
    }
  } catch (error) {
    console.error('Logout all devices error:', error);
    if (showToast) {
      showToast('Failed to logout from all devices', 'error');
    }
  }
};