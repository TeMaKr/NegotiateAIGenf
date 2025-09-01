<template>
  <v-chart
    class="chart"
    :option="option"
    autoresize
    style="height: 500px; width: 100%"
  />
</template>

<script setup lang="ts">
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
} from "echarts/components";
import VChart from "vue-echarts";
import { ref, computed, watchEffect } from "vue";
import { useQuery } from "@tanstack/vue-query";
import { Collections, pb, QueryEnumKeys } from "@/composables/pocketbase";
import { useTheme } from "vuetify";

use([
  GridComponent,
  CanvasRenderer,
  BarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
]);

const theme = useTheme();

const { data: submissionsPerSession } = useQuery({
  queryKey: [QueryEnumKeys.SubmissionsPerSession],
  queryFn: async () => {
    return await pb
      .collection(Collections.SubmissionsPerSession)
      .getFullList({});
  },
});

const sessions = computed(() => {
  return submissionsPerSession.value?.map((item) => item.session) || [];
});

const submissionsCount = computed(() => {
  return (
    submissionsPerSession.value?.map((item) => item.submissions_count) || []
  );
});

const option = computed(() => {
  if (!submissionsPerSession.value?.length) return {};

  return {
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "shadow",
      },
      formatter: (params: any) => {
        const sessionName = params[0].name;
        const submissionCount = params[0].value;
        return `
          <strong>Session: ${sessionName}</strong><br/>
          Submissions: ${submissionCount}
        `;
      },
    },
    grid: {
      left: "3%",
      right: "4%",
      bottom: "15%",
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: sessions.value,
      axisTick: {
        show: false,
      },
      axisLine: {
        show: false,
      },
      axisLabel: {
        fontWeight: "300",
      },
    },
    yAxis: {
      type: "value",
      axisLabel: {
        fontWeight: "300",
      },
      minInterval: 1,
    },
    series: [
      {
        data: submissionsCount.value,
        type: "bar",
        label: {
          show: true,
          position: "inside",
        },
        emphasis: {
          focus: "series",
        },
        itemStyle: {
          color: theme.current.value.colors.primary,
        },
      },
    ],
  };
});

watchEffect(() => {
  if (option.value?.series?.[0]) {
    option.value.xAxis.data = sessions.value;
    option.value.series[0].data = submissionsCount.value;
  }
});
</script>
