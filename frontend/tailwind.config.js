/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#18A058',
          hover: '#36B37E',
          light: '#E8F7EF',
        },
        bg: '#F7F8FA',
        card: '#FFFFFF',
        title: '#1F2329',
        body: '#4E5969',
        muted: '#86909C',
        border: '#E5E6EB',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      boxShadow: {
        card: '0 1px 3px 0 rgba(0,0,0,0.06), 0 1px 2px -1px rgba(0,0,0,0.04)',
        'card-hover': '0 4px 12px 0 rgba(0,0,0,0.08), 0 2px 4px -1px rgba(0,0,0,0.04)',
        'card-lg': '0 8px 24px 0 rgba(0,0,0,0.08)',
      },
      borderRadius: {
        xl: '12px',
        '2xl': '16px',
      },
      typography: (theme) => ({
        DEFAULT: {
          css: {
            color: theme('colors.body'),
            maxWidth: 'none',
            a: { color: theme('colors.primary.DEFAULT'), textDecoration: 'none', '&:hover': { color: theme('colors.primary.hover') } },
            h1: { color: theme('colors.title'), fontWeight: '700' },
            h2: { color: theme('colors.title'), fontWeight: '600' },
            h3: { color: theme('colors.title'), fontWeight: '600' },
            h4: { color: theme('colors.title'), fontWeight: '600' },
            code: { color: '#18A058', backgroundColor: '#E8F7EF', padding: '2px 6px', borderRadius: '4px', fontWeight: '500', '&::before': { content: '""' }, '&::after': { content: '""' } },
            pre: { backgroundColor: '#1e1e1e', color: '#d4d4d4', borderRadius: '12px', padding: '1.25rem 1.5rem' },
            'pre code': { backgroundColor: 'transparent', color: 'inherit', padding: '0', borderRadius: '0' },
            blockquote: { borderLeftColor: theme('colors.primary.DEFAULT'), color: theme('colors.body'), fontStyle: 'normal', backgroundColor: '#F0FFF4', padding: '0.75rem 1rem', borderRadius: '0 8px 8px 0' },
            'blockquote p:first-of-type::before': { content: '""' },
            'blockquote p:last-of-type::after': { content: '""' },
            hr: { borderColor: theme('colors.border') },
            'ul > li::marker': { color: theme('colors.primary.DEFAULT') },
            'ol > li::marker': { color: theme('colors.primary.DEFAULT') },
            table: { fontSize: '0.875rem' },
            thead: { borderBottomColor: theme('colors.border') },
            'thead th': { color: theme('colors.title'), fontWeight: '600' },
            'tbody tr': { borderBottomColor: theme('colors.border') },
          },
        },
      }),
    },
  },
  plugins: [require('@tailwindcss/typography')],
}
