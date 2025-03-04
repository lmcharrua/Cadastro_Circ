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

        },
      }
    ,
  
  plugins: [
    require("@tailwindcss/forms"), 
    require("@tailwindcss/typography"),
   ],
}
