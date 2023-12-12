/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./dist/**/*.{html,js}"],
  theme: {
    extend: {
      colors:{
        'red':'#923D41',
        'black': '#011936',
        'white': '#FFFCFF',
        'delete': '#E82727'
      },
    },
  },
  plugins: [],
}

