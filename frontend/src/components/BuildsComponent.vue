<template>
  <v-data-table-server
    v-model:items-per-page="itemsPerPage"
    :items="items"
    :items-length="totalItems"
    :loading="loading"
    @update:options="loadItems"
    :hide-default-footer="hideDefaultFooter"
  />
</template>

<script setup lang="ts">
import { ref } from "vue";
import { getBuilds, type BuildPublic } from "@/client";

const props = withDefaults(
  defineProps<{ defaultItemsPerPage?: number; hideDefaultFooter?: boolean }>(),
  { defaultItemsPerPage: 10, hideDefaultFooter: false },
);

const itemsPerPage = ref(props.defaultItemsPerPage);
const items = ref<BuildPublic[]>([]);
const loading = ref(true);
const totalItems = ref(0);

const loadItems = async (opts: { page: number; itemsPerPage: number }) => {
  loading.value = true;
  const { page, itemsPerPage } = opts;
  const { data, error } = await getBuilds({
    query: { limit: itemsPerPage, offset: (page - 1) * itemsPerPage },
  });
  totalItems.value = data?.total ?? 0;
  items.value = data?.items ?? [];
  loading.value = false;
};
</script>
