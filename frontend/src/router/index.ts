/**
 * router/index.ts
 *
 * Manual routes for ./src/pages/*.vue
 */

// Composables
import { createRouter, createWebHistory } from "vue-router";
import Index from "@/pages/index.vue";
import builds from "@/pages/builds.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      component: Index,
    },
    {
      path: "/builds",
      component: builds
    }
  ],
});

export default router;
