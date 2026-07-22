<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>

    <bottom-navigation />
  </v-app>
</template>

<script setup lang="ts">
import BottomNavigation from "./components/BottomNavigation.vue";
</script>
