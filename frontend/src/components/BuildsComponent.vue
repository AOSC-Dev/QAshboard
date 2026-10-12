<template>
  <build-table
    v-model:page="page"
    v-model:items-per-page="itemsPerPage"
    :items="items"
    :items-length="totalItems"
    :loading="loading"
    :load-items="loadItems"
    :hide-default-footer="hideDefaultFooter"
    :success="success"
  >
  </build-table>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { getBuilds, type BuildPublic } from "@/client";
import BuildTable from "./BuildTable.vue";

const props = withDefaults(
  defineProps<{
    defaultItemsPerPage?: number;
    hideDefaultFooter?: boolean;
    success?: boolean | null;
  }>(),
  { defaultItemsPerPage: 10, hideDefaultFooter: false, success: null },
);

const page = ref(1);
const itemsPerPage = ref(props.defaultItemsPerPage);
const items = ref<BuildPublic[]>([]);
const loading = ref(true);
const totalItems = ref(0);

const loadItems = async (opts: { page: number; itemsPerPage: number }) => {
  loading.value = true;
  const { page, itemsPerPage } = opts;
  const { data, error } = await getBuilds({
    query: {
      limit: itemsPerPage,
      offset: (page - 1) * itemsPerPage,
      success: props.success,
    },
  });
  totalItems.value = data?.total ?? 0;
  items.value = data?.items ?? [];
  loading.value = false;
};
</script>
