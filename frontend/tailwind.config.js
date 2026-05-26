export default {
  content: ["./index.html", "./src/**/*.{jsx,js}"],
  theme: {
    extend: {
      colors: {
        court:   "#0C0D12",
        surface: "#12151A",
        rim:     "#1E2530",
        volt:    "#FFD100",
        "txt":   "#F0F0F0",
        "muted": "#8899AA",
      },
      fontFamily: {
        condensed: ["Barlow Condensed", "sans-serif"],
        sans:      ["Barlow", "sans-serif"],
      },
    },
  },
  plugins: [],
};
