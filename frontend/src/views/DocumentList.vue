<template>
  <v-row>
    <v-col cols="12" md="10" lg="10" xl="8" class="mx-auto">
      <v-container class="py-12">
        <h1 class="fontsize-h2 mt-12 mb-10 underlined-header">
          Submissions Browser
        </h1>
        <p class="mb-2 text-body-1 text-grey-darken-2">
          This document list provides access to the official submissions of the
          Intergovernmental Negotiating Committee on Plastic Pollution (INC).
          Documents can be filtered by Delegations/Groups of States, session or
          topics and searched by title. Click on the items in the list for a
          detailed view with metadata and direct access to PDF files.
        </p>
        <p class="mb-2 text-body-1 text-grey-darken-2">
          <strong>Data Source: </strong>The dataset includes official documents
          of the INC, including contributions of INC members (written statements
          and in-session documents) to all sessions held so far. Observer
          documents are excluded. The dataset is constantly updated, with
          verified documents from ongoing rounds being added after manual review
          by our team.
        </p>
        <v-row class="justify-center">
          <v-col cols="12" sm="11" md="9" lg="12">
            <div class="d-flex align-center mb-8">
              <document-create-dialog>
                <template #activator="{ props }">
                  <v-btn
                    v-bind="props"
                    color="primary"
                    prepend-icon="mdi-plus"
                    variant="elevated"
                  >
                    Create New Document
                  </v-btn>
                </template>
              </document-create-dialog>
            </div>

            <v-text-field
              v-model="search"
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              placeholder="Search documents..."
              class="mb-8"
              hide-details
              clearable
            ></v-text-field>

            <app-filter
              v-model:authors="filterAuthors"
              v-model:sessions="filterSessions"
              v-model:topics="filterTopics"
              v-model:verified="filterVerified"
              :isFilterVerified="isAuthenticated"
              class="flex-grow-1"
            />

            <div v-if="isQueryFetching">
              <v-skeleton-loader
                color="transparent"
                type="heading"
                class="my-2"
              ></v-skeleton-loader>

              <v-skeleton-loader
                color="transparent"
                type="heading"
                class="my-2"
              ></v-skeleton-loader>

              <v-skeleton-loader
                color="transparent"
                type="heading"
                class="my-2"
              ></v-skeleton-loader>
            </div>

            <div v-else-if="isQueryError">
              <p class="text-medium-emphasis">
                An error occurred while fetching documents. Please try again
                later. If the problem persists, please contact support.
              </p>
            </div>

            <div v-else-if="submissions.length > 0">
              <list-document-item
                v-for="submission in submissions"
                :key="submission.id"
                :submission="submission"
              ></list-document-item>
              <v-pagination
                v-model="page"
                :length="totalPages"
                class="mt-6"
                size="small"
                rounded
                @update:model-value="
                  router.push({
                    query: {
                      ...route.query,
                      page: page,
                    },
                  })
                "
              ></v-pagination>
            </div>

            <div v-else class="text-center my-12">
              <p class="text-medium-emphasis">
                No documents found matching the search criteria.
              </p>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import {
  Collections,
  pb,
  QueryEnumKeys,
  usePocketBase,
} from "@/composables/pocketbase";
import {
  SubmissionsSessionOptions,
  type AuthorsResponse,
  type SubmissionsResponse,
  type TopicsResponse,
} from "@/composables/pocketbase/types";
import { useQuery } from "@tanstack/vue-query";
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import ListDocumentItem from "@/components/ListDocumentItem.vue";

const route = useRoute();
const router = useRouter();

const { isAuthenticated } = await usePocketBase();
const search = ref("");
const filterSessions = ref<SubmissionsSessionOptions[]>([]);
const filterAuthors = ref<string[]>([]);
const filterTopics = ref<string[]>([]);
const filterVerified = ref<boolean | null>(null);
const isMounted = ref(false);

const page = ref();
const totalPages = ref(0);

const {
  data: submissions,
  isFetching: isQueryFetching,
  isError: isQueryError,
} = useQuery({
  queryKey: [
    QueryEnumKeys.Submissions,
    page,
    search,
    filterSessions,
    filterAuthors,
    filterTopics,
    filterVerified,
  ],
  queryFn: async () => {
    let filterString = "";
    let params: { [key: string]: any } = {};

    // Handle verification for authenticated users and public
    if (isAuthenticated.value) {
      if (filterVerified.value !== null) {
        filterString += `(verified = {:verified})`;
        params.verified = filterVerified.value;
      }
    } else {
      filterString += "(verified = {:verified})";
      params.verified = true;
    }

    // Add search filter
    if (search.value && search.value.length > 0) {
      if (filterString.length > 0) {
        filterString += " && ";
      }
      filterString += `(title ~ {:title})`;
      params.title = search.value;
    }

    // Add filters for sessions, authors, and topics
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

    const response = await pb.collection(Collections.Submissions).getList<
      SubmissionsResponse & {
        expand?: {
          author?: AuthorsResponse[];
          topic?: TopicsResponse[];
        };
      }
    >(page.value, 15, {
      filter: pb.filter(filterString, params),
      expand: "author,topic",
      sort: "author.type,author.name",
    });

    if (totalPages.value !== response.totalPages) {
      page.value = 1;
      router.push({
        query: {
          ...route.query,
          page: 1,
        },
      });
    }
    totalPages.value = response.totalPages;

    return response.items;
  },
  initialData: [],
  enabled: isMounted,
});

onMounted(() => {
  page.value = route.query.page ? parseInt(route.query.page as string) : 1;
  isMounted.value = true;
});
</script>

<style>
.custom-chip .label {
  position: relative;
}

.custom-chip .label::before {
  content: " ";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgb(var(--v-theme-primary));
  opacity: 0.4;
  border-top-right-radius: 8px;
  border-bottom-right-radius: 8px;
}

.custom-chip .label a:visited {
  color: rgb(var(--v-theme-on-primary));
}

.underlined-header {
  text-decoration: underline;
  text-decoration-color: #09677f;
  text-decoration-thickness: 4px;
  text-underline-offset: 8px;
}
</style>
