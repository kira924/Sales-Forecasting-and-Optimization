// src/components/settings/Settings.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  User, 
  Mail, 
  Building, 
  Lock, 
  Bell, 
  Palette, 
  Globe, 
  Shield,
  Trash2,
  Eye,
  EyeOff,
  Check,
  X,
  AlertTriangle
} from 'lucide-react';
import Button from '../common/Button';
import Card from '../common/Card';
import { useToast } from '../common/Toast';

const Settings = () => {
  const navigate = useNavigate();
  const { success, error, warning } = useToast();
  
  // Get user data from localStorage
  const [userData, setUserData] = useState({
    name: localStorage.getItem('userName') || 'User',
    email: localStorage.getItem('userEmail') || 'user@example.com',
    company: localStorage.getItem('userCompany') || '',
  });

  // Profile form state
  const [profileData, setProfileData] = useState(userData);
  const [profileLoading, setProfileLoading] = useState(false);

  // Password form state
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });
  const [showPasswords, setShowPasswords] = useState({
    current: false,
    new: false,
    confirm: false,
  });
  const [passwordLoading, setPasswordLoading] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState(0);

  // Appearance state
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'light');
  const [language, setLanguage] = useState(localStorage.getItem('language') || 'en');

  // Notifications state
  const [notifications, setNotifications] = useState({
    emailNotifications: localStorage.getItem('emailNotifications') !== 'false',
    weeklySummary: localStorage.getItem('weeklySummary') !== 'false',
    dailyReports: localStorage.getItem('dailyReports') === 'true',
  });

  // Delete account modal
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deleteConfirmation, setDeleteConfirmation] = useState('');

  // Calculate password strength
  useEffect(() => {
    const password = passwordData.newPassword;
    let strength = 0;
    
    if (password.length >= 8) strength += 25;
    if (password.length >= 12) strength += 25;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength += 25;
    if (/\d/.test(password)) strength += 15;
    if (/[^A-Za-z0-9]/.test(password)) strength += 10;
    
    setPasswordStrength(Math.min(strength, 100));
  }, [passwordData.newPassword]);

  // Handle profile update
  const handleProfileUpdate = async (e) => {
    e.preventDefault();
    setProfileLoading(true);

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Update localStorage
      localStorage.setItem('userName', profileData.name);
      localStorage.setItem('userEmail', profileData.email);
      localStorage.setItem('userCompany', profileData.company);
      
      setUserData(profileData);
      success('Profile updated successfully!');
    } catch (err) {
      error('Failed to update profile. Please try again.');
    } finally {
      setProfileLoading(false);
    }
  };

  // Handle password change
  const handlePasswordChange = async (e) => {
    e.preventDefault();

    // Validation
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      error('New passwords do not match!');
      return;
    }

    if (passwordData.newPassword.length < 8) {
      error('Password must be at least 8 characters long!');
      return;
    }

    if (passwordStrength < 50) {
      warning('Password is weak. Consider using a stronger password.');
      return;
    }

    setPasswordLoading(true);

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      success('Password changed successfully!');
      setPasswordData({
        currentPassword: '',
        newPassword: '',
        confirmPassword: '',
      });
    } catch (err) {
      error('Failed to change password. Please try again.');
    } finally {
      setPasswordLoading(false);
    }
  };

  // Handle theme change
  const handleThemeChange = (newTheme) => {
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    success(`Theme changed to ${newTheme} mode`);
    // In production, apply theme to document
    // document.documentElement.classList.toggle('dark', newTheme === 'dark');
  };

  // Handle notification toggle
  const handleNotificationToggle = (key) => {
    const newValue = !notifications[key];
    setNotifications(prev => ({ ...prev, [key]: newValue }));
    localStorage.setItem(key, newValue.toString());
    success(`${key} ${newValue ? 'enabled' : 'disabled'}`);
  };

  // Handle account deletion
  const handleDeleteAccount = async () => {
    if (deleteConfirmation !== 'DELETE') {
      error('Please type DELETE to confirm');
      return;
    }

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Clear all data
      localStorage.clear();
      success('Account deleted successfully');
      navigate('/signin');
    } catch (err) {
      error('Failed to delete account. Please try again.');
    }
  };

  // Get password strength color
  const getPasswordStrengthColor = () => {
    if (passwordStrength < 30) return 'bg-danger';
    if (passwordStrength < 60) return 'bg-warning';
    return 'bg-success';
  };

  const getPasswordStrengthText = () => {
    if (passwordStrength < 30) return 'Weak';
    if (passwordStrength < 60) return 'Medium';
    return 'Strong';
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-primary">Settings</h1>
          <p className="text-gray-400 mt-2">Manage your account settings and preferences</p>
        </div>

        <div className="space-y-6">
          {/* Profile Settings */}
          <Card>
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-secondary bg-opacity-10 rounded-lg flex items-center justify-center">
                <User className="w-6 h-6 text-secondary" />
              </div>
              <div>
                <h2 className="text-xl font-semibold text-primary">Profile Settings</h2>
                <p className="text-sm text-gray-400">Update your personal information</p>
              </div>
            </div>

            <form onSubmit={handleProfileUpdate} className="space-y-4">
              {/* Name */}
              <div>
                <label className="block text-sm font-medium text-gray-500 mb-2">
                  Full Name
                </label>
                <input
                  type="text"
                  value={profileData.name}
                  onChange={(e) => setProfileData({ ...profileData, name: e.target.value })}
                  className="input-field"
                  placeholder="John Doe"
                />
              </div>

              {/* Email */}
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">
                  Email Address
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="email"
                    value={profileData.email}
                    onChange={(e) => setProfileData({ ...profileData, email: e.target.value })}
                    className="input-field pl-10"
                    placeholder="you@example.com"
                  />
                </div>
              </div>

              {/* Company */}
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">
                  Company Name <span className="text-gray-400">(Optional)</span>
                </label>
                <div className="relative">
                  <Building className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="text"
                    value={profileData.company}
                    onChange={(e) => setProfileData({ ...profileData, company: e.target.value })}
                    className="input-field pl-10"
                    placeholder="ABC Car Dealership"
                  />
                </div>
              </div>

              <Button
                type="submit"
                variant="primary"
                loading={profileLoading}
              >
                Update Profile
              </Button>
            </form>
          </Card>

          {/* Password Change */}
          <Card>
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-warning bg-opacity-10 rounded-lg flex items-center justify-center">
                <Lock className="w-6 h-6 text-warning" />
              </div>
              <div>
                <h2 className="text-xl font-semibold text-primary">Change Password</h2>
                <p className="text-sm text-gray-400">Update your password regularly</p>
              </div>
            </div>

            <form onSubmit={handlePasswordChange} className="space-y-4">
              {/* Current Password */}
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">
                  Current Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type={showPasswords.current ? 'text' : 'password'}
                    value={passwordData.currentPassword}
                    onChange={(e) => setPasswordData({ ...passwordData, currentPassword: e.target.value })}
                    className="input-field pl-10 pr-10"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPasswords({ ...showPasswords, current: !showPasswords.current })}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-primary"
                  >
                    {showPasswords.current ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>

              {/* New Password */}
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">
                  New Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type={showPasswords.new ? 'text' : 'password'}
                    value={passwordData.newPassword}
                    onChange={(e) => setPasswordData({ ...passwordData, newPassword: e.target.value })}
                    className="input-field pl-10 pr-10"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPasswords({ ...showPasswords, new: !showPasswords.new })}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-primary"
                  >
                    {showPasswords.new ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
                
                {/* Password Strength Indicator */}
                {passwordData.newPassword && (
                  <div className="mt-2">
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-gray-400">Password Strength</span>
                      <span className={`font-medium ${
                        passwordStrength < 30 ? 'text-danger' :
                        passwordStrength < 60 ? 'text-warning' : 'text-success'
                      }`}>
                        {getPasswordStrengthText()}
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full transition-all ${getPasswordStrengthColor()}`}
                        style={{ width: `${passwordStrength}%` }}
                      />
                    </div>
                  </div>
                )}
              </div>

              {/* Confirm Password */}
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">
                  Confirm New Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type={showPasswords.confirm ? 'text' : 'password'}
                    value={passwordData.confirmPassword}
                    onChange={(e) => setPasswordData({ ...passwordData, confirmPassword: e.target.value })}
                    className="input-field pl-10 pr-10"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPasswords({ ...showPasswords, confirm: !showPasswords.confirm })}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-primary"
                  >
                    {showPasswords.confirm ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
                
                {/* Match Indicator */}
                {passwordData.confirmPassword && (
                  <div className="mt-2 flex items-center space-x-2">
                    {passwordData.newPassword === passwordData.confirmPassword ? (
                      <>
                        <Check className="w-4 h-4 text-success" />
                        <span className="text-sm text-success">Passwords match</span>
                      </>
                    ) : (
                      <>
                        <X className="w-4 h-4 text-danger" />
                        <span className="text-sm text-danger">Passwords do not match</span>
                      </>
                    )}
                  </div>
                )}
              </div>

              <Button
                type="submit"
                variant="primary"
                loading={passwordLoading}
                disabled={!passwordData.currentPassword || !passwordData.newPassword || !passwordData.confirmPassword}
              >
                Change Password
              </Button>
            </form>
          </Card>

          {/* Appearance */}
          <Card>
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                <Palette className="w-6 h-6 text-purple-600" />
              </div>
              <div>
                <h2 className="text-xl font-semibold text-primary">Appearance</h2>
                <p className="text-sm text-gray-400">Customize your interface</p>
              </div>
            </div>

            <div className="space-y-4">
              {/* Theme */}
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-3">
                  Theme
                </label>
                <div className="grid grid-cols-3 gap-3">
                  {['light', 'dark', 'auto'].map((themeOption) => (
                    <button
                      key={themeOption}
                      onClick={() => handleThemeChange(themeOption)}
                      className={`
                        p-4 rounded-lg border-2 transition-all
                        ${theme === themeOption
                          ? 'border-secondary bg-secondary bg-opacity-10'
                          : 'border-gray-200 hover:border-gray-300'
                        }
                      `}
                    >
                      <div className="text-center">
                        <div className="text-2xl mb-2">
                          {themeOption === 'light' && '☀️'}
                          {themeOption === 'dark' && '🌙'}
                          {themeOption === 'auto' && '⚙️'}
                        </div>
                        <span className="text-sm font-medium text-primary capitalize">
                          {themeOption}
                        </span>
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Language */}
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">
                  Language
                </label>
                <div className="relative">
                  <Globe className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <select
                    value={language}
                    onChange={(e) => {
                      setLanguage(e.target.value);
                      localStorage.setItem('language', e.target.value);
                      success(`Language changed to ${e.target.value === 'en' ? 'English' : 'Arabic'}`);
                    }}
                    className="input-field pl-10"
                  >
                    <option value="en">English</option>
                    <option value="ar">العربية (Arabic)</option>
                  </select>
                </div>
              </div>
            </div>
          </Card>

          {/* Notifications */}
          <Card>
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                <Bell className="w-6 h-6 text-blue-600" />
              </div>
              <div>
                <h2 className="text-xl font-semibold text-primary">Notifications</h2>
                <p className="text-sm text-gray-400">Manage notification preferences</p>
              </div>
            </div>

            <div className="space-y-4">
              {/* Email Notifications */}
              <div className="flex items-center justify-between py-3 border-b border-gray-200">
                <div>
                  <h3 className="text-sm font-medium text-primary">Email Notifications</h3>
                  <p className="text-xs text-gray-400 mt-1">Receive updates about new features</p>
                </div>
                <button
                  onClick={() => handleNotificationToggle('emailNotifications')}
                  className={`
                    relative w-12 h-6 rounded-full transition-colors
                    ${notifications.emailNotifications ? 'bg-success' : 'bg-gray-200'}
                  `}
                >
                  <div
                    className={`
                      absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform
                      ${notifications.emailNotifications ? 'translate-x-6' : 'translate-x-0'}
                    `}
                  />
                </button>
              </div>

              {/* Weekly Summary */}
              <div className="flex items-center justify-between py-3 border-b border-gray-200">
                <div>
                  <h3 className="text-sm font-medium text-primary">Weekly Forecast Summary</h3>
                  <p className="text-xs text-gray-400 mt-1">Get weekly sales forecasts via email</p>
                </div>
                <button
                  onClick={() => handleNotificationToggle('weeklySummary')}
                  className={`
                    relative w-12 h-6 rounded-full transition-colors
                    ${notifications.weeklySummary ? 'bg-success' : 'bg-gray-200'}
                  `}
                >
                  <div
                    className={`
                      absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform
                      ${notifications.weeklySummary ? 'translate-x-6' : 'translate-x-0'}
                    `}
                  />
                </button>
              </div>

              {/* Daily Reports */}
              <div className="flex items-center justify-between py-3">
                <div>
                  <h3 className="text-sm font-medium text-primary">Daily Profit Reports</h3>
                  <p className="text-xs text-gray-400 mt-1">Daily updates on car rankings</p>
                </div>
                <button
                  onClick={() => handleNotificationToggle('dailyReports')}
                  className={`
                    relative w-12 h-6 rounded-full transition-colors
                    ${notifications.dailyReports ? 'bg-success' : 'bg-gray-200'}
                  `}
                >
                  <div
                    className={`
                      absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform
                      ${notifications.dailyReports ? 'translate-x-6' : 'translate-x-0'}
                    `}
                  />
                </button>
              </div>
            </div>
          </Card>

          {/* Privacy & Security */}
          <Card>
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-danger bg-opacity-10 rounded-lg flex items-center justify-center">
                <Shield className="w-6 h-6 text-danger" />
              </div>
              <div>
                <h2 className="text-xl font-semibold text-primary">Privacy & Security</h2>
                <p className="text-sm text-gray-400">Manage your account security</p>
              </div>
            </div>

            <div className="space-y-3">
              <Button
                variant="secondary"
                fullWidth
                onClick={() => warning('Two-factor authentication coming soon!')}
              >
                <Lock className="w-4 h-4 mr-2" />
                Enable Two-Factor Authentication
              </Button>

              <Button
                variant="secondary"
                fullWidth
                onClick={() => success('Data download will be sent to your email')}
              >
                Download My Data
              </Button>

              <Button
                variant="danger"
                fullWidth
                onClick={() => setShowDeleteModal(true)}
              >
                <Trash2 className="w-4 h-4 mr-2" />
                Delete Account
              </Button>
            </div>
          </Card>
        </div>
      </div>

      {/* Delete Account Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6 animate-fade-in">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-12 h-12 bg-danger bg-opacity-10 rounded-full flex items-center justify-center">
                <AlertTriangle className="w-6 h-6 text-danger" />
              </div>
              <div>
                <h3 className="text-xl font-bold text-primary">Delete Account</h3>
                <p className="text-sm text-gray-400">This action cannot be undone</p>
              </div>
            </div>

            <div className="mb-6">
              <p className="text-gray-500 mb-4">
                Are you sure you want to delete your account? All your data will be permanently removed.
              </p>
              <p className="text-sm text-danger mb-4">
                Type <strong>DELETE</strong> to confirm:
              </p>
              <input
                type="text"
                value={deleteConfirmation}
                onChange={(e) => setDeleteConfirmation(e.target.value)}
                className="input-field"
                placeholder="Type DELETE"
              />
            </div>

            <div className="flex space-x-3">
              <Button
                variant="secondary"
                fullWidth
                onClick={() => {
                  setShowDeleteModal(false);
                  setDeleteConfirmation('');
                }}
              >
                Cancel
              </Button>
              <Button
                variant="danger"
                fullWidth
                onClick={handleDeleteAccount}
                disabled={deleteConfirmation !== 'DELETE'}
              >
                Delete Account
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Settings;