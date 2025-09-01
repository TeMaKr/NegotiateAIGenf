<template>
  <v-container>
    <div class="d-flex justify-center align-center" style="height: 100vh">
      <v-card width="500px">
        <app-alert :is-alert="isError">E-Mail or password incorrect.</app-alert>
        <v-card-text class="d-flex flex-column align-center text-center">
          <h1>Negotiation AI Login</h1>
          <p class="text-caption mt-4">
            This area is for internal use by authorized users only. All public
            content remains available throughout the rest of the site.
          </p>
        </v-card-text>
        <v-card-text>
          <v-text-field
            v-model="email"
            autocomplete="email"
            autofocus
            label="E-Mail"
            variant="outlined"
          />
          <v-text-field
            v-model="password"
            :append-inner-icon="isPasswordVisible ? 'mdi-eye-off' : 'mdi-eye'"
            autocomplete="current-password"
            label="Password"
            :type="isPasswordVisible ? 'text' : 'password'"
            variant="outlined"
            @click:append-inner="isPasswordVisible = !isPasswordVisible"
          />
        </v-card-text>

        <v-card-actions class="justify-center">
          <v-btn
            class="text-none"
            color="primary"
            text="Login"
            variant="flat"
            @click="login"
          />
        </v-card-actions>
      </v-card>
    </div>
  </v-container>
</template>
<script setup lang="ts">
import { ref } from "vue";
import { pb } from "@/composables/pocketbase";
import { Collections } from "@/composables/pocketbase/types";
import { lastRoute } from "@/router";

const router = useRouter();

const email = ref("");
const password = ref("");
const isError = ref(false);
const isPasswordVisible = ref(false);

const login = async () => {
  try {
    await pb
      .collection(Collections.Users)
      .authWithPassword(email.value, password.value);
    let lastPage = "";
    if (lastRoute?.fullPath) {
      lastPage = lastRoute.fullPath as string;
    } else {
      lastPage = "/chat-interface";
    }
    await router.push({ path: lastPage });
  } catch (error) {
    console.error(error);
    isError.value = true;
  }
};
</script>
