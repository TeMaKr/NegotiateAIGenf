import {
  createRouter,
  createWebHistory,
  type RouteLocationNormalized,
  type RouteRecordRaw,
} from "vue-router";
import { usePocketBase } from "@/composables/pocketbase";

declare module "vue-router" {
  interface RouteMeta {
    requiresAuth?: boolean;
  }
}

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    redirect: "/landing-page",
  },
  {
    path: "/landing-page",
    name: "LandingPage",
    component: () => import("@/views/LandingPage.vue"),
    meta: {
      requiresAuth: false,
    },
  },
  {
    path: "/chat-interface",
    name: "ChatInterface",
    component: () => import("@/views/ChatInterface.vue"),
    meta: {
      requiresAuth: false,
    },
  },
  {
    path: "/document-detail/:id",
    name: "DocumentDetail",
    component: () => import("@/views/DocumentDetail.vue"),
    meta: {
      requiresAuth: false,
    },
  },
  {
    path: "/document-list",
    name: "DocumentList",
    component: () => import("@/views/DocumentList.vue"),
    meta: {
      requiresAuth: false,
    },
  },
  {
    path: "/submissions-by-topic",
    name: "SubmissionsByTopic",
    component: () => import("@/views/SubmissionsByTopic.vue"),
    meta: {
      requiresAuth: false,
    },
  },
  {
    path: "/imprint",
    name: "Imprint",
    component: () => import("@/views/Imprint.vue"),
    meta: {
      requiresAuth: false,
    },
  },
  {
    path: "/data-privacy",
    name: "DataPrivacy",
    component: () => import("@/views/DataPrivacy.vue"),
    meta: {
      requiresAuth: false,
    },
  },
  {
    path: "/password-reset",
    name: "PasswordReset",
    component: () => import("@/views/PasswordReset.vue"),
    meta: {
      allowedRoles: false,
    },
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/Login.vue"),
    meta: {
      requiresAuth: false,
    },
  },
  {
    path: "/settings",
    name: "Settings",
    component: () => import("@/views/Settings.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/treaty-explorer",
    name: "DraftTreatyExplorer",
    component: () => import("@/views/DraftTreatyExplorer.vue"),
    meta: {
      title: "Draft Treaty Explorer",
    },
  },
  {
    path: "/documentation",
    name: "TechnicalDocumentation",
    component: () => import("@/views/TechnicalDocumentation.vue"),
    meta: {
      requiresAuth: false,
    },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

let lastRoute: RouteLocationNormalized | null = null;

router.beforeEach(async (to, _from, next) => {
  const { isAuthenticated, refresh } = await usePocketBase();

  if (_from.name) {
    lastRoute = _from;
  }

  await refresh();

  if (to.meta.requiresAuth && !isAuthenticated.value) {
    return next({ path: "/login" });
  }

  return next();
});

export { lastRoute };

export default router;
