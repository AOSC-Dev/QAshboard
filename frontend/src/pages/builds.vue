<template>
  <h1>{{ $t("builds.title") }}</h1>
  <v-container class="h-full flex items-center" max-width="900">
    <BuildsComponent />
  </v-container>
</template>

<script setup lang="ts">
import BuildsComponent from "@/components/BuildsComponent.vue";
</script>
