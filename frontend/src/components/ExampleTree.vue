<template>
  <v-chart :option="option" autoresize style="height: 150px; max-width: 90%" />
</template>

<script setup lang="ts">
const option = computed(() => {
  return {
    series: [
      {
        type: "tree",
        silent: true,
        symbolSize: 15,
        symbolColor: "#09677F",
        itemStyle: {
          color: "#09677F",
        },
        expandAndCollapse: false,
        data: [
          {
            name: "Topic",

            children: [
              {
                name: "Child A",
                children: [
                  {
                    name: "Leaf C",
                  },
                  {
                    name: "Leaf D",
                  },
                  {
                    name: "Leaf E",
                  },
                ],
              },
              {
                name: "Child B",
              },
              {
                name: "Child D",
              },
              {
                name: "Child F",
              },
            ],
          },
        ],
        label: {
          position: "right",
          show: false,
        },
        lineStyle: {
          color: "#09677F",
          curveness: 0.4,
          width: 1.5,
        },
      },
    ],
  };
});
</script>
