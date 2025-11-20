/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#2C3E50',
          light: '#34495E',
          dark: '#1A252F',
        },
        secondary: {
          DEFAULT: '#3498DB',
          light: '#5DADE2',
          dark: '#2980B9',
        },
        success: {
          DEFAULT: '#27AE60',
          light: '#2ECC71',
          dark: '#229954',
        },
        warning: {
          DEFAULT: '#F39C12',
          light: '#F5B041',
          dark: '#D68910',
        },
        danger: {
          DEFAULT: '#E74C3C',
          light: '#EC7063',
          dark: '#C0392B',
        },
        gray: {
          50: '#F8F9FA',
          100: '#ECF0F1',
          200: '#BDC3C7',
          300: '#95A5A6',
          400: '#7F8C8D',
          500: '#34495E',
        },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
        mono: ['Roboto Mono', 'Courier New', 'monospace'],
      },
      fontSize: {
        'xs': '0.75rem',    // 12px
        'sm': '0.875rem',   // 14px
        'base': '1rem',     // 16px
        'lg': '1.125rem',   // 18px
        'xl': '1.25rem',    // 20px
        '2xl': '1.5rem',    // 24px
        '3xl': '1.75rem',   // 28px
        '4xl': '2.25rem',   // 36px
      },
      spacing: {
        '128': '32rem',
        '144': '36rem',
      },
      borderRadius: {
        'sm': '4px',
        'md': '8px',
        'lg': '12px',
      },
      boxShadow: {
        'sm': '0 1px 3px rgba(0,0,0,0.12)',
        'md': '0 4px 6px rgba(0,0,0,0.1)',
        'lg': '0 10px 24px rgba(0,0,0,0.15)',
      },
      animation: {
        'fade-in': 'fadeIn 0.25s ease-in-out',
        'slide-in': 'slideIn 0.3s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideIn: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}