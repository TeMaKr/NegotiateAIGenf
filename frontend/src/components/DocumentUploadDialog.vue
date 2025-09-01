<template>
  <v-dialog v-if="isAuthenticated" v-model="isOpen" max-width="600" persistent>
    <template v-slot:activator="{ props }">
      <slot :props="props" name="activator"></slot>
    </template>

    <v-card title="Upload Document File">
      <v-form v-model="isFormValid" ref="form">
        <v-card-text>
          <div class="mb-2">
            <v-file-input
              v-model="file"
              label="Please upload a document file"
              variant="outlined"
              append-inner-icon="mdi-upload"
              accept="application/pdf"
              prepend-icon=""
              :rules="attachmentsRules"
            />
          </div>
        </v-card-text>

        <v-expand-transition>
          <v-alert v-if="isMutateError" type="error" tile>
            {{ mutateErrorMessage }}
          </v-alert>
        </v-expand-transition>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn rounded="lg" color="surface-2" @click="isOpen = false">
            Cancel
          </v-btn>
          <v-btn
            :loading="isMutatePending"
            :disabled="!isFormValid"
            rounded="lg"
            variant="flat"
            @click="mutate"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import {
  Collections,
  pb,
  QueryEnumKeys,
  usePocketBase,
} from "@/composables/pocketbase";
import type { SubmissionsResponse } from "@/composables/pocketbase/types";
import { useSnackbarQueueStore } from "@/stores/snackbar-queue";
import { useMutation, useQueryClient } from "@tanstack/vue-query";
const props = defineProps<{
  document: SubmissionsResponse;
}>();

const store = useSnackbarQueueStore();
const queryClient = useQueryClient();

const file = ref<File>();

const updateDocument = async () => {
  return await pb
    .collection(Collections.Submissions)
    .update(props.document.id, { file: file.value });
};

const successFn = async (data: SubmissionsResponse) => {
  queryClient.invalidateQueries({
    queryKey: [QueryEnumKeys.Submissions, props.document.id],
  });

  store.appendSuccess(`Document "${data.title}" uploaded successfully`);
};

const attachmentsRules = [
  (v: File) => !!v || "File is required",
  (v: File) => v.size < 5 * 1024 * 1024 || "File size must be less than 5MB",
];

const { isAuthenticated } = await usePocketBase();

const isOpen = ref(false);
const isFormValid = ref(false);
const form = useTemplateRef("form");

const mutateErrorMessage =
  "'The document file could not be uploaded. Please try again later.'";

const {
  mutate,
  isError: isMutateError,
  isPending: isMutatePending,
} = useMutation({
  mutationFn: updateDocument,
  onSuccess: async (data) => {
    isOpen.value = false;
    form.value?.reset();
    await successFn(data);
  },
});
</script>
