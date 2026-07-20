<template>
  <div>{{ data }}</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getBuilds } from "@/client";

const data = ref();
onMounted(async () => {
  const result = await getBuilds({ query: { limit: 3 } });
  data.value = result.data;
});
</script>
