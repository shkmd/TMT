/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Dark theme colors matching mockup
        dark: {
          bg: '#0a0e1a',
          surface: '#0f1419',
          card: '#151b26',
          hover: '#1a2130',
          border: '#1e2937',
        },
        // Teal/green accent colors
        primary: {
          50: '#f0fdfa',
          100: '#ccfbf1',
          200: '#99f6e4',
          300: '#5eead4',
          400: '#2dd4bf',
          500: '#14b8a6',
          600: '#0d9488',
          700: '#0f766e',
          800: '#115e59',
          900: '#134e4a',
        },
        // Success/profit green
        success: {
          500: '#10b981',
          600: '#059669',
        },
        // Danger/loss red
        danger: {
          500: '#ef4444',
          600: '#dc2626',
        },
      },
      backgroundColor: {
        'dark-gradient': 'linear-gradient(135deg, #0a0e1a 0%, #0f1419 100%)',
      },
    },
  },
  plugins: [],
}
