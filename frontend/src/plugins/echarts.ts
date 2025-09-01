import { type App } from "vue";
import "echarts";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { MapChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  GeoComponent,
} from "echarts/components";
import VChart from "vue-echarts/csp";
import "vue-echarts/csp/style.css";

// import lightTheme from "./themes/light-theme.json";

use([
  CanvasRenderer,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  MapChart,
  GeoComponent,
]);

// registerTheme("light-theme", lightTheme);

export default {
  install(app: App) {
    app.component("VChart", VChart);
  },
};
