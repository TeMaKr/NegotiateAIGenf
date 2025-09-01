/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Composables
import { createVuetify, type ThemeDefinition } from "vuetify";
// Styles
import "@mdi/font/css/materialdesignicons.css";

import "vuetify/styles";

export default createVuetify({
  theme: {
    defaultTheme: "light",
    themes: {
      light: {
        colors: {
          primary: "#09677F",
          "primary-variant": "#0C7E7B",
          "primary-variant-2": "#084656",
          "on-primary": "#FFFFFF",
          secondary: "#349DB9",
          "secondary-variant": "#107D99",
          "on-secondary": "#FFFFFF",
          error: "#BA1A1A",
          "on-error": "#FFFFFF",
          background: "#F5FAFD",
          "background-variant": "#FFFFFF",
          "on-background": "#171C1F",
          surface: "#F5FAFB",
          "on-surface": "#171D1E",
          outline: "#70787C",
          "outline-variant": "#BFC8CC",
          success: "#519E2E",
          "on-success": "#FFFFFF",
          warning: "#BC8A20",
          "on-warning": "#FFFFFF",
          info: "#205DB9",
          "on-info": "#FFFFFF",
        },
      },
    },
  },
  defaults: {
    VBtn: {
      flat: true,
      class: "text-none",
    },
  },
});
