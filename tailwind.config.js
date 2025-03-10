/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}",
            "./circuitos/templates/**/*.{html,js}",
            "./cartas/templates/**/*.{html,js}",
            "./cmain/templates/**/*.{html,js}",
            "./foe/templates/**/*.{html,js}",
            "./node_modules/flowbite/**/*.js"
  ],
  theme: {
        colors: {
          'ipt-main': '#00AAF8',
          'ip-main': '#1E9D8B',
          'ipe-main': '#698392',
          'ipp-main': '#7F3B3A',
          'gil-main': '#CF7600',

        },
      }
    ,
  
  plugins: [
    require("@tailwindcss/forms"), 
    require("@tailwindcss/typography"),
    require('flowbite/plugin'),
   ],
}
