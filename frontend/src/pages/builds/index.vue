<template>
  <v-container class="grid gap-4">
    <v-card :title="$t('builds.title')" />

    <div class="flex gap-4 items-center justify-between">
      <v-btn-toggle v-model="success" mandatory>
        <v-btn icon="mdi-check" :value="true" />
        <v-btn icon="mdi-close" :value="false" />
        <v-btn text="All" :value="null" />
      </v-btn-toggle>
    </div>

    <v-card class="w-full">
      <BuildsComponent :success="success" />
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from "vue";
import BuildsComponent from "@/components/BuildsComponent.vue";

const success = ref(null);
</script>
