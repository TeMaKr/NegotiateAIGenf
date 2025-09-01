<template>
  <v-container class="py-12">
    <v-row class="justify-center">
      <v-col cols="12" sm="11" md="9" lg="8" xl="7">
        <div class="d-flex justify-space-between align-center mb-4">
          <v-btn
            :to="{ name: 'DocumentList', query: { ...route.query } }"
            color="primary"
            variant="tonal"
            prepend-icon="mdi-arrow-left"
            size="small"
            rounded="lg"
          >
            Back to Submission Browser
          </v-btn>
        </div>
        <div class="d-flex justify-space-between align-center">
          <div v-if="isQueryError"></div>

          <div v-if="isQueryFetching"></div>

          <div v-if="!!document" class="w-100">
            <h1 class="mb-2">{{ document.title }}</h1>

            <div class="mb-4">
              <template v-if="document.file">
                <v-btn
                  :href="document.file"
                  target="_blank"
                  rounded="lg"
                  color="primary"
                  prepend-icon="mdi-file-document"
                >
                  Open document file
                </v-btn>
              </template>
              <template v-else>
                <v-chip rounded="lg" class="mr-1" color="error">
                  <v-icon icon="mdi-file-document" class="mr-1"></v-icon>
                  No file provided
                </v-chip>
              </template>
            </div>

            <v-table class="rounded-lg border">
              <tbody>
                <tr>
                  <td class="text-medium-emphasis">
                    Delegations/Groups of States
                  </td>
                  <td>
                    <v-chip-group column>
                      <v-chip
                        v-for="author in document.expand?.author || []"
                        size="small"
                        rounded="lg"
                      >
                        {{ author.name }}
                      </v-chip>
                    </v-chip-group>
                  </td>
                </tr>
                <tr>
                  <td class="text-medium-emphasis w-33">Session</td>
                  <td>
                    <v-chip size="small" rounded="lg">
                      {{ document.session }}
                    </v-chip>
                  </td>
                </tr>
                <tr>
                  <td class="text-medium-emphasis w-33">Original source</td>
                  <td>
                    <v-chip
                      v-if="!!document.href"
                      size="small"
                      rounded="lg"
                      :href="document.href"
                      target="_blank"
                    >
                      Link to original source
                    </v-chip>
                    <v-chip v-else size="small" rounded="lg" color="error">
                      Link missing
                    </v-chip>
                  </td>
                </tr>
                <tr>
                  <td class="text-medium-emphasis">Topics</td>
                  <td>
                    <v-chip-group column>
                      <v-chip
                        v-for="topic in document.expand?.topic || []"
                        size="small"
                        rounded="lg"
                      >
                        {{ topic?.name }}
                      </v-chip>
                    </v-chip-group>
                  </td>
                </tr>
                <tr>
                  <td class="text-medium-emphasis">Document type</td>
                  <td>
                    <v-chip size="small" rounded="lg">
                      {{ document.document_type }}
                    </v-chip>
                  </td>
                </tr>
                <tr>
                  <td class="text-medium-emphasis">Verified</td>
                  <td>
                    <v-chip
                      :color="
                        document.verified === true ? 'success' : 'warning'
                      "
                      size="small"
                      rounded="lg"
                    >
                      {{
                        document.verified === true ? "Verified" : "Not verified"
                      }}
                    </v-chip>
                  </td>
                </tr>
                <tr>
                  <td class="text-medium-emphasis">Created</td>
                  <td>
                    <v-tooltip location="bottom">
                      <template #activator="{ props }">
                        <span v-bind="props">
                          {{ dayjs(document.created).fromNow() }}
                        </span>
                      </template>
                      {{ dayjs(document.created).format("LLL") }}
                    </v-tooltip>
                  </td>
                </tr>
                <tr>
                  <td class="text-medium-emphasis">Updated</td>
                  <td>
                    <v-tooltip location="bottom">
                      <template #activator="{ props }">
                        <span v-bind="props">
                          {{ dayjs(document.updated).fromNow() }}
                        </span>
                      </template>
                      {{ dayjs(document.updated).format("LLL") }}
                    </v-tooltip>
                  </td>
                </tr>
              </tbody>
            </v-table>

            <h2 class="mt-2">Description</h2>
            <p class="text-body-2 text-medium-emphasis mb-6">
              {{ document.description }}
            </p>

            <span class="mr-2"
              ><document-upload-dialog :document="document">
                <template #activator="{ props }">
                  <v-btn
                    v-bind="props"
                    class="mt-2"
                    variant="flat"
                    color="primary"
                    rounded="lg"
                  >
                    <v-icon icon="mdi-upload" class="mr-1"></v-icon>
                    Upload
                  </v-btn>
                </template>
              </document-upload-dialog></span
            >
            <span
              ><document-edit-dialog :document="document">
                <template #activator="{ props }">
                  <v-btn
                    v-bind="props"
                    class="mt-2"
                    variant="flat"
                    color="primary"
                    rounded="lg"
                  >
                    <v-icon icon="mdi-pencil" class="mr-1"></v-icon>
                    Edit
                  </v-btn>
                </template>
              </document-edit-dialog></span
            >
          </div>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { Collections, pb, QueryEnumKeys } from "@/composables/pocketbase";
import { useQuery } from "@tanstack/vue-query";
import { computed } from "vue";
import { useRoute } from "vue-router";
import dayjs from "@/plugins/dayjs";
import DocumentEditDialog from "@/components/DocumentEditDialog.vue";
import DocumentUploadDialog from "@/components/DocumentUploadDialog.vue";
import type {
  AuthorsResponse,
  SubmissionsResponse,
  TopicsResponse,
} from "@/composables/pocketbase/types";

const route = useRoute();

const submissionId = computed(() => route.params.id.toString());

interface SubmissionsDetailsResponse extends SubmissionsResponse {
  expand?: {
    author?: AuthorsResponse[];
    topic?: TopicsResponse[];
  };
}

const {
  data: document,
  isFetching: isQueryFetching,
  isError: isQueryError,
} = useQuery<SubmissionsDetailsResponse>({
  queryKey: [QueryEnumKeys.Submissions, submissionId],
  queryFn: async () => {
    const response = await pb
      .collection(Collections.Submissions)
      .getOne<SubmissionsDetailsResponse>(submissionId.value, {
        expand: "author,topic",
      });
    response.file = pb.files.getURL(response, response.file);
    return response;
  },
});
</script>
