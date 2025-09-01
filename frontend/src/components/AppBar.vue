<template>
  <app-navigation-drawer v-model="drawer" />
  <v-app-bar color="white" flat>
    <v-btn
      color="primary"
      :to="{ name: 'LandingPage', query: { ...route.query } }"
      variant="flat"
      class="negotiate-ai-btn"
      >NegotiateAI</v-btn
    >

    <div
      v-if="!mdAndDown && !isAuthenticated"
      class="d-flex justify-center w-100"
    >
      <v-tabs color="primary">
        <v-tab
          text="Start"
          :to="{ name: 'LandingPage', query: { ...route.query } }"
          prepend-icon="mdi-home"
        />
        <v-tab
          text="Submissions Analyser"
          :to="{ name: 'ChatInterface', query: { ...route.query } }"
          prepend-icon="mdi-message-question"
        />
        <v-tab
          text="Advanced Analyser"
          :to="{ name: 'SubmissionsByTopic', query: { ...route.query } }"
          prepend-icon="mdi-table-search"
        />
        <v-tab
          text="Submissions Browser"
          :to="{ name: 'DocumentList', query: { ...route.query } }"
          prepend-icon="mdi-file-document-multiple-outline"
        />
        <v-tab
          text="Draft Treaty Explorer"
          :to="{ name: 'DraftTreatyExplorer', query: { ...route.query } }"
          prepend-icon="mdi-gauge"
        />
        <v-tab text="Login" :to="{ name: 'Login', query: { ...route.query } }">
          <template #default>
            <v-btn
              v-if="!isAuthenticated"
              variant="flat"
              text="Login"
              :to="{ name: 'Login', query: { ...route.query } }"
              color="primary"
              class="ms-auto text-none"
            />
          </template>
        </v-tab>
      </v-tabs>
    </div>

    <template #append>
      <v-app-bar-nav-icon
        v-if="mdAndDown || isAuthenticated"
        @click="drawer = !drawer"
        class="burger-menu-spacing rounded-lg"
        variant="flat"
        color="primary"
      />
    </template>
  </v-app-bar>
</template>

<script lang="ts" setup>
import { usePocketBase } from "@/composables/pocketbase";
import { useTheme, useDisplay } from "vuetify";
import { useRoute } from "vue-router";

const { isAuthenticated } = await usePocketBase();
const route = useRoute();

const drawer = ref(false);

const theme = useTheme();
const { mdAndDown } = useDisplay();
</script>

<style scoped>
.negotiate-ai-btn {
  font-size: 16px;
  margin-left: 32px !important;
  padding: 6px 12px;
  border-radius: 8px;
  color: v-bind('theme.current.value.colors["primary"]') !important;
  background-color: #09677f0f !important;
  /* 6% opacity */
  letter-spacing: normal;
}

.burger-menu-spacing {
  margin-right: 32px;
}

.v-tab:not(.v-tab--selected) {
  color: v-bind('theme.current.value.colors["outline"]') !important;
}

.v-tab:not(.v-tab--selected) .v-icon {
  color: v-bind('theme.current.value.colors["outline"]') !important;
}

@media (min-width: 600px) {
  .negotiate-ai-btn {
    margin-left: 80px !important;
  }

  .burger-menu-spacing {
    margin-right: 80px !important;
  }
}

@media (min-width: 1264px) {
  .negotiate-ai-btn {
    margin-left: 240px !important;
  }
}
</style>
