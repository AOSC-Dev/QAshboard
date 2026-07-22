/**
 * router/index.ts
 *
 * Manual routes for ./src/pages/*.vue
 */

// Composables
import { createRouter, createWebHistory } from "vue-router";
import Index from "@/pages/index.vue";
import builds from "@/pages/builds.vue";
import stats from "@/pages/stats.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      component: Index,
    },
    {
      path: "/stats",
      component: stats,
    },
    {
      path: "/builds",
      component: builds,
    },
  ],
});

export default router;
