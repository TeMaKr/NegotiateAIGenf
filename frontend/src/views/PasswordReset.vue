<template>
  <div
    style="
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100%;
    "
  >
    <v-card width="500px">
      <app-alert :is-alert="isError">
        An error occurred while resetting the password. Please try again.
      </app-alert>
      <v-card-text class="d-flex flex-column align-center">
        <h1>Set a password</h1>
      </v-card-text>
      <v-form v-model="isValid" id="reset-form" @submit.prevent="mutate()">
        <v-card-text>
          <v-text-field
            v-model="password"
            variant="outlined"
            :rules="passwordRules"
            :type="isVisiblePassword ? 'text' : 'password'"
            label="Password"
          >
            <template v-slot:append>
              <v-icon
                v-if="isVisiblePassword"
                @click="() => (isVisiblePassword = !isVisiblePassword)"
              >
                mdi-eye
              </v-icon>
              <v-icon
                v-else
                @click="() => (isVisiblePassword = !isVisiblePassword)"
              >
                mdi-eye-off
              </v-icon>
              <v-tooltip bottom max-width="400px">
                <template v-slot:activator="{ props }">
                  <v-icon class="ml-1" v-bind="props"> mdi-information </v-icon>
                </template>
                <p class="text-body-1">Password rules</p>
                <ul>
                  <li>At least 12 characters</li>
                  <li>At least one special character</li>
                  <li>At least one lowercase letter</li>
                  <li>At least one uppercase letter</li>
                  <li>At least one digit</li>
                </ul>
              </v-tooltip>
            </template>
          </v-text-field>

          <v-text-field
            v-model="passwordConfirm"
            :rules="passwordConfirmationRules"
            :type="isVisiblePassword ? 'text' : 'password'"
            label="Confirm Password"
            variant="outlined"
          />
        </v-card-text>
      </v-form>

      <v-card-actions class="justify-center">
        <v-btn
          :loading="isPending"
          :disabled="!isValid"
          variant="flat"
          color="primary"
          type="submit"
          class="text-none"
          form="reset-form"
        >
          Set Password
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useMutation } from "@tanstack/vue-query";
import { useRouter, useRoute } from "vue-router";
import { pb } from "@/composables/pocketbase";
import { Collections } from "@/composables/pocketbase/types";

import AppAlert from "@/components/AppAlert.vue";

const router = useRouter();
const route = useRoute();

const isValid = ref<boolean>(false);
const isVisiblePassword = ref<boolean>(false);
const password = ref<string>("");
const passwordConfirm = ref<string>("");

const containCapitalLetter = /^.*[A-Z].*$/;
const containLowerCaseLetter = /^.*[a-z].*$/;
const containNumber = /^.*[0-9].*$/;
const containSymbol = /^.*[^a-zA-Z0-9].*$/;

const passwordRules = computed(() => {
  return [
    (v: string) => !!v || "Password is required",
    (v: string) =>
      (v && v.length >= 12) || "Password must be at least 12 characters",
    (v: string) =>
      containCapitalLetter.test(v) || "At least one uppercase letter",
    (v: string) =>
      containLowerCaseLetter.test(v) || "At least one lowercase letter",
    (v: string) => containNumber.test(v) || "At least one digit",
    (v: string) => containSymbol.test(v) || "At least one special character",
  ];
});

const passwordConfirmationRules = computed(() => {
  return [
    passwordConfirm.value === password.value || "Passwords must be identical",
  ];
});

const { isPending, isError, mutate } = useMutation({
  mutationFn: async () => {
    await pb
      .collection(Collections.Users)
      .confirmPasswordReset(
        route.query.token as string,
        password.value,
        passwordConfirm.value,
      );
  },
  onSuccess: () => {
    router.push({ name: "LandingPage" });
  },
});
</script>
