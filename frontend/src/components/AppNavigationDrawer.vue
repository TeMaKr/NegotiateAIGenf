<template>
  <v-navigation-drawer
    v-model="showDrawer"
    disable-resize-watcher
    :permanent="!mdAndDown && isAuthenticated"
    color="background-variant"
    width="300"
  >
    <v-list nav class="px-sm-8 px-md-8">
      <!-- User Profile Section (when authenticated) -->
      <div v-if="isAuthenticated">
        <v-list-item class="py-4">
          <template #prepend>
            <v-avatar size="40" color="primary" variant="tonal">
              <span class="text-h6">{{
                user?.first_name?.charAt(0).toUpperCase()
              }}</span>
            </v-avatar>
          </template>
          <v-list-item-title class="font-weight-medium">
            {{ `${user?.first_name} ${user?.last_name}` }}
          </v-list-item-title>
          <v-list-item-subtitle class="text-caption">
            {{ user?.email }}
          </v-list-item-subtitle>
        </v-list-item>
        <v-divider class="my-2" />
      </div>

      <!-- Main Navigation Items -->
      <v-list-item
        :to="{ name: 'LandingPage', query: { ...route.query } }"
        prepend-icon="mdi-home"
        class="mb-1"
      >
        <template #title><span class="font-weight-bold">Start</span></template>
      </v-list-item>

      <v-list-item
        :to="{ name: 'ChatInterface', query: { ...route.query } }"
        prepend-icon="mdi-message-question"
        class="mb-1"
      >
        <template #title>
          <span class="font-weight-bold">Submissions Analyser</span>
        </template>
      </v-list-item>

      <v-list-item
        :to="{ name: 'SubmissionsByTopic', query: { ...route.query } }"
        prepend-icon="mdi-table-search"
        class="mb-1"
      >
        <template #title>
          <span class="font-weight-bold">Advanced Analyser</span>
        </template>
      </v-list-item>

      <v-list-item
        :to="{ name: 'DocumentList', query: { ...route.query } }"
        prepend-icon="mdi-file-document-multiple-outline"
        class="mb-1"
      >
        <template #title>
          <span class="font-weight-bold">Submissions Browser</span>
        </template>
      </v-list-item>

      <v-list-item
        :to="{ name: 'DraftTreatyExplorer', query: { ...route.query } }"
        prepend-icon="mdi-gauge"
        class="mb-1"
      >
        <template #title>
          <span class="font-weight-bold">Draft Treaty Explorer</span>
        </template>
      </v-list-item>

      <!-- Settings Section (when authenticated) -->
      <template v-if="isAuthenticated">
        <v-list-item
          :to="{ name: 'Settings', query: { ...route.query } }"
          prepend-icon="mdi-cog"
          class="mb-1"
        >
          <template #title>
            <span class="font-weight-bold">Settings</span>
          </template>
        </v-list-item>
      </template>
      <div class="pb-4 mt-4">
        <v-btn
          v-if="isAuthenticated"
          @click="logout"
          variant="outlined"
          color="primary"
          block
        >
          Logout
        </v-btn>
        <v-btn
          v-else
          :to="{ name: 'Login', query: { ...route.query } }"
          variant="flat"
          color="primary"
          block
        >
          Login
        </v-btn>
      </div>
    </v-list>

    <!-- Login/Logout Section -->
    <template #append> </template>
  </v-navigation-drawer>
</template>

<script lang="ts" setup>
import { useDisplay, useTheme } from "vuetify";
import { pb, usePocketBase } from "@/composables/pocketbase";
import { useRoute } from "vue-router";

const route = useRoute();

const showDrawer = defineModel({ required: true, type: Boolean });

const theme = useTheme();

const { user, isAuthenticated } = await usePocketBase();
const { mdAndDown } = useDisplay();
const router = useRouter();

// Open drawer on default
watch(
  () => router.currentRoute.value.meta.requiresAuth,
  (from, to) => {
    if (to) {
      if (!showDrawer.value && from !== to) {
        showDrawer.value = true;
      }
    }
  },
  { immediate: true },
);

// Close drawer on window expand
watch(
  () => mdAndDown.value,
  () => {
    if (!mdAndDown.value) {
      showDrawer.value = false;
    }
  },
);

const logout = () => {
  try {
    pb.authStore.clear();
  } catch (error) {
    console.error(error);
  } finally {
    showDrawer.value = false;
    router.push({ name: "LandingPage" });
  }
};
</script>

<style scoped>
.v-list-item:not(.v-list-item--active) .font-weight-bold {
  color: v-bind('theme.current.value.colors["outline"]') !important;
}

.v-list-item:not(.v-list-item--active) .v-icon {
  color: v-bind('theme.current.value.colors["outline"]') !important;
}
</style>
