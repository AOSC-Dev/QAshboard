<template>
  <v-data-table-server
    v-model:page="page"
    v-model:items-per-page="itemsPerPage"
    :headers="headers"
    :items="items"
    :items-length="itemsLength"
    :items-per-page-options="itemsPerPageOptions"
    :loading="loading"
    @update:options="loadItems"
    :hide-default-footer="hideDefaultFooter"
    :search="search"
    :group-by="groupByPackages ? [{ key: 'package_name' }] : undefined"
    group-expand-icon="mdi-chevron-right"
    group-collapse-icon="mdi-chevron-down"
    disable-sort
  >
    <template
      v-if="groupByPackages && architectures"
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
                item.items.filter((i) => i.raw.architecture === arch)[0]?.raw
                  ?.success,
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
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { type BuildPublic } from "@/client";

const props = withDefaults(
  defineProps<{
    loadItems: (opts: { page: number; itemsPerPage: number }) => {};
    items: BuildPublic[];
    itemsLength: number;
    loading: boolean;
    hideDefaultFooter?: boolean;
    success?: boolean | null;
    groupByPackages?: boolean;
    architectures?: string[] | null;
  }>(),
  { hideDefaultFooter: false, success: null, groupByPackages: false },
);

const page = defineModel<number>("page");
const itemsPerPage = defineModel<number>("items-per-page");

const itemsPerPageOptions = [10, 25, 50, 100, 250, 500];
const search = ref();

const { t } = useI18n();
const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;

const headers = computed(() => {
  const commonHeaders = [
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
  ];

  if (props.groupByPackages)
    commonHeaders.unshift({
      key: "data-table-group",
      title: t("builds.columns.package_name"),
    });
  else
    commonHeaders.unshift({
      key: "package_name",
      title: t("builds.columns.package_name"),
    });

  return commonHeaders;
});

watch(
  () => props.success,
  () => {
    page.value = 1;
    search.value = String(props.success);
  },
);
</script>
