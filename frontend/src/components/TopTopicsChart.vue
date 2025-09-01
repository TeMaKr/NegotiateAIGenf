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
  LegendComponent,
  GridComponent,
  TooltipComponent,
} from "echarts/components";
import VChart from "vue-echarts";
import { computed } from "vue";
import { useQuery } from "@tanstack/vue-query";
import { Collections, pb, QueryEnumKeys } from "@/composables/pocketbase";
import { useTheme } from "vuetify";
import type {
  SubmissionsResponse,
  TopicsResponse,
} from "@/composables/pocketbase/types";

use([
  GridComponent,
  CanvasRenderer,
  BarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
]);

const theme = useTheme();
const { data: topics } = useQuery({
  queryKey: [QueryEnumKeys.Topics, "submissionsPerTopic"],
  queryFn: async () => {
    return await pb.collection(Collections.Topics).getFullList<
      TopicsResponse & {
        expand: {
          submissions_via_topic: SubmissionsResponse[];
          child: TopicsResponse[];
        };
      }
    >({ expand: "submissions_via_topic,child", sort: "-name" });
  },
});

const aggregatedTopicsData = computed(() => {
  if (!topics.value) return [];

  const childTopicIds = new Set<string>(
    topics.value
      .filter((topic) => topic.expand?.child)
      .flatMap((topic) => topic.expand.child.map((child) => child.id)),
  );

  // Create a map to store aggregated submission counts
  const topicSubmissionMap = new Map<string, number>();

  // First, collect direct submissions for each topic
  topics.value.forEach((topic) => {
    const directSubmissions = topic.expand?.submissions_via_topic?.length || 0;
    topicSubmissionMap.set(topic.id, directSubmissions);
  });

  topics.value.forEach((topic) => {
    if (topic.expand?.child) {
      topic.expand.child.forEach((childTopic) => {
        const childSubmissions =
          topics.value?.find((t) => t.id === childTopic.id)?.expand
            ?.submissions_via_topic?.length || 0;

        const currentParentCount = topicSubmissionMap.get(topic.id) || 0;
        topicSubmissionMap.set(topic.id, currentParentCount + childSubmissions);
      });
    }
  });

  return topics.value
    .filter((topic) => !childTopicIds.has(topic.id))
    .map((topic) => ({
      id: topic.id,
      name: topic.name,
      submissionsCount: topicSubmissionMap.get(topic.id) || 0,
      directSubmissions: topic.expand?.submissions_via_topic?.length || 0,
      childTopics:
        topic.expand?.child?.map((childTopic) => {
          const childSubmissionCount =
            topics.value?.find((t) => t.id === childTopic.id)?.expand
              ?.submissions_via_topic?.length || 0;
          return {
            id: childTopic.id,
            name: childTopic.name,
            submissionsCount: childSubmissionCount,
          };
        }) || [],
    }))
    .sort((a, b) => {
      // Sort by total submissions count in descending order
      return b.submissionsCount - a.submissionsCount;
    })
    .slice(0, 10); // Limit to top 10 topics
});

const option = computed(() => {
  if (!aggregatedTopicsData.value.length) return {};

  const topicNames = aggregatedTopicsData.value.map((topic) => topic.name);
  const directSubmissions = aggregatedTopicsData.value.map(
    (topic) => topic.directSubmissions,
  );
  const childSubmissions = aggregatedTopicsData.value.map(
    (topic) => topic.submissionsCount - topic.directSubmissions,
  );

  return {
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "shadow",
      },
      formatter: (params: any) => {
        const dataIndex = params[0].dataIndex;
        const topic = aggregatedTopicsData.value[dataIndex];

        let tooltipContent = `
          <strong>Topic ${topic.name}:</strong><br/>
          Total Submissions: ${topic.submissionsCount}<br/>
          Direct Submissions: ${topic.directSubmissions}<br/>
        `;

        if (topic.childTopics.length > 0) {
          tooltipContent += ` <br/>`;
          topic.childTopics.forEach((child) => {
            tooltipContent += `<strong>Subtopic ${child.name}:</strong>`;
            tooltipContent += `<br/>Submissions: ${child.submissionsCount}<br/>`;
          });
        }

        return tooltipContent;
      },
    },
    legend: {
      data: ["Subtopic Submissions", "Direct Submissions"],
      bottom: 10,
    },
    grid: {
      left: "3%",
      right: "4%",
      bottom: "15%",
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: topicNames,
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
        name: "Subtopic Submissions",
        data: childSubmissions,
        type: "bar",
        stack: "total",
        label: {
          show: true,
          position: "inside",
          formatter: (params: any) => {
            return params.value > 0 ? params.value : "";
          },
          fontWeight: "400",
        },
        emphasis: {
          focus: "series",
        },
        itemStyle: {
          color: theme.current.value.colors.secondary,
        },
      },
      {
        name: "Direct Submissions",
        data: directSubmissions,
        type: "bar",
        stack: "total",
        label: {
          show: true,
          position: "inside",
          formatter: (params: any) => {
            return params.value > 0 ? params.value : "";
          },
          fontWeight: "400",
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
</script>
