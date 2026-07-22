<template>
  <VChart :option="option" autoresize />
</template>

<script setup lang="ts">
import { ref, provide, onMounted } from "vue";
import { useTheme } from "vuetify";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { LineChart } from "echarts/charts";
import {
  DatasetComponent,
  GridComponent,
  LegendComponent,
  TitleComponent,
  TooltipComponent,
  TransformComponent,
} from "echarts/components";
import type { ECBasicOption } from "echarts/types/dist/shared";
import VChart, { THEME_KEY } from "vue-echarts";
import { getCoverage } from "@/client";

use([
  CanvasRenderer,
  LineChart,
  DatasetComponent,
  GridComponent,
  LegendComponent,
  TitleComponent,
  TooltipComponent,
  TransformComponent,
]);

const theme = useTheme();
provide(THEME_KEY, () =>
  theme.global.current.value.dark ? "dark" : "default",
);

const option = ref<ECBasicOption>();

onMounted(async () => {
  const { data } = await getCoverage({
    query: { interval: "P1D" },
  });
  const coverage = data ?? [];
  const architectures = [...new Set(coverage.map((i) => i.architecture))];

  option.value = {
    backgroundColor: "transparent",
    legend: {},
    tooltip: { trigger: "axis" },
    xAxis: { type: "time" },
    yAxis: { axisLabel: { formatter: "{value} %" } },
    dataset: [
      { source: coverage },
      ...architectures.map((architecture) => ({
        transform: {
          type: "filter",
          config: { dimension: "architecture", value: architecture },
        },
      })),
    ],
    series: architectures.map((name, index) => ({
      name,
      type: "line",
      datasetIndex: index + 1,
      encode: { x: "snapshot", y: "coverage" },
      tooltip: {
        valueFormatter: (y: number) => y.toFixed(2) + " %",
      },
    })),
  };
});
</script>
