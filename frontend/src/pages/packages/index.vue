<template>
  <v-container class="grid gap-4">
    <v-card :title="$t('packages.title')" />

    <v-card class="w-full">
      <build-table
        v-model:page="page"
        v-model:items-per-page="itemsPerPage"
        :items="items"
        :items-length="totalItems"
        :loading="loading"
        :load-items="loadItems"
        :group-by-packages="true"
        :architectures="architectures"
      />
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { getPackages, type BuildPublic } from "@/client";
import BuildTable from "../../components/BuildTable.vue";

const page = ref(1);
const itemsPerPage = ref(10);
const items = ref<BuildPublic[]>([]);
const loading = ref(true);
const totalItems = ref(0);
const architectures = ref<string[]>([]);

const loadItems = async (opts: { page: number; itemsPerPage: number }) => {
  loading.value = true;
  const { page, itemsPerPage } = opts;
  const { data, error } = await getPackages({
    query: {
      limit: itemsPerPage,
      offset: (page - 1) * itemsPerPage,
    },
  });

  totalItems.value = data?.total ?? 0;
  items.value = data?.items ?? [];
  architectures.value = data?.architectures ?? [];
  loading.value = false;
};
</script>
