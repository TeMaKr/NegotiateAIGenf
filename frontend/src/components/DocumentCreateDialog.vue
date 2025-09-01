<template>
  <v-dialog v-if="isAuthenticated" v-model="isOpen" max-width="600" persistent>
    <template v-slot:activator="{ props }">
      <slot :props="props" name="activator"></slot>
    </template>
    <v-card title="Create document">
      <v-form v-model="isFormValid" ref="form">
        <v-card-text>
          <v-text-field
            v-model="title"
            label="Title"
            :rules="[(v) => !!v || 'Please enter a title']"
            variant="solo-filled"
            flat
          ></v-text-field>

          <v-text-field
            v-model="description"
            label="Description"
            variant="solo-filled"
            :rules="[(v) => !!v || 'Please enter a description']"
            flat
          ></v-text-field>

          <div class="mb-2">
            <AppDocumentTypeAutoComplete
              v-model="documentType"
              :rules="[
                (v: SubmissionsDocumentTypeOptions) =>
                  !!v || 'Please select a document type',
              ]"
            ></AppDocumentTypeAutoComplete>
          </div>

          <div class="mb-2">
            <AppAuthorsAutoComplete
              v-model="author"
              :rules="[
                (v: AuthorsResponse[]) =>
                  v.length > 0 ||
                  'Please select at least one Delegation/Group of States',
              ]"
            ></AppAuthorsAutoComplete>
          </div>

          <div class="mb-2">
            <AppSessionAutoComplete
              v-model="session"
              :rules="[
                (v: SubmissionsSessionOptions) =>
                  !!v || 'Please select a session',
              ]"
            ></AppSessionAutoComplete>
          </div>

          <div class="mb-2">
            <AppTopicsAutoComplete
              v-model="topic"
              :rules="[
                (v: TopicsResponse[]) =>
                  v.length > 0 || 'Please select at least one topic',
              ]"
            ></AppTopicsAutoComplete>
          </div>

          <div class="mb-2">
            <v-text-field
              v-model="href"
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
            <v-chip-group v-model="verified" mandatory>
              <v-chip :value="true" size="small" rounded="lg" color="success">
                Verified
              </v-chip>
              <v-chip :value="false" size="small" rounded="lg" color="warning">
                Not verified
              </v-chip>
            </v-chip-group>
          </div>
          <div class="mb-2">
            <p class="text-caption">File upload</p>
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
            <span> The document could not be created. </span>
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
import {
  SubmissionsDocumentTypeOptions,
  SubmissionsSessionOptions,
  type AuthorsResponse,
  type SubmissionsResponse,
  type TopicsResponse,
} from "@/composables/pocketbase/types";
import { useSnackbarQueueStore } from "@/stores/snackbar-queue";
import { useMutation, useQueryClient } from "@tanstack/vue-query";
import validator from "validator";

const { isAuthenticated } = await usePocketBase();

const isOpen = ref(false);
const isFormValid = ref(false);
const form = useTemplateRef("form");
const store = useSnackbarQueueStore();
const queryClient = useQueryClient();

const title = ref("");
const description = ref("");
const author = ref<string[]>();
const session = ref<SubmissionsSessionOptions>(
  SubmissionsSessionOptions["E5.2"],
);
const verified = ref<boolean>(false);
const topic = ref<string[]>();
const href = ref<string>("");
const documentType = ref<SubmissionsDocumentTypeOptions>(
  SubmissionsDocumentTypeOptions["insession document"],
);

const file = ref<File>();
const attachmentsRules = [
  (v: File) => !!v || "File is required",
  (v: File) => v.size < 5 * 1024 * 1024 || "File size must be less than 5MB",
];
const {
  mutate,
  isError: isMutateError,
  isPending: isMutatePending,
} = useMutation({
  mutationFn: async () => {
    return await pb.collection(Collections.Submissions).create({
      title: title.value,
      description: description.value,
      author: author.value,
      session: session.value,
      verified: verified.value,
      topic: topic.value,
      file: file.value,
      href: href.value,
      document_type: documentType.value,
    });
  },
  onSuccess: () => {
    isOpen.value = false;
    form.value?.reset();
    async (data: SubmissionsResponse) => {
      queryClient.invalidateQueries({
        queryKey: [QueryEnumKeys.Submissions],
      });
      store.appendSuccess(`Document "${data.title}" created successfully`);
    };
  },
});
</script>
