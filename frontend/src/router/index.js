import { createRouter, createWebHistory } from "vue-router";
import MessageView from "../views/MessageView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: MessageView,
  },
  {
    path: "/state",
    name: "state",
    component: () =>
      import(/* webpackChunkName: "state" */ "../views/StateView.vue"),
  },
  {
    path: "/emergency",
    name: "emergency",
    component: () =>
      import(/* webpackChunkName: "state" */ "../views/EmergencyView.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
