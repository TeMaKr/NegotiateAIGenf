/**
 * plugins/index.ts
 *
 * Automatically included in `./src/main.ts`
 */

// Types
import type { App } from "vue";
import { VueQueryPlugin } from "@tanstack/vue-query";
import router from "../router";
import pinia from "../stores";
import ECharts from "./echarts";
import plausible from "./plausible";

// Plugins
import vuetify from "./vuetify";

export function registerPlugins(app: App) {
  app
    .use(vuetify)
    .use(router)
    .use(pinia)
    .use(VueQueryPlugin)
    .use(ECharts)
    .use(plausible);
}
