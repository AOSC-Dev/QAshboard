<template>
  <v-container class="grid gap-4">
    <v-card title="Stats" />

    <v-container class="flex gap-4 items-center">
      <v-date-input
        label="Start"
        v-model="start"
        hide-details
        :allowed-dates="(d) => (d ? d < end : true)"
      />
      <v-date-input
        label="End"
        v-model="end"
        hide-details
        :allowed-dates="
          (d) => (d ? d <= new Date() && (start ? d > start : true) : true)
        "
      />
    </v-container>

    <v-card class="h-160 w-full">
      <CoverageChart :start="start" :end="end" />
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { shallowRef } from "vue";
import CoverageChart from "@/components/CoverageChart.vue";

const start = shallowRef();
const end = shallowRef(new Date());
</script>
