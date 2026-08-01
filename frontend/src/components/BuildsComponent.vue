<template>
  <v-data-table-server
    v-model:page="page"
    v-model:items-per-page="itemsPerPage"
    :items="items"
    :items-length="totalItems"
    :loading="loading"
    @update:options="loadItems"
    :hide-default-footer="hideDefaultFooter"
    :search="search"
    disable-sort
  >
    <template v-slot:item.success="{ value }">
      <v-icon
        :icon="value ? 'mdi-check' : 'mdi-close'"
        :color="value ? 'success' : 'error'"
      />
    </template>
    <template v-slot:item.timestamp="{ value }">
      {{ new Date(value).toLocaleDateString() }}
    </template>
  </v-data-table-server>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { getBuilds, type BuildPublic } from "@/client";

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
const search = ref();

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

watch(
  () => props.success,
  () => {
    page.value = 1;
    search.value = String(props.success);
  },
);
</script>
