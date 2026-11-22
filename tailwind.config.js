/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/js/**/*.js",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        // Rosa magenta del logo Brillo Rosa (600 = color del texto del logo)
        brand: {
          50:  '#fff1f7',
          100: '#ffe4f0',
          200: '#fecae2',
          300: '#fd9fca',
          400: '#fb68a9',
          500: '#f0308a',
          600: '#e0006a',
          700: '#bc0058',
          800: '#9a0549',
          900: '#800a40',
          950: '#4d0022',
        },
        // Neutros (usados en el panel admin)
        surface: {
          0:   '#ffffff',
          50:  '#faf8f9',
          100: '#f3eff1',
          200: '#e7e1e4',
          300: '#d3cacf',
          400: '#a89ca3',
          500: '#7d7178',
          600: '#5f545a',
          700: '#4a4046',
          800: '#332b30',
          900: '#211b1f',
          950: '#140f12',
        },
        // Ciruela profunda: texto principal en lugar de negro
        ink: {
          50:  '#fbf5f8',
          100: '#f4e8ee',
          200: '#e6cfdb',
          300: '#c7a9b8',
          400: '#a5828f',
          500: '#8e6278',
          600: '#74485f',
          700: '#5b2a44',
          800: '#431a31',
          900: '#2e0a1f',
          950: '#1d0413',
        },
        milk:  '#fff7fa',
        blush: '#fce8f0',
        bubble: '#ff8cc6',
      },
      fontFamily: {
        sans: ['Figtree', 'system-ui', '-apple-system', 'sans-serif'],
        display: ['Fraunces', 'Georgia', 'serif'],
      },
      fontSize: {
        'hero': ['clamp(3rem, 6.2vw + 1rem, 6.75rem)', { lineHeight: '0.95', letterSpacing: '-0.035em' }],
      },
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.75rem',
      },
      boxShadow: {
        'soft': '0 1px 2px rgba(46,10,31,0.04), 0 2px 8px -2px rgba(46,10,31,0.06)',
        'card': '0 1px 3px rgba(46,10,31,0.05), 0 8px 24px -8px rgba(46,10,31,0.08)',
        'card-hover': '0 12px 32px -12px rgba(224,0,106,0.25)',
        'elevated': '0 10px 40px -12px rgba(46,10,31,0.18)',
        'float': '0 30px 80px -20px rgba(46,10,31,0.35)',
        'gloss': '0 18px 40px -16px rgba(224,0,106,0.55)',
      },
      transitionTimingFunction: {
        'silk': 'cubic-bezier(0.22, 1, 0.36, 1)',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out forwards',
        'slide-up': 'slideUp 0.5s cubic-bezier(0.22,1,0.36,1) forwards',
        'shimmer': 'shimmer 2s linear infinite',
        'marquee': 'marquee 38s linear infinite',
        'twinkle': 'twinkle 3.2s ease-in-out infinite',
      },
      keyframes: {
        fadeIn:    { '0%': { opacity: '0' }, '100%': { opacity: '1' } },
        slideUp:   { '0%': { opacity: '0', transform: 'translateY(20px)' }, '100%': { opacity: '1', transform: 'translateY(0)' } },
        shimmer:   { '0%': { backgroundPosition: '-200% 0' }, '100%': { backgroundPosition: '200% 0' } },
        marquee:   { '0%': { transform: 'translateX(0)' }, '100%': { transform: 'translateX(-50%)' } },
        twinkle:   { '0%, 100%': { opacity: '1', transform: 'scale(1) rotate(0deg)' }, '50%': { opacity: '.35', transform: 'scale(.6) rotate(20deg)' } },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
      },
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
}
