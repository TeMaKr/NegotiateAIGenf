<template>
  <v-row>
    <v-col cols="12" md="4">
      <div class="text-body-2">
        <p class="text-body-1">
          The topics organise treaty content based on the articles from the
          negotiation of the International Negotiating Committee on Plastic
          Pollution. The topics are derived from the structure of the most
          recent chair text, following the same order as the final draft, while
          maintaining some variation from the original treaty language.
        </p>

        <v-card variant="outlined" class="my-4">
          <div>
            <v-tabs v-model="tab" bg-color="surface">
              <v-tab value="one">How it works</v-tab>
              <v-tab value="two" :disabled="!selectedTopic">Key Elements</v-tab>
            </v-tabs>
            <v-btn @click="resetChart">Reset</v-btn>
          </div>

          <v-card-text style="height: 400px" class="overflow-y-auto">
            <v-tabs-window v-model="tab">
              <v-tabs-window-item value="one">
                <ul class="mb-4" style="margin-left: 0; padding-left: 1.2em">
                  <li class="mb-2">
                    <strong>Main topics (First Level)</strong> represent the
                    core thematic areas derived from the articles of the current
                    draft treaty. These are the primary topics used across all
                    filters in the application and reflect the structure of the
                    latest chair's text.
                  </li>
                  <li class="mb-2">
                    <strong>Historical topics (Second Level)</strong> include
                    categories from earlier drafts of the treaty. While no
                    longer used in the filters, submissions originally
                    categorized under these topics remain accessible when you
                    select the relevant main topic—for example, submissions
                    about fishing gear can still be found when you select
                    "releases and leakages" or "plastic waste management".
                  </li>
                  <li class="mb-2">
                    <strong>Key Elements</strong> are manually defined
                    analytical subcategories that highlight specific aspects
                    within each main topic. They enable more detailed analysis
                    of submissions and support targeted comparisons of country
                    positions in the Advanced Analyser & Comparison tool.
                  </li>
                </ul>

                <h4 class="mb-3">Usage:</h4>
                <p class="mb-3">
                  Click on any main topic to reveal related historical topics
                  and associated Key Elements. Historical topics may contain
                  different or additional Key Elements compared to their main
                  topics, as they can be associated with multiple areas of the
                  treaty.
                </p>
              </v-tabs-window-item>

              <v-tabs-window-item value="two">
                <p class="text-h6 font-weight-bold">
                  Topic: {{ selectedTopic?.name }}
                </p>

                <div v-if="selectedTopic">
                  <h4 class="mt-4">Key Elements:</h4>
                  <ul class="ml-4">
                    <li
                      v-for="element in selectedTopic.key_elements"
                      :key="element"
                    >
                      {{ element }}
                    </li>
                  </ul>
                </div>
              </v-tabs-window-item>
            </v-tabs-window>
          </v-card-text>
        </v-card>
      </div>
    </v-col>
    <v-col cols="12" md="8">
      <div style="height: 600px">
        <v-chart
          ref="chart"
          :option="option"
          autoresize
          style="height: 100%"
          @click="handleNodeClick"
        />
      </div>
      <div class="d-flex">
        <v-spacer></v-spacer>
        <v-btn
          class="mt-4"
          color="primary"
          variant="outlined"
          @click="resetChart"
          :disabled="!selectedTopic"
          prepend-icon="mdi-undo"
          >Reset</v-btn
        >
      </div>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useTheme } from "vuetify";
import topicsData from "../../data/topics.json";

const theme = useTheme();

// init chart
const chart = ref();

const tab = ref("one");

interface Subcategory {
  subcategory: string;
  key_elements: string[];
}

interface Topic {
  category: string;
  subcategories: Subcategory[];
  key_elements: string[];
}

interface TopicData {
  name: string;
  key_elements: string[];
}

const selectedTopic = ref<TopicData | null>(null);

const data = computed(() => {
  if (!topicsData || !Array.isArray(topicsData)) return [];

  return [
    {
      name: "Topics",
      children: topicsData.map((parentTopic: Topic) => ({
        name: parentTopic.category,
        topicData: {
          name: parentTopic.category,
          key_elements: parentTopic.key_elements.sort(),
        },
        children:
          parentTopic.subcategories && parentTopic.subcategories.length > 0
            ? parentTopic.subcategories.map((subcategory: Subcategory) => ({
                name: subcategory.subcategory,
                topicData: {
                  name: subcategory.subcategory,
                  key_elements: subcategory.key_elements.sort(),
                },
              }))
            : undefined,
      })),
    },
  ];
});

const handleNodeClick = (params: any) => {
  if (params.data.topicData) {
    selectedTopic.value = params.data.topicData;
    tab.value = "two"; // Switch to Key Elements tab when a topic is clicked
  } else {
    selectedTopic.value = null;
    tab.value = "one"; // Switch back to How it works tab if no topic is selected
  }
};

const resetChart = () => {
  selectedTopic.value = null;

  tab.value = "one"; // Reset to the first tab
  if (chart.value) {
    chart.value.chart.setOption({
      series: [
        {
          initialTreeDepth: 1, // Reset to show only the root "Topics"
        },
      ],
    });
  }
};

const option = computed(() => ({
  tooltip: {
    trigger: "item",
    triggerOn: "mousemove",
    formatter: function (params: any) {
      const data = params.data;
      return `
        <div style="padding: 8px; max-width: 300px;">
          <div style="word-wrap: break-word; white-space: normal;">
            ${data.name}
          </div>
        </div>
      `;
    },
    backgroundColor: "rgba(0, 0, 0, 0.8)",
    borderColor: "#666666",
    textStyle: {
      color: "#ffffff",
    },
  },
  series: [
    {
      type: "tree",
      data: data.value,
      top: "1%",
      left: "7%",
      bottom: "1%",
      right: "30%", // Reduced from 20% to 50% to shorten horizontal lines
      symbolSize: 12,

      initialTreeDepth: 1, // Start with just the root "Topics"

      animationDuration: 550,
      animationDurationUpdate: 750,

      emphasis: {
        focus: "descendant",
      },

      expandAndCollapse: true, // Enable click-to-expand

      label: {
        show: true,
        position: "left",
        verticalAlign: "middle",
        align: "right",
        color: theme.current.value.colors.onSurface,
        fontSize: 12, // Increased from 9 to 12
        fontWeight: "normal",
        formatter: function (params: any) {
          const name = params.data.name;
          // Truncate long names to 25 characters
          if (name.length > 25) {
            return name.substring(0, 25) + "...";
          }
          return name;
        },
      },

      leaves: {
        label: {
          position: "right",
          verticalAlign: "middle",
          align: "left",
          fontSize: 12, // Also increased for leaf nodes
        },
      },

      itemStyle: {
        color: theme.current.value.colors.primary,
        borderWidth: 1,
      },
      lineStyle: {
        color: theme.current.value.colors.primary,
        width: 1,
      },
    },
  ],
}));
</script>
