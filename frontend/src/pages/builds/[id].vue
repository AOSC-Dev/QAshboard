<template>
  <v-container class="grid gap-4">
    <v-card :title="`Build Detail [${buildId}]`" />
    <v-card class="px-2">
      <v-table v-if="buildDetail.data.value">
        <tbody>
          <tr v-for="entry in Object.entries(buildDetail.data.value)">
            <td>{{ entry[0] }}</td>
            <td>{{ entry[1] }}</td>
          </tr>
        </tbody>
      </v-table>
      <div class="py-2 px-2" v-else>
        {{ buildLogs.error.value }}
      </div>
    </v-card>
    <v-card class="p-4">
      <div class="flex justify-between items-center">
        <span class="text-lg">Logs</span>
        <v-btn
          :href="buildLogsUrl"
          text="Raw"
          target="_blank"
          elevation="0"
          append-icon="mdi-open-in-new"
        />
      </div>
      <v-divider class="my-2" />
      <pre
        v-if="buildLogs.data.value"
        v-html="buildLogs.data.value"
        class="text-sm overflow-auto"
      ></pre>
      <div v-else>
        {{ buildLogs.error.value }}
      </div>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { AnsiUp } from "ansi_up";
import { getBuild, getBuildLogs } from "@/client";

const route = useRoute();

const buildId = computed(() => Number(route.params.id));
const buildDetail = { data: ref(), error: ref() };
const buildLogs = { data: ref(), error: ref() };
const buildLogsUrl = ref("");

const updateBuildDetails = async () => {
  const { data, error } = await getBuild({ path: { id: buildId.value } });
  buildDetail.data.value = data;
  buildDetail.error.value = error;
};

const updateBuildlogs = async () => {
  const { data, error, request } = await getBuildLogs({
    path: { id: buildId.value },
  });
  buildLogsUrl.value = request?.url ?? "";

  const ansiUp = new AnsiUp();
  buildLogs.data.value = ansiUp.ansi_to_html(data || "");
  buildLogs.error.value = error;
};

watch(buildId, () => Promise.all([updateBuildDetails(), updateBuildlogs()]), {
  immediate: true,
});
</script>
