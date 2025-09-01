<template>
  <v-dialog v-if="isAuthenticated" v-model="isOpen" max-width="600" persistent>
    <template v-slot:activator="{ props }">
      <slot :props="props" name="activator"></slot>
    </template>
    <v-card :title="props.title">
      <v-form v-model="isFormValid" ref="form">
        <v-card-text>
          <v-text-field
            v-model="document.title"
            label="Title"
            :rules="[(v) => !!v || 'Please enter a title']"
            variant="solo-filled"
            flat
          ></v-text-field>

          <v-text-field
            v-model="document.description"
            label="Description"
            variant="solo-filled"
            :rules="[(v) => !!v || 'Please enter a description']"
            flat
          ></v-text-field>

          <div class="mb-2">
            <AppDocumentTypeAutoComplete
              v-model="document.document_type"
              :rules="[
                (v: SubmissionsDocumentTypeOptions) =>
                  !!v || 'Please select a document type',
              ]"
            ></AppDocumentTypeAutoComplete>
          </div>

          <div class="mb-2">
            <AppAuthorsAutoComplete
              v-model="document.author"
              :rules="[
                (v: AuthorsResponse[]) =>
                  v.length > 0 ||
                  'Please select at least one Delegation/Group of States',
              ]"
            ></AppAuthorsAutoComplete>
          </div>

          <div class="mb-2">
            <AppSessionAutoComplete
              v-model="document.session"
              :rules="[
                (v: SubmissionsSessionOptions) =>
                  !!v || 'Please select a session',
              ]"
            ></AppSessionAutoComplete>
          </div>

          <div class="mb-2">
            <v-text-field
              v-model="document.href"
              label="Original Source"
              variant="solo-filled"
              :rules="[
                (v) =>
                  (!!v && validator.isURL(v)) || 'Please enter a valid url',
              ]"
              flat
            ></v-text-field>
          </div>
          <div class="mb-2">
            <AppTopicsAutoComplete
              v-model="document.topic"
              :rules="[
                (v: TopicsResponse[]) =>
                  v.length > 0 || 'Please select at least one topic',
              ]"
            ></AppTopicsAutoComplete>
          </div>

          <template v-if="hasFile">
            <div class="mb-2">
              <p class="text-caption">
                Verification State
                <v-tooltip>
                  <template #activator="{ props }">
                    <v-icon
                      v-bind="props"
                      size="16"
                      color="primary"
                      class="mb-1"
                      style="vertical-align: middle"
                    >
                      mdi-information-outline
                    </v-icon>
                  </template>
                  <span>
                    Please note that vectors are created for all sessions if
                    document is set to Verified. For sessions 5 and above in
                    addition the augmentation process is started.
                  </span>
                </v-tooltip>
              </p>
              <v-chip-group v-model="document.verified" mandatory>
                <v-chip :value="true" size="small" rounded="lg" color="success">
                  Verified
                </v-chip>
                <v-chip
                  :value="false"
                  size="small"
                  rounded="lg"
                  color="warning"
                >
                  Not verified
                </v-chip>
              </v-chip-group>
            </div>
          </template>
          <template v-else>
            <p>Please upload a file to set the verification state.</p>
          </template>
        </v-card-text>

        <v-expand-transition>
          <v-alert v-if="isMutateError" type="error" tile>
            {{ props.mutateErrorMessage }}
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
import { usePocketBase } from "@/composables/pocketbase";
import type {
  AuthorsResponse,
  SubmissionsDocumentTypeOptions,
  SubmissionsRecord,
  SubmissionsResponse,
  SubmissionsSessionOptions,
  TopicsResponse,
} from "@/composables/pocketbase/types";
import { useMutation } from "@tanstack/vue-query";
import { ref, useTemplateRef } from "vue";
import validator from "validator";

const { isAuthenticated } = await usePocketBase();

const isOpen = ref(false);
const isFormValid = ref(false);
const form = useTemplateRef("form");

const document = defineModel<SubmissionsRecord>("document", { required: true });

const props = withDefaults(
  defineProps<{
    title: string;
    mutateErrorMessage: string;
    mutationFn: () => Promise<SubmissionsResponse>;
    resetFormOnSuccess?: boolean;
    successFn: (data: SubmissionsResponse) => Promise<void>;
    hasFile?: boolean;
  }>(),
  {
    resetFormOnSuccess: true,
    hasFile: false,
  },
);

const {
  mutate,
  isError: isMutateError,
  isPending: isMutatePending,
} = useMutation({
  mutationFn: props.mutationFn,
  onSuccess: async (data) => {
    isOpen.value = false;
    if (props.resetFormOnSuccess) {
      form.value?.reset();
    }
    await props.successFn(data);
  },
});
</script>
