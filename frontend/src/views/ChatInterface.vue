<template>
  <v-row>
    <v-col cols="12" md="10" lg="10" xl="8" class="mx-auto">
      <v-container class="py-12">
        <app-alert :is-alert="isSubmissionError">
          Submission could not be loaded.
        </app-alert>
        <h1 class="fontsize-h2 mt-12 mb-10 underlined-header">
          Submissions Analyser
        </h1>
        <p class="mb-4 text-body-1 text-grey-darken-2">
          The Submissions Analyser simplifies the search and analysis of
          documents submitted by delegations and Groups of States, enabling
          delegates and other stakeholders to quickly identify crucial
          information. With an intuitive interface, the tool supports
          treaty-specific queries and provides direct links to relevant
          submissions for deeper exploration. Due to technical limitations, the
          tool generates responses based on a maximum of seven documents at a
          time. It uses AI to provide answers grounded in publicly available
          negotiation documents. While we strive for accuracy and transparency,
          responses may sometimes be incomplete or imprecise. When in doubt,
          please consult the original documents.
        </p>
        <div class="d-flex align-center mb-2">
          <h2 class="fontsize-h5">Select Filters</h2>
          <v-icon
            v-tooltip:bottom="{
              text: 'You must select at least one Delegation/Groups of States before asking questions. Filtering ensures the system focuses on a manageable subset of documents, enabling more precise and contextually relevant answers',
              maxWidth: 700,
            }"
            color="primary"
            class="ml-1"
          >
            mdi-information-outline
          </v-icon>
        </div>
        <app-filter
          v-model:authors="filterAuthors"
          v-model:sessions="filterSessions"
          v-model:topics="filterTopics"
          :isFilterVerified="false"
          isAuthorsRequired
          class="mb-2"
        />
        <div class="d-flex align-center mb-2">
          <h2 class="fontsize-h5">Ask a question</h2>
          <v-tooltip location="bottom" max-width="700">
            <template v-slot:activator="{ props }">
              <v-icon v-bind="props" color="primary" class="ml-1">
                mdi-information-outline
              </v-icon>
            </template>
            <div>
              <p>
                This feature helps you ask questions about submissions by
                Delegations/Groups of States and quickly find relevant positions
                and information. The system searches through pre-filtered
                in-session documents to provide targeted answers. Please note
                that for each question, the system can only review a limited
                number of document sections. It automatically selects the most
                relevant passages to answer your query.
              </p>
              <br />
              <p><strong>Tips for best results:</strong></p>
              <ul class="ml-4">
                <li>
                  Be precise with your questions and use filters to narrow down
                  submissions
                </li>
                <li>
                  When comparing Delegations or Groups of States, select all
                  relevant parties in your filters
                </li>
                <li>
                  Focused searches provide better quality answers than broad
                  database queries
                </li>
                <li>
                  Each answer includes direct links to source documents for
                  verification and deeper examination
                </li>
              </ul>
            </div>
          </v-tooltip>
        </div>
        <v-textarea
          v-model="query"
          variant="solo"
          placeholder="Please enter your question"
          persistent-placeholder
          :rules="queryRule"
          rows="5"
          bg-color="white"
          auto-grow
          counter
          persistent-counter
          class="mb-2"
        >
          <template v-slot:counter="{ counter }">
            {{ counter }} / 250 characters
          </template>
          <template #append-inner>
            <div
              v-tooltip:bottom="
                filterAuthors.length < 1 || !query
                  ? 'Please select delegations/group of states and provide a question.'
                  : 'Submit question'
              "
              style="height: 100%; cursor: pointer"
              class="d-flex flex-column justify-end align-end pb-3"
            >
              <v-btn
                color="primary"
                text="Send"
                prepend-icon="mdi-send"
                :disabled="!query || filterAuthors.length < 1"
                :loading="isQueryLoading"
                @click="querySubmissions()"
              />
            </div>
          </template>
        </v-textarea>

        <v-row class="mb-8">
          <v-col cols="12" sm="4">
            <v-card
              variant="tonal"
              color="primary"
              class="mx-auto"
              @click="
                query = exampleQuestionOne;
                isDialog = false;
              "
            >
              <v-card-item class="text-caption text-primary">
                <v-row>
                  <v-col cols="2" class="d-flex align-center">
                    <v-icon>mdi-help-circle-outline</v-icon>
                  </v-col>
                  <v-col cols="10">
                    <p>
                      {{ exampleQuestionOne }}
                    </p>
                  </v-col>
                </v-row>
              </v-card-item>
            </v-card>
          </v-col>
          <v-col cols="12" sm="4">
            <v-card
              variant="tonal"
              color="primary"
              class="mx-auto"
              @click="
                query = exampleQuestionTwo;
                isDialog = false;
              "
            >
              <v-card-item class="text-caption text-primary">
                <v-row>
                  <v-col cols="2" class="d-flex align-center">
                    <v-icon>mdi-help-circle-outline</v-icon>
                  </v-col>
                  <v-col cols="10">
                    <p>
                      {{ exampleQuestionTwo }}
                    </p>
                  </v-col>
                </v-row>
              </v-card-item>
            </v-card>
          </v-col>
          <v-col cols="12" sm="4">
            <v-card
              variant="tonal"
              color="primary"
              class="mx-auto"
              @click="
                query = exampleQuestionThree;
                isDialog = false;
              "
            >
              <v-card-item class="text-caption text-primary">
                <v-row>
                  <v-col cols="2" class="d-flex align-center">
                    <v-icon>mdi-help-circle-outline</v-icon>
                  </v-col>
                  <v-col cols="10">
                    <p>
                      {{ exampleQuestionThree }}
                    </p>
                  </v-col>
                </v-row>
              </v-card-item>
            </v-card>
          </v-col>
        </v-row>

        <app-alert
          class="mb-4"
          :closable="false"
          :is-alert="
            typeof isQueryError === 'object'
              ? isQueryError.message
              : isQueryError
          "
          :type="typeof isQueryError === 'object' ? isQueryError.type : 'error'"
        >
          {{
            typeof isQueryError === "object"
              ? isQueryError.message
              : isQueryError
          }}
        </app-alert>

        <v-card
          v-if="generateResponses || isQueryLoading"
          flat
          variant="tonal"
          color="primary"
          min-height="300"
          class="d-flex align-center"
        >
          <v-card-text v-if="isQueryLoading" id="response">
            <v-skeleton-loader type="article" height="250" width="100%" />
          </v-card-text>
          <v-card-text v-if="!isQueryLoading" id="response">
            <v-chip
              variant="outlined"
              size="small"
              rounded="lg"
              color="primary"
              prepend-icon="mdi-creation"
              class="mb-4"
            >
              <p>Powered by <strong>GPT-4</strong></p>
            </v-chip>
            <div class="d-flex align-center mb-4">
              <h3 class="fontsize-h6 text-black mr-2">Answer</h3>
              <v-btn
                :icon="expandAnswer ? 'mdi-chevron-up' : 'mdi-chevron-down'"
                @click="expandAnswer = !expandAnswer"
              />
            </div>
            <v-expand-transition>
              <p v-if="expandAnswer" class="mb-4 text-black">
                {{ generateResponses?.answer }}
              </p>
            </v-expand-transition>

            <div class="d-flex align-center mb-4">
              <h3 class="fontsize-h6 text-black mr-2">References</h3>
              <v-btn
                :icon="expandReferences ? 'mdi-chevron-up' : 'mdi-chevron-down'"
                @click="expandReferences = !expandReferences"
              />
            </div>
            <v-expand-transition>
              <div v-if="expandReferences">
                <ul class="ml-8">
                  <li
                    v-for="(reference, index) in generateResponses?.references"
                    :key="index"
                  >
                    <p v-if="reference.retriever_id" class="ml-1 text-black">
                      [{{ reference?.retriever_id }}]:
                      <a
                        :href="reference.href"
                        target="_blank"
                        class="text-primary"
                        style="word-break: break-word !important"
                      >
                        {{ reference.href }}
                      </a>
                    </p>
                  </li>
                </ul>
              </div>
            </v-expand-transition>

            <div class="d-flex align-center mb-4">
              <h3 class="fontsize-h6 text-black mr-2">Reference Excerpts</h3>
              <v-tooltip location="bottom" max-width="400">
                <template v-slot:activator="{ props }">
                  <v-icon
                    v-bind="props"
                    color="primary"
                    class="mr-2"
                    size="small"
                  >
                    mdi-information-outline
                  </v-icon>
                </template>
                <span
                  >These are the submission sections the AI referenced to
                  generate your answer. Review these original passages to verify
                  the response and gain deeper insight into the source material.
                </span>
              </v-tooltip>
              <v-btn
                :icon="expandNotes ? 'mdi-chevron-up' : 'mdi-chevron-down'"
                @click="expandNotes = !expandNotes"
              />
            </div>
            <v-expand-transition>
              <div v-if="expandNotes">
                <div
                  v-for="(chunks, submissionId) in generateResponses?.context"
                  :key="submissionId"
                  class="mb-4"
                >
                  <v-chip rounded="lg" color="secondary">
                    <p class="text-grey-darken-2">
                      <strong>Submission: {{ submissionId }}</strong>
                    </p>
                  </v-chip>
                  <p
                    v-for="chunk in chunks"
                    :key="chunk"
                    class="text-black mb-2"
                    style="word-break: break-word !important"
                  >
                    {{ chunk }}
                  </p>
                </div>
              </div>
            </v-expand-transition>
          </v-card-text>
        </v-card>
      </v-container>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import apiClient from "@/plugins/api-client";
import { ref, computed, watch } from "vue";
import {
  Collections,
  SubmissionsSessionOptions,
  type SubmissionsResponse,
  type AuthorsResponse,
  type TopicsResponse,
} from "@/composables/pocketbase/types";
import { pb, QueryEnumKeys } from "@/composables/pocketbase";
import { useQuery } from "@tanstack/vue-query";
import type {
  QuerySubmissionOut,
  SubmissionDataDetail,
  QuerySubmissionIn,
} from "@/services";
import { useGoTo } from "vuetify";

const goTo = useGoTo();

const generateResponses = ref<QuerySubmissionOut>();
const query = ref("");
const filterSessions = ref<SubmissionsSessionOptions[]>([]);
const filterAuthors = ref<string[]>([]);
const filterTopics = ref<string[]>([]);
const isDialog = ref<boolean>(false);
const exampleQuestionOne =
  "Do the selected countries prefer a top-down instrument?";
const exampleQuestionTwo =
  "What measures do SIDS and PSIDS propose to reduce existing plastic pollution?";
const exampleQuestionThree =
  "Which of the selected countries prefer a global approach to regulate plastic products?";
const isQueryError = ref();
const isQueryLoading = ref(false);
const expandAnswer = ref(true);
const expandNotes = ref(false);
const expandReferences = ref(false);

const queryRule = [(v: string) => v.length <= 250 || "Max. 250 characters"];

const submissionMetadata = computed(
  (): Record<string, SubmissionDataDetail> => {
    const metadata: Record<string, SubmissionDataDetail> = {};
    submissions.value.forEach((submission) => {
      metadata[submission.retriever_id] = {
        authors: submission.expand?.author?.map((author) => author.name) || [],
        topics: submission.expand?.topic?.map((topic) => topic.name) || [],
      };
    });
    return metadata;
  },
);

const querySubmissions = async () => {
  isQueryError.value = undefined;
  if (filterAuthors.value.length < 1) {
    isQueryError.value =
      "Please select at least one Delegation/Group of States.";
    return;
  }
  if (Object.keys(submissionMetadata.value).length < 1) {
    isQueryError.value = {
      message:
        "No submissions found for the selected filters. Please adjust your filters. You can find all available submissions in the Submission Browser. Note that in the Submission Analyser only in-session documents are available for Q&A.",
      type: "info",
    };
    return;
  }
  isQueryLoading.value = true;
  try {
    const response =
      await apiClient.aiTools.querySubmissionApiQuerySubmissionPost({
        submission_metadata: submissionMetadata.value,
        question: query.value,
      });
    generateResponses.value = response;
    return response;
  } catch (error) {
    isQueryError.value = "Response could not be loaded.";
  } finally {
    isQueryLoading.value = false;
    goTo("#response");
  }
};

const { data: submissions, isError: isSubmissionError } = useQuery({
  queryKey: [
    QueryEnumKeys.Submissions,
    filterSessions,
    filterAuthors,
    filterTopics,
  ],
  queryFn: async () => {
    let filterString = "";
    let params: { [key: string]: any } = {};
    filterString += "(verified = {:verified})";
    params.verified = true;
    filterString += " && (document_type = {:document_type})";
    params.document_type = "insession document";
    const filterMap = [
      {
        value: filterSessions.value,
        field: "session",
      },
      {
        value: filterAuthors.value,
        field: "author",
      },
      {
        value: filterTopics.value,
        field: "topic",
      },
    ];

    filterMap.forEach(({ value, field }) => {
      if (value.length) {
        if (filterString.length > 0) {
          filterString += " && ";
        }
        filterString += "(";
        value.forEach((item, index) => {
          if (index > 0) {
            filterString += " || ";
          }
          filterString += `(${field}:each ?= {:${field}${index}})`;
          params[`${field}${index}`] = item;
        });
        filterString += ")";
      }
    });
    return await pb.collection(Collections.Submissions).getFullList<
      SubmissionsResponse & {
        expand?: {
          author?: AuthorsResponse[];
          topic?: TopicsResponse[];
        };
      }
    >({
      filter: pb.filter(filterString, params),
      expand: "author,topic",
    });
  },
  initialData: [],
});

// Reset isQueryError when any filter changes
watch([filterAuthors, filterSessions, filterTopics], () => {
  isQueryError.value = undefined;
});
</script>

<style scoped>
.underlined-header {
  text-decoration: underline;
  text-decoration-color: #09677f;
  text-decoration-thickness: 4px;
  text-underline-offset: 8px;
}
</style>
