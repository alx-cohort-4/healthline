/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}", 
  ],
  theme: {
    extend: {
      colors: {
        'text-primary': '#000000DE',
        'text-secondary': '#00000099',
        'content-brand': '#175CD3',
        'background-hover': '#F2F2F2',
        'content-tertiary-inverse': '#B2B2B2',
        'content-secondary': '#333333',
      },
      fontSize: {
        base: '1rem',
        sm: '0.875rem',
        lg: '1.5rem',
      },
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
