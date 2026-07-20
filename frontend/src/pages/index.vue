<template>
  <v-container class="h-full flex items-center" max-width="900">
    {{ data }}
  </v-container>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { getBuilds } from "@/client";

const data = ref();
onMounted(async () => {
  const result = await getBuilds({ query: { limit: 3 } });
  data.value = result.data;
});
</script>
