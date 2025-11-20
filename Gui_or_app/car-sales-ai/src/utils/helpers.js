
// 1. Generate a unique ID
export const generateId = () => {
  return '_' + Math.random().toString(36).substr(2, 9);
};

// 2. Format number as currency
export const formatCurrency = (value, currency = 'USD') => {
  try {
    if (!currency || typeof currency !== "string" || currency.length !== 3) {
      currency = "USD"; // fallback currency
    }

    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency
    }).format(Number(value) || 0);

  } catch (err) {
    return value; // fallback if formatter fails
  }
};


// 3. Format number as percentage
export const formatPercentage = (value, decimals = 2) => {
  if (isNaN(value)) return value;
  return `${(value).toFixed(decimals)}%`;
};

// 4. Calculate growth between two numbers
export const calculateGrowth = (current, previous) => {
  if (isNaN(current) || isNaN(previous) || previous === 0) return null;
  return ((current - previous) / previous);
};

// 5. Validate email format
export const isValidEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(String(email).toLowerCase());
};

// 6. Get password strength
export const getPasswordStrength = (password) => {
  let score = 0;
  if (!password) return score;

  // length
  if (password.length >= 8) score++;
  if (password.length >= 12) score++;

  // lowercase & uppercase
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) score++;

  // numbers
  if (/\d/.test(password)) score++;

  // special characters
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score++;

  // Return strength label
  if (score <= 2) return 'Weak';
  if (score <= 4) return 'Medium';
  return 'Strong';
};
