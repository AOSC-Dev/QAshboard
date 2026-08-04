<template>
  <v-container class="grid gap-4">
    <v-card :title="`Build Detail [${buildId}]`" />
    <v-card>
      <v-table class="px-2">
        <tbody v-if="buildDetail.data.value">
          <tr v-for="entry in Object.entries(buildDetail.data.value)">
            <td>{{ entry[0] }}</td>
            <td>{{ entry[1] }}</td>
          </tr>
        </tbody>
      </v-table>
    </v-card>
    <v-card class="p-4">
      <span class="text-lg">Logs</span>
      <v-divider class="my-2" />
      <pre
        v-if="buildLogs.data.value"
        v-html="buildLogs.data.value"
        class="text-sm overflow-auto"
      ></pre>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { useRoute } from "vue-router";
import { AnsiUp } from "ansi_up";
import { getBuild, getBuildLogs } from "@/client";

const route = useRoute();
const ansiUp = new AnsiUp();

const buildId = route.params.id;
const buildDetail = { data: ref(), error: ref() };
const buildLogs = { data: ref(), error: ref() };

const updateBuildDetails = async () => {
  const { data, error } = await getBuild({ path: { id: Number(buildId) } });
  buildDetail.data.value = data;
  buildDetail.error.value = error;
};

const updateBuildlogs = async () => {
  const { data, error } = await getBuildLogs({ path: { id: Number(buildId) } });

  buildLogs.data.value = ansiUp.ansi_to_html(data || "");
  buildLogs.error.value = error;
};

// const log = await data.text()
watch(
  () => route.params.id,
  () => {
    (updateBuildDetails(), updateBuildlogs());
  },
  { immediate: true },
);
</script>
