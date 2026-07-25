<template>
  <VChart :option="option" autoresize />
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
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
import VChart from "vue-echarts";
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

const props = defineProps<{ start?: Date; end?: Date }>();

const option = ref<ECBasicOption>();

const update = async () => {
  const { data } = await getCoverage({
    query: {
      start: props.start?.toISOString(),
      end: props.end?.toISOString(),
      interval: "P1D",
    },
  });
  const coverage = data ?? [];
  const architectures = [...new Set(coverage.map((i) => i.architecture))];

  option.value = {
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
    })) || undefined,
  };
};

watch([() => props.start, () => props.end], update, { immediate: true });
</script>
