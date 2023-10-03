import { createRouter, createWebHistory } from "vue-router";
import ControlView from "../views/ControlView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "control",
      component: ControlView,
    },
    {
      path: "/program",
      name: "program",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/ProgramView.vue"),
    },
  ],
});

export default router;
