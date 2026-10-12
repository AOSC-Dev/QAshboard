<template>
  <v-container class="grid gap-4">
    <v-card :title="$t('packages.title')" />

    <v-card class="w-full">
      <v-data-table-server
        v-model:page="page"
        v-model:items-per-page="itemsPerPage"
        :items-per-page-options="itemsPerPageOptions"
        :loading="loading"
        :headers="headers"
        :items="items"
        :items-length="totalItems"
        :group-by="[{ key: 'package_name' }]"
        group-expand-icon="mdi-chevron-right"
        group-collapse-icon="mdi-chevron-down"
        @update:options="loadItems"
        disable-sort
      >
        <template
          v-slot:group-header="{ item, columns, toggleGroup, isGroupOpen }"
        >
          <tr>
            <td @click="toggleGroup(item)">
              <div class="flex items-center gap-2">
                <v-btn
                  :icon="isGroupOpen(item) ? '$expand' : '$next'"
                  color="medium-emphasis"
                  density="comfortable"
                  size="small"
                  elevation="0"
                />
                <span>{{ item.value }}</span>
              </div>
            </td>
            <td :colspan="columns.length - 1">
              <v-icon
                v-for="arch in architectures"
                :key="arch"
                v-bind="
                  ((v) =>
                    typeof v !== 'boolean'
                      ? { icon: 'mdi-circle-slice-8', color: '#8d8d8d' }
                      : v === true
                        ? { icon: 'mdi-check-circle-outline', color: 'success' }
                        : { icon: 'mdi-close-circle-outline', color: 'error' })(
                    item.items.filter((i) => i.raw.architecture === arch)[0]
                      ?.raw?.success,
                  )
                "
              />
            </td>
          </tr>
        </template>
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
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useI18n } from "vue-i18n";
import { getPackages, type BuildPublic } from "@/client";

const { t } = useI18n();
const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
const page = ref(1);
const itemsPerPage = ref(10);
const itemsPerPageOptions = [10, 25, 50, 100, 250, 500];
const items = ref<BuildPublic[]>([]);
const loading = ref(true);
const totalItems = ref(0);
const architectures = ref<string[]>([]);

const headers = computed(() => [
  { key: "data-table-group", title: t("builds.columns.package_name") },
  { key: "success", title: t("builds.columns.success") },
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
