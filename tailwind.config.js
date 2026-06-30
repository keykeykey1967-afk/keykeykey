/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // 報徳学園スクールカラー（深紺）で blue を上書き
        blue: {
          50:  '#edf0f9',
          100: '#d2d8f0',
          200: '#a5b1e1',
          300: '#788bd2',
          400: '#4b64c3',
          500: '#2540b4',
          600: '#1c328e',
          700: '#162771',
          800: '#101c54',  // 紺色メイン（ナビ・ヒーロー）
          900: '#0b1239',
        },
        gold: {
          300: '#e8d48a',
          400: '#dcc06a',
          500: '#c9a84c',  // 金色アクセント
          600: '#b0912e',
        },
      },
    },
  },
  plugins: [],
}
