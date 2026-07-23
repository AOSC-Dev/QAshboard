<template>
  <v-container class="h-full items-center">
    <v-card :title="$t('home.title')" class="block" />

    <div class="grid sm:grid-cols-3 gap-4 mt-4">
      <v-card v-for="item in latestCoverage">
        <v-card-title>{{ item.architecture }}</v-card-title>
        <div class="w-40 h-40 mx-auto mb-2">
          <v-chart :option="options(item.coverage)" />
        </div>
      </v-card>
    </div>
  </v-container>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import VChart from "vue-echarts";
import { use } from "echarts/core";
import { PieChart } from "echarts/charts";
import { TitleComponent } from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";
import { getCoverage } from "@/client";

use([TitleComponent, PieChart, CanvasRenderer]);

const options = (coverage: number) => {
  const a = coverage.toFixed(2);
  const b = (100 - Number(a)).toFixed(2);
  return {
    series: [
      {
        type: "pie",
        label: { show: false, position: "center" },
        labelLine: { show: false },
        emphasis: { label: { show: true } },
        radius: ["40%", "80%"],
        data: [
          { value: a, name: a },
          { value: b, name: b },
        ],
      },
    ],
  };
};

const latestCoverage = ref();

onMounted(async () => {
  const date = new Date().toISOString();
  const { data } = await getCoverage({
    query: { start: date, end: date, interval: "P1D" },
  });
  latestCoverage.value = data;
});
</script>
