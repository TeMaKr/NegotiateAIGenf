<template>
  <v-dialog v-model="isDialog" width="500">
    <template v-slot:activator="{ props }">
      <v-btn v-bind="props" icon="mdi-account-edit-outline" elevation="0" />
    </template>
    <template v-slot:default>
      <v-card>
        <app-alert :is-alert="isErrorMutate">
          User could not be updated
        </app-alert>
        <v-form
          class="pa-2"
          v-model="isValid"
          id="create-form"
          @submit.prevent="mutate()"
        >
          <v-card-title> Edit user </v-card-title>
          <v-divider />
          <v-card-text>
            <v-text-field
              v-model="userClone.first_name"
              variant="outlined"
              label="First name"
              :rules="nameRules"
            />
            <v-text-field
              v-model="userClone.last_name"
              variant="outlined"
              label="Last name"
              :rules="nameRules"
            />
          </v-card-text>
          <v-divider />
          <v-card-actions>
            <app-delete-dialog
              title="User"
              :mutation-fn="() => deleteUser()"
              :on-success="() => onDeleteSuccess()"
              button-text="Delete"
              isButton
            >
              <template v-slot:title> Delete user </template>
              <div>
                Do you really want to delete this user? This action cannot be
                undone.
              </div>
            </app-delete-dialog>
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
import { ref, toRefs, toRaw } from "vue";
import { useMutation, useQueryClient, useQuery } from "@tanstack/vue-query";
import { pb, QueryEnumKeys } from "@/composables/pocketbase";
import {
  Collections,
  type UsersResponse,
} from "@/composables/pocketbase/types";

const queryClient = useQueryClient();

const props = defineProps<{
  user: UsersResponse;
}>();

const { user } = toRefs(props);
const userClone = ref(structuredClone(toRaw(user.value)));

const isValid = ref<boolean>(false);
const isDialog = ref(false);

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
    userClone.value.emailVisibility = true;
    return await pb.collection(Collections.Users).update(userClone.value.id, {
      ...userClone.value,
    });
  },
  onSuccess: () => {
    emit("updated");
    queryClient.invalidateQueries({ queryKey: [QueryEnumKeys.Users] });
    isDialog.value = false;
  },
});

const deleteUser = async () => {
  await pb.collection(Collections.Users).delete(userClone.value.id);
};

const onDeleteSuccess = async () => {
  await queryClient.invalidateQueries({ queryKey: [QueryEnumKeys.Users] });
};

const emit = defineEmits<{
  (e: "updated"): void;
}>();
</script>
