<template>
  <v-container class="grid gap-4 items-center">
    <v-card class="block">
      <v-card-item>
        <v-card-subtitle>
          <a href="https://aosc.io" target="_blank">AOSC</a>
          <span> / </span><a href="/">QAshboard</a>
        </v-card-subtitle>
      </v-card-item>
      <v-card-text class="text-4xl flex justify-start items-center">
        <a href="https://aosc.io" target="_blank" class="w-[1em]">
          <v-img src="@/assets/logo.svg" />
        </a>
        <span>/</span> <a href="/">QAshboard</a>
      </v-card-text>
    </v-card>

    <div class="grid sm:grid-cols-3 gap-4">
      <v-card
        title="AOSC.io"
        :subtitle="$t('home.links.aoscIo')"
        append-icon="mdi-open-in-new"
        href="https://aosc.io"
        target="_blank"
      />
      <v-card
        title="Packages"
        :subtitle="$t('home.links.aoscPackages')"
        append-icon="mdi-open-in-new"
        href="https://packages.aosc.io"
        target="_blank"
      />
      <v-card
        title="BuildIt!"
        :subtitle="$t('home.links.aoscBuildIt')"
        append-icon="mdi-open-in-new"
        href="https://buildit.aosc.io"
        target="_blank"
      />
    </div>

    <v-divider />

    <div class="grid sm:grid-cols-3 gap-4">
      <v-card v-for="item in latestCoverage">
        <v-card-title>{{ item.architecture }}</v-card-title>
        <div class="w-40 h-40 mx-auto mb-2">
          <v-chart :option="options(item.coverage)" />
        </div>
      </v-card>
    </div>

    <v-card>
      <builds-component
        :default-items-per-page="5"
        :hide-default-footer="true"
      />
    </v-card>

    <v-btn to="/builds" append-icon="mdi-arrow-right">
      {{ $t("home.allBuilds") }}
    </v-btn>
  </v-container>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import VChart from "vue-echarts";
import { useTheme } from "vuetify";
import { use } from "echarts/core";
import { PieChart } from "echarts/charts";
import { TitleComponent } from "echarts/components";
import { SVGRenderer } from "echarts/renderers";
import { getCoverage } from "@/client";
import BuildsComponent from "@/components/BuildsComponent.vue";

use([TitleComponent, PieChart, SVGRenderer]);

const theme = useTheme();

const options = (coverage: number) => {
  const a = coverage.toFixed(2);
  const b = (100 - Number(a)).toFixed(2);
  return {
    title: {
      text: `${a}%`,
      subtext: "successful",
      top: "37%",
      itemGap: 2,
    },
    series: [
      {
        type: "pie",
        labelLine: { show: false },
        radius: ["58%", "80%"],
        data: [
          {
            value: a,
            name: a,
            itemStyle: {
              color: theme.current.value.colors.primary,
              borderColor: theme.current.value.colors["surface-variant"],
              borderWidth: 2,
            },
          },
          {
            value: b,
            name: b,
            itemStyle: {
              color: theme.current.value.colors.surface,
              borderColor: theme.current.value.colors["surface-variant"],
              borderWidth: 2,
            },
          },
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
