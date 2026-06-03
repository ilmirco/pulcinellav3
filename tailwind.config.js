/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*.html", "./*.js"],
  theme: {
    extend: {
      colors: {
        brand: {
          green: '#1A6B2A',
          red: '#CC1515',
          black: '#111111',
          light: '#FAFAF5',
          gray: '#333333'
        }
      },
      fontFamily: {
        heading: ['"Playfair Display"', 'serif'],
        body: ['Lato', 'sans-serif'],
      }
    }
  },
  plugins: [],
}
