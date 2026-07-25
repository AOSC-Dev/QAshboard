<template>
  <v-container class="grid gap-4">
    <v-card :title="$t('builds.title')" />

    <v-card class="w-full">
      <BuildsComponent />
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import BuildsComponent from "@/components/BuildsComponent.vue";
</script>
