<template>
  <v-bottom-navigation>
    <v-btn v-for="item in navigation" :key="item.to" :to="item.to" exact>
      <v-icon :icon="item.icon" />
      <span>{{ item.label }}</span>
    </v-btn>
  </v-bottom-navigation>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n();

const navigation = computed(() => [
  { to: "/", icon: "mdi-view-dashboard-outline", label: t("home.title") },
  { to: "/builds", icon: "mdi-hammer-wrench", label: t("builds.title") },
]);
</script>
