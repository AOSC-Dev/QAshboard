<template>
  <v-data-table-server
    v-model:page="page"
    v-model:items-per-page="itemsPerPage"
    :headers="headers"
    :items="items"
    :items-length="totalItems"
    :items-per-page-options="itemsPerPageOptions"
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
      {{ new Date(value).toLocaleString(undefined, { timeZone }) }}
    </template>
    <template v-slot:item.id="{ value }">
      <v-btn
        :to="`/builds/${value}`"
        icon="mdi-open-in-new"
        size="small"
        elevation="0"
      />
    </template>
  </v-data-table-server>
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { getBuilds, type BuildPublic } from "@/client";

const props = withDefaults(
  defineProps<{
    defaultItemsPerPage?: number;
    hideDefaultFooter?: boolean;
    success?: boolean | null;
  }>(),
  { defaultItemsPerPage: 10, hideDefaultFooter: false, success: null },
);

const { t } = useI18n();

const page = ref(1);
const itemsPerPage = ref(props.defaultItemsPerPage);
const itemsPerPageOptions = [10, 25, 50, 100, 250, 500];
const items = ref<BuildPublic[]>([]);
const loading = ref(true);
const totalItems = ref(0);
const search = ref();

const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;

const headers = computed(() => [
  { key: "success", title: t("builds.columns.success") },
  {
    key: "package_name",
    title: t("builds.columns.package_name"),
  },
  {
    key: "timestamp",
    title: t("builds.columns.timestamp", [timeZone]),
  },
  {
    key: "architecture",
    title: t("builds.columns.architecture"),
  },
  { key: "buildbot", title: t("builds.columns.buildbot") },
  {
    key: "failure_reason",
    title: t("builds.columns.failure_reason"),
  },
  { key: "id" },
]);

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
