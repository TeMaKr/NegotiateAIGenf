<template>
  <v-dialog v-model="isDialog" width="500">
    <template v-slot:activator="{ props }">
      <v-btn
        v-bind="props"
        variant="flat"
        text="Create user"
        color="primary"
        class="text-none"
      />
    </template>
    <template v-slot:default>
      <v-card>
        <app-alert :is-alert="isErrorMutate">
          User could not be created
        </app-alert>
        <v-form
          class="pa-2"
          v-model="isValid"
          id="create-form"
          @submit.prevent="mutate()"
        >
          <v-card-title>Create user</v-card-title>
          <v-divider />
          <v-card-text>
            The user will receive an email with an invitation link. There they
            can set their password.
          </v-card-text>
          <v-card-text>
            <v-text-field
              v-model="user.email"
              :rules="emailRules"
              variant="outlined"
              label="Email"
              autocomplete="email"
            />
            <v-text-field
              v-model="user.first_name"
              variant="outlined"
              label="First name"
              :rules="nameRules"
            />
            <v-text-field
              v-model="user.last_name"
              variant="outlined"
              label="Last name"
              :rules="nameRules"
            />
          </v-card-text>
          <v-divider />
          <v-card-actions>
            <v-spacer />
            <v-btn variant="tonal" @click="isDialog = false"> Cancel </v-btn>
            <v-btn
              variant="flat"
              color="primary"
              :loading="isPendingMutate"
              :disabled="!isValid"
              form="create-form"
              type="submit"
            >
              Save
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </template>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useMutation, useQueryClient } from "@tanstack/vue-query";
import { pb, QueryEnumKeys } from "@/composables/pocketbase";
import { Collections } from "@/composables/pocketbase/types";

const queryClient = useQueryClient();

const isValid = ref<boolean>(false);
const isDialog = ref(false);
const user = ref({
  email: "",
  first_name: "",
  last_name: "",
});

const nameRules = [
  (v: string) => !!v || "Name is required",
  (v: string) =>
    (v && v.length >= 2) || "Name must be at least 2 characters long",
];
const emailRules = [
  (v: string | undefined) => !!v || "E-Mail is required",
  (v: string | undefined) => (!!v && validateEmail(v)) || "E-Mail is not valid",
];
const validateEmail = (email: string) => {
  return !!String(email)
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
    );
};

const {
  isPending: isPendingMutate,
  isError: isErrorMutate,
  mutate,
} = useMutation({
  mutationFn: async () => {
    const password = window.crypto.randomUUID();
    let response = await pb.collection(Collections.Users).create({
      ...user.value,
      password: password,
      passwordConfirm: password,
      emailVisibility: true,
      verified: false,
    });
    await pb.collection(Collections.Users).requestPasswordReset(response.email);
  },
  onSuccess: () => {
    emit("created");
    queryClient.invalidateQueries({ queryKey: [QueryEnumKeys.Users] });
    isDialog.value = false;
  },
});

const emit = defineEmits<{
  (e: "created"): void;
}>();
</script>
