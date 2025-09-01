<template>
  <v-row>
    <v-col cols="12" md="10" lg="10" xl="8" class="mx-auto">
      <v-container class="py-12">
        <h1 class="fontsize-h2 mt-12 mb-10 underlined-header">
          Advanced Analyser
        </h1>

        <p class="mb-4 text-body-1 text-grey-darken-2">
          Advanced Analyser provides a structured way to explore and compare
          submissions from INC-5.1 and INC-5.2. The tool enables detailed
          comparison of submissions from different Delegations and Groups of
          States on specific treaty topics. For example, you want to compare
          submissions on the topic "plastic products" from session 5.2 to
          analyse what different Delegations and Groups of States propose for
          this topic.
          <br />
        </p>
        <p class="text-body-1 text-grey-darken-2">
          <strong><u>How It Works</u></strong>
        </p>
        <ol class="ml-5 mb-12 text-body-1 text-grey-darken-2">
          <li>
            Select filters: Choose a session and topic with optional filtering
            by specific delegations/groups.
          </li>
          <li>
            View results: A table displays matching submissions (columns) with
            extracted relevant passages for each key element (rows).
          </li>
          <li>
            Compare positions: Select up to three extracted passages of a key
            element to compare the positions of the submissions.
          </li>
          <li>
            Side-by-side comparison and AI summary: Compare the three positions
            and generate an AI summary to identify the most important
            differences and similarities between the selected passages.
          </li>
        </ol>

        <div class="d-flex align-center">
          <h2>
            <span class="fontsize-h5"> Step 1: </span>
            <span class="fontsize-h5-light">Add mandatory(</span>
            <span class="text-primary">*</span>
            <span class="fontsize-h5-light">) filters to proceed</span>
          </h2>
          <v-icon
            v-tooltip:bottom="{
              text: 'Choose a session and a topic, with optional filtering by specific delegations/groups.',
              maxWidth: 700,
            }"
            color="primary"
            class="ml-1"
          >
            mdi-information-outline
          </v-icon>
        </div>
        <v-row class="mb-12">
          <v-col cols="12" sm="4">
            <p class="mb-1"><span class="text-primary">*</span>Add Session</p>
            <v-select
              v-model="session"
              :items="sessions"
              variant="outlined"
              placeholder="Sessions"
              hint="Treaty sessions to find submissions in"
              persistent-hint
              prepend-inner-icon="mdi-format-list-numbered"
              menu-icon="mdi-chevron-down"
              density="compact"
              bg-color="white"
              color="primary"
              chips
              @update:model-value="isAnalyze = false"
            >
              <template #chip="{ item }">
                <v-chip rounded="lg">
                  <p class="text-grey-darken-2">
                    <strong>{{ item.title }}</strong>
                  </p>
                </v-chip>
              </template>
            </v-select>
          </v-col>
          <v-col cols="12" sm="4">
            <p class="mb-1"><span class="text-primary">*</span>Add Topic</p>
            <v-autocomplete
              v-model="topic"
              :items="topics"
              item-title="name"
              variant="outlined"
              placeholder="Topics"
              persistent-hint
              prepend-inner-icon="mdi-message-text-outline"
              menu-icon="mdi-chevron-down"
              density="compact"
              bg-color="white"
              color="primary"
              chips
              return-object
              @update:model-value="isAnalyze = false"
            >
              <template #chip="{ item }">
                <v-chip rounded="lg">
                  <p class="text-grey-darken-2">
                    <strong>{{ item.title }}</strong>
                  </p>
                </v-chip>
              </template>
              <template #details>
                <div class="v-messages__message">
                  <span class="text-grey">Submission topics</span>
                  <span class="text-grey font-italic">
                    - See the
                    <a
                      href="/treaty-explorer"
                      target="_blank"
                      class="text-primary"
                      >draft treaty explorer</a
                    >
                    for more details on the topics' structure.
                  </span>
                </div>
              </template>
            </v-autocomplete>
          </v-col>
          <v-col cols="12" sm="4">
            <p class="mb-1">Optional: Limit Results</p>
            <v-autocomplete
              v-model="authors"
              :items="authorsResponse"
              item-title="name"
              item-value="id"
              variant="outlined"
              placeholder="Delegation/Groups of States"
              hint="Specific delegation/Groups of States"
              persistent-hint
              prepend-inner-icon="mdi-account-group-outline"
              menu-icon="mdi-chevron-down"
              density="compact"
              bg-color="white"
              color="primary"
              :disabled="!session || !topic"
              chips
              multiple
              clearable
              @update:model-value="isAnalyze = false"
            >
              <template #chip="{ item }">
                <v-chip rounded="lg">
                  <p class="text-grey-darken-2">
                    <strong>{{ item.title }}</strong>
                  </p>
                </v-chip>
              </template>
            </v-autocomplete>
          </v-col>
          <v-col cols="12" class="d-flex justify-end">
            <v-btn
              color="primary"
              text="Analyse Now"
              :disabled="!topic || !session"
              @click="isAnalyze = true"
            />
          </v-col>
          <v-col cols="12">
            <app-alert
              :is-alert="tableItems.length < 1 && isAnalyze"
              type="info"
              color="warning"
            >
              No key elements have been created for the selected topic yet. To
              view or compare submissions related to this topic, please use the
              Submission Analyser or the Submissions Browser.
            </app-alert>
          </v-col>
        </v-row>

        <div
          :style="tableItems.length < 1 || !isAnalyze ? { opacity: 0.6 } : {}"
          :class="['mb-12', { 'fullscreen-table': isFullscreen }]"
        >
          <div class="d-flex align-center">
            <h2>
              <span class="fontsize-h5"> Step 2: </span>
              <span class="fontsize-h5-light">
                Select extracted passages to compare ({{
                  selectedCellsData.length
                }}/3)
              </span>
            </h2>
            <v-icon
              v-tooltip:bottom="{
                text: 'A table displays matching submissions (columns) with extracted relevant passages for each key element (rows). Select up to three extracted passages of a key element to compare the positions of the submissions.',
                maxWidth: 700,
              }"
              color="primary"
              class="ml-1"
            >
              mdi-information-outline
            </v-icon>
          </div>
          <p class="mb-4 text-body-1 text-grey-darken-1">
            <strong>Key elements</strong>: Submissions which are officially
            assigned to articles or thematic areas currently under negotiation,
            such as waste management or product design. To enable deeper
            analysis, each topic is further broken down into manually defined
            Key Elements - analytical categories that highlight specific aspects
            within a topic. These Key Elements serve as focused comparison
            points for analysing delegation positions. They form the basis for
            how the tool organises content.
          </p>
          <v-alert type="warning" class="mb-4">
            This is a prototype tool and uses AI-generated content, which may be
            inaccurate in parts. For example, in document processing,
            strikethrough text from original PDFs is not recognised, so deleted
            content may appear as active items in the table. Always verify the
            information by reviewing the original submission documents directly.
          </v-alert>
          <div class="d-flex align-center mb-1">
            <v-chip
              variant="outlined"
              size="small"
              rounded="lg"
              color="primary"
              prepend-icon="mdi-creation"
            >
              <p>Powered by <strong>GPT-4</strong></p>
            </v-chip>
            <v-spacer />
            <v-btn
              variant="outlined"
              text="Clear Selection"
              color="secondary"
              :disabled="selectedCellsData.length < 1"
              class="mr-2"
              @click="clearSelectedCells"
            />

            <v-btn
              variant="outlined"
              text="Fullscreen"
              :prepend-icon="
                isFullscreen ? 'mdi-fullscreen-exit' : 'mdi-fullscreen'
              "
              color="secondary"
              @click="isFullscreen = !isFullscreen"
              :disabled="tableItems.length < 1"
            />
          </div>

          <v-card
            v-if="tableItems.length < 1 || !isAnalyze"
            variant="text"
            :border="true"
            height="300"
            class="d-flex flex-column"
            style="background-color: white"
          >
            <v-card-title style="height: 50px; background-color: #09677f33" />
            <v-card-text class="d-flex align-center justify-center flex-grow-1">
              <p class="text-center">
                <strong>No Results yet.</strong>
                <br />
                Please choose a fitting Session and topic to see submissions.
              </p>
            </v-card-text>
          </v-card>

          <v-data-table-virtual
            v-else
            :items="tableItems"
            :headers="headers"
            item-value="id"
            height="500"
            fixed-header
            class="custom-table"
          >
            <template v-slot:headers="{ columns }">
              <tr class="header-row">
                <th
                  color="primary"
                  v-for="(column, index) in columns"
                  :key="`header-${index}`"
                  class="header-cell"
                  :style="{ width: column.width, minWidth: column.minWidth }"
                >
                  <div class="d-flex flex-row align-center my-2">
                    <v-chip
                      v-if="(column as CustomDataTableHeader).authorsDisplayed!"
                      v-tooltip:bottom="{
                        text: (column as CustomDataTableHeader).authors,
                        maxWidth: '400px',
                      }"
                      rounded="lg"
                    >
                      <p>
                        <strong>{{
                          (column as CustomDataTableHeader).authorsDisplayed
                        }}</strong>
                      </p>
                    </v-chip>
                    <v-btn
                      v-if="(column as CustomDataTableHeader).link"
                      variant="text"
                      icon="mdi-open-in-new"
                      size="x-small"
                      class="ml-4"
                      @click.stop="
                        showPdf((column as CustomDataTableHeader).link)
                      "
                    >
                    </v-btn>
                  </div>
                  <p class="my-1">
                    <strong v-if="column.value === 'keyElement'">
                      {{ column.title }}
                    </strong>
                    <span v-else class="text-caption text-grey-darken-2">
                      {{ column.title }}
                    </span>
                  </p>
                </th>
              </tr>
            </template>
            <template v-slot:item="{ item, index }">
              <tr>
                <td class="font-weight-bold key-element-cell">
                  {{ item.keyElement }}
                </td>
                <td
                  v-for="submission in submissions"
                  :key="submission.id"
                  class="align-top submission-cell"
                  :class="{
                    'selected-cell': isSelectedCell(
                      submission.id,
                      item.keyElement,
                    ),
                    'disabled-cell': !isCellSelectable(
                      submission.id,
                      item.keyElement,
                    ),
                  }"
                  @click="
                    isCellSelectable(submission.id, item.keyElement) &&
                    toggleCellSelection(submission.id, item.keyElement)
                  "
                >
                  <div class="text-body-2">
                    <template
                      v-if="
                        submission.key_element?.[item.keyElement] &&
                        submission.key_element?.[item.keyElement].length > 2
                      "
                    >
                      <div v-if="!isExpanded(submission.id, item.keyElement)">
                        <div class="d-flex align-center">
                          <span class="flex-grow-1">
                            {{
                              truncateText(
                                submission.key_element[item.keyElement],
                              )
                            }}
                          </span>
                          <v-icon
                            v-if="
                              isSelectedCell(submission.id, item.keyElement)
                            "
                            size="small"
                            color="primary"
                            class="ml-2"
                          >
                            mdi-check-circle
                          </v-icon>
                        </div>
                        <v-btn
                          v-if="
                            submission.key_element[item.keyElement].length > 100
                          "
                          variant="text"
                          size="x-small"
                          color="primary"
                          class="ml-1"
                          @click.stop="
                            toggleExpand(submission.id, item.keyElement)
                          "
                        >
                          Show more
                        </v-btn>
                      </div>
                      <div v-else class="expanded-text">
                        <div class="d-flex align-center mb-2">
                          <span class="flex-grow-1">
                            {{ submission.key_element[item.keyElement] }}
                          </span>
                          <v-icon
                            v-if="
                              isSelectedCell(submission.id, item.keyElement)
                            "
                            size="small"
                            color="primary"
                            class="ml-2"
                          >
                            mdi-check-circle
                          </v-icon>
                        </div>
                        <v-btn
                          variant="text"
                          size="x-small"
                          color="primary"
                          @click.stop="
                            toggleExpand(submission.id, item.keyElement)
                          "
                        >
                          Show less
                        </v-btn>
                      </div>
                    </template>
                    <template v-else>
                      <span class="text-grey">
                        {{
                          replaceEmptyKeyElements(
                            submission.key_element?.[item.keyElement],
                          )
                        }}
                      </span>
                    </template>
                  </div>
                </td>
              </tr>
            </template>
          </v-data-table-virtual>
          <div class="d-flex align-center justify-end">
            <p class="text-caption text-grey">
              Scroll to the right for more submissions
            </p>
            <v-icon size="x-small" color="grey" class="ml-1">
              mdi-chevron-double-right
            </v-icon>
          </div>
        </div>
        <div
          :style="selectedCellsData.length < 1 ? { opacity: 0.6 } : {}"
          class="mb-12"
        >
          <div class="d-flex align-center">
            <h2>
              <span class="fontsize-h5"> Step 3: </span>
              <span class="fontsize-h5-light">
                Compare selected submission elements
              </span>
            </h2>
            <v-icon
              v-tooltip:bottom="{
                text: 'Compare the three positions and generate an AI summary to identify the most important differences and similarities between the selected passages.',
                maxWidth: 700,
              }"
              color="primary"
              class="ml-1"
            >
              mdi-information-outline
            </v-icon>
          </div>
          <v-card
            variant="text"
            width="100%"
            min-height="300"
            :border="true"
            class="d-flex flex-column"
            style="background-color: white"
          >
            <v-card-title class="d-flex align-center">
              <v-chip
                variant="outlined"
                size="small"
                rounded="lg"
                color="primary"
                prepend-icon="mdi-creation"
              >
                <p>Powered by <strong>GPT-4</strong></p>
              </v-chip>
              <v-spacer />
              <v-btn
                variant="outlined"
                text="Clear Selection"
                color="secondary"
                :disabled="selectedCellsData.length < 1"
                class="mr-2"
                @click="clearSelectedCells"
              />
              <div
                v-tooltip:bottom="
                  'Choose at least two of the same Key Elements to create an AI summary.'
                "
                style="cursor: pointer"
              >
                <v-btn
                  color="primary"
                  text="Generate AI-Summary"
                  :disabled="
                    !selectedCellsData.every(
                      (str) =>
                        str.keyElement === selectedCellsData[0].keyElement,
                    ) || selectedCellsData.length < 2
                  "
                  :loading="isMutatePending"
                  @click="mutate()"
                />
              </div>
            </v-card-title>
            <v-divider />
            <v-card-text v-if="selectedCellsData.length > 0" class="pa-0 ma-2">
              <v-row class="align-stretch">
                <v-col
                  v-for="(cellData, index) in selectedCellsData"
                  :key="`${cellData.submissionId}|||${cellData.keyElement}`"
                  :cols="12 / Math.min(selectedCellsData.length, 3)"
                  :style="{
                    borderRight:
                      index < selectedCellsData.length - 1
                        ? '1px solid #e0e0e0'
                        : 'none',
                    borderRadius: 0,
                  }"
                  class="mt-1 d-flex flex-column"
                >
                  <div
                    class="d-flex flex-row justify-space-between align-start mb-2"
                    style="
                      min-height: 100px;
                      display: flex;
                      align-items: flex-start;
                    "
                  >
                    <strong
                      style="
                        max-width: calc(100% - 40px);
                        line-height: 1.2;
                        display: block;
                      "
                    >
                      <p v-if="cellData.submission?.expand.author" class="mb-2">
                        <strong>
                          {{
                            cellData.submission?.expand.author?.length > 1
                              ? cellData.submission?.expand.author?.[0]?.name +
                                ` +${cellData.submission?.expand.author?.length - 1} other Delegations/Groups of States`
                              : cellData.submission?.expand.author?.[0]?.name
                          }}
                        </strong>
                      </p>
                      <p class="text-caption text-grey mb-4">
                        {{ cellData.submission?.title }}
                        <br />
                        {{ cellData.keyElement }}
                      </p>
                    </strong>
                    <v-btn
                      variant="plain"
                      icon="mdi-close"
                      size="small"
                      color="primary"
                      class="flex-shrink-0"
                      @click="
                        removeSelectedCell(
                          cellData.submissionId,
                          cellData.keyElement,
                        )
                      "
                    />
                  </div>
                  <div class="flex-grow-1">
                    {{ cellData.content }}
                  </div>
                </v-col>
                <v-divider v-if="summary"></v-divider>
                <v-col v-if="summary" cols="12">
                  <p class="mb-2">
                    <strong>AI-Summary</strong>
                  </p>
                  <p>
                    {{ summary.summary }}
                  </p>
                </v-col>
                <v-col class="d-flex justify-end">
                  <v-chip
                    variant="outlined"
                    size="small"
                    rounded="lg"
                    color="primary"
                    prepend-icon="mdi-creation"
                  >
                    <p>Powered by <strong>GPT-4</strong></p>
                  </v-chip>
                </v-col>
              </v-row>
            </v-card-text>
            <div v-else class="d-flex align-center justify-center flex-grow-1">
              <v-card-text>
                <p class="text-center">
                  <strong>No Submissions selected.</strong>
                  <br />
                  Select at least one submission to view in this area.
                </p>
              </v-card-text>
            </div>
          </v-card>
        </div>
      </v-container>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { Collections, pb, QueryEnumKeys } from "@/composables/pocketbase";
import {
  SubmissionsSessionOptions,
  type AuthorsResponse,
  type SubmissionsResponse,
  type TopicsResponse,
} from "@/composables/pocketbase/types";
import apiClient from "@/plugins/api-client";
import { useMutation, useQuery } from "@tanstack/vue-query";

interface CustomDataTableHeader {
  title: string;
  value: string;
  sortable: boolean;
  width: string;
  minWidth: string;
  authorsDisplayed?: string;
  authors?: string;
  link?: string;
}

const session = ref<SubmissionsSessionOptions>(
  SubmissionsSessionOptions["E5.2"],
);
const topic = ref<TopicsResponse<{ child?: TopicsResponse[] }>>();
const authors = ref<string[]>([]);
const sessions = [
  SubmissionsSessionOptions["E5.1"],
  SubmissionsSessionOptions["E5.2"],
];
const itemGroup = ref<string[]>([]);
const expandedCells = ref<Set<string>>(new Set());
const selectedCells = ref<Set<string>>(new Set());
const selectedSubmissions = ref<
  {
    submission: SubmissionsResponse<
      { [key: string]: string },
      {
        author?: AuthorsResponse[];
      }
    >;
    index: number;
  }[]
>([]);
const summary = ref();
const isFullscreen = ref(false);
const isAnalyze = ref(false);

const headers = computed<CustomDataTableHeader[]>(() => {
  const baseHeaders = [
    {
      title: "Key Element",
      value: "keyElement",
      sortable: false,
      width: "180px",
      minWidth: "180px",
    },
  ];

  const submissionHeaders = submissions.value.map((submission, index) => ({
    title: submission.title,
    authorsDisplayed:
      submission.author && submission.author.length > 1
        ? `${(submission.expand?.author?.[0] as any)?.name} +${submission.author.length - 1} other Delegations/Groups of States`
        : (submission.expand?.author?.[0] as any)?.name,
    authors:
      submission.expand?.author?.map((author) => author.name).join(", ") || "-",
    link: submission.href,
    value: `submission_${submission.id}`,
    sortable: false,
    width: "350px",
    minWidth: "350px",
  }));

  return [...baseHeaders, ...submissionHeaders];
});

const tableItems = computed(() => {
  if (submissions.value.length === 0) return [];
  const keyElements = new Set<string>();
  submissions.value.forEach((submission) => {
    if (submission.key_element) {
      Object.keys(submission.key_element).forEach((key) =>
        keyElements.add(key),
      );
    }
  });
  return Array.from(keyElements)
    .sort((a, b) => a.localeCompare(b))
    .map((keyElement) => ({
      id: keyElement,
      keyElement: keyElement,
    }));
});

const selectedCellsData = computed(() => {
  return Array.from(selectedCells.value).map((cellKey) => {
    const [submissionId, keyElement] = cellKey.split("|||");
    const submission = submissions.value.find((s) => s.id === submissionId);
    const submissionIndex = submissions.value.findIndex(
      (s) => s.id === submissionId,
    );
    return {
      submissionId,
      keyElement,
      submission,
      submissionIndex,
      content: replaceEmptyKeyElements(submission?.key_element?.[keyElement]),
    };
  });
});

const selectedKeyElement = computed(() => {
  if (selectedCells.value.size === 0) return null;
  return Array.from(selectedCells.value)[0].split("|||")[1];
});

const isCellSelectable = (submissionId: string, keyElement: string) => {
  const cellKey = `${submissionId}|||${keyElement}`;
  // If cell is already selected, it's always selectable (for deselection)
  if (selectedCells.value.has(cellKey)) {
    return true;
  }
  // If no cells are selected, all cells are selectable
  if (selectedCells.value.size === 0) {
    return true;
  }
  // If we've reached the limit of 3 selections, no new cells are selectable
  if (selectedCells.value.size >= 3) {
    return false;
  }
  // Only cells with the same key element as the first selection are selectable
  return keyElement === selectedKeyElement.value;
};

const isExpanded = (submissionId: string, keyElement: string) => {
  const cellKey = `${submissionId}|||${keyElement}`;
  return expandedCells.value.has(cellKey);
};

const toggleExpand = (submissionId: string, keyElement: string) => {
  const cellKey = `${submissionId}|||${keyElement}`;
  if (expandedCells.value.has(cellKey)) {
    expandedCells.value.delete(cellKey);
  } else {
    expandedCells.value.add(cellKey);
  }
};

const isSelectedCell = (submissionId: string, keyElement: string) => {
  const cellKey = `${submissionId}|||${keyElement}`;
  return selectedCells.value.has(cellKey);
};

const toggleCellSelection = (submissionId: string, keyElement: string) => {
  const cellKey = `${submissionId}|||${keyElement}`;
  if (selectedCells.value.has(cellKey)) {
    selectedCells.value.delete(cellKey);
  } else {
    if (selectedCells.value.size === 0) {
      selectedCells.value.add(cellKey);
    } else {
      const firstSelectedKeyElement = Array.from(selectedCells.value)[0].split(
        "|||",
      )[1];
      if (keyElement === firstSelectedKeyElement) {
        if (selectedCells.value.size >= 3) {
          return;
        }
        selectedCells.value.add(cellKey);
      }
    }
  }
};

const removeSelectedCell = (submissionId: string, keyElement: string) => {
  const cellKey = `${submissionId}|||${keyElement}`;
  selectedCells.value.delete(cellKey);
};

const clearSelectedCells = () => {
  selectedCells.value.clear();
};

const filterTopicArray = computed(() => {
  if (!topic.value) return;
  return [...new Set([topic.value.id, ...topic.value.child])];
});

const truncateText = (text: string) => {
  if (text.length <= 100) return text;
  const truncatedText = text.substring(0, 100);
  return truncatedText.substring(0, truncatedText.lastIndexOf(" ")) + "...";
};

const replaceEmptyKeyElements = (text: string | undefined) => {
  if (!text || text.length < 3)
    return "No relevant sections found in the submission for this key element.";
  return text;
};

const {
  mutate,
  isError: isMutateError,
  isPending: isMutatePending,
} = useMutation({
  mutationFn: async () => {
    let response =
      await apiClient.aiTools.summarizeKeyElementApiSummarizeKeyElementPost({
        key_element: selectedCellsData.value[0].keyElement,
        submission_extracts: selectedCellsData.value.map((el) => {
          return {
            author:
              el.submission?.expand.author?.map((author) => author.name) || [],
            text: el.content,
          };
        }),
      });
    summary.value = response;
  },
});

const { data: submissions, isFetching } = useQuery({
  queryKey: [QueryEnumKeys.Submissions, session, topic, authors],
  queryFn: async () => {
    if (!filterTopicArray.value) return [];

    let filterString = `(verified = ${true}) && (`;
    filterString += `session = '${session.value}'`;
    filterString += ") && (";
    filterTopicArray.value.forEach((el, index) => {
      if (index > 0) filterString += " || ";
      filterString += `topic ?~ '${el}'`;
    });
    filterString += ")";
    if (authors.value.length > 0) {
      filterString += " && (";
      authors.value.forEach((el, index) => {
        if (index > 0) filterString += " || ";
        filterString += `author ?~ '${el}'`;
      });
      filterString += ")";
    }

    return (await pb.collection(Collections.Submissions).getFullList({
      filter: pb.filter(`${filterString}`),
      expand: "author",
    })) as SubmissionsResponse<
      { [key: string]: string },
      {
        author?: AuthorsResponse[];
      }
    >[];
  },
  initialData: [],
});

const { data: topics } = useQuery({
  queryKey: [QueryEnumKeys.Topics],
  queryFn: async () => {
    return (await pb.collection(Collections.Topics).getFullList({
      filter: "child:length > 0 || topics_via_child.child:length = 0",
      expand: "child",
      sort: "article",
    })) as TopicsResponse<{
      child?: TopicsResponse[];
    }>[];
  },
  initialData: [],
});

const { data: authorsResponse } = useQuery({
  queryKey: [QueryEnumKeys.Authors],
  queryFn: async () => {
    return await pb.collection(Collections.Authors).getFullList({
      sort: "type,name",
    });
  },
  initialData: [],
});

watch(
  itemGroup,
  () => {
    selectedSubmissions.value = submissions.value
      .map((submission, index) => ({ submission, index }))
      .filter(({ submission }) => itemGroup.value.includes(submission.id));
  },
  { immediate: true },
);

watch(
  [session, topic, authors],
  () => {
    selectedCells.value = new Set();
  },
  { immediate: true },
);

watch(
  [selectedCells],
  () => {
    summary.value = undefined;
  },
  { immediate: true },
);

const showPdf = async (link: string | undefined) => {
  window.open(link, "_blank");
};
</script>

<style scoped>
.underlined-header {
  text-decoration: underline;
  text-decoration-color: #09677f;
  text-decoration-thickness: 4px;
  text-underline-offset: 8px;
}

.fontsize-h5-light {
  font-size: 18px !important;
  line-height: 28px !important;
  letter-spacing: 0.15px !important;
  font-weight: 300 !important;
}

@media (min-width: 600px) and (max-width: 959px) {
  .fontsize-h5-light {
    font-size: 20px !important;
    line-height: 32px !important;
    letter-spacing: 0.15px !important;
  }
}

@media (min-width: 960px) and (max-width: 1263px) {
  .fontsize-h5-light {
    font-size: 20px !important;
    line-height: 32px !important;
    letter-spacing: 0.15px !important;
  }
}

@media (min-width: 1264px) {
  .fontsize-h5-light {
    font-size: 24px !important;
    line-height: 32px !important;
    letter-spacing: 0px !important;
  }
}

.expanded-text {
  max-height: 400px;
  overflow-y: auto;
  padding-right: 12px;
}

.align-top {
  vertical-align: top;
  padding: 8px !important;
}

.custom-table :deep(.header-row) {
  background-color: #09677f33;
  font-weight: bold;
}

.custom-table {
  border: 1px solid rgba(0, 0, 0, 0.12);
  border-radius: 4px;
  overflow: hidden;
  overflow-x: auto;
}

.custom-table :deep(.v-table__wrapper) {
  overflow-x: scroll;
  scrollbar-width: auto;
}

.custom-table :deep(.v-table__wrapper)::-webkit-scrollbar {
  height: 12px;
  background-color: #f5f5f5;
  border-radius: 6px;
}

.custom-table :deep(.v-table__wrapper)::-webkit-scrollbar-thumb {
  background-color: #c1c1c1;
  border-radius: 6px;
}

.custom-table :deep(.v-table__wrapper)::-webkit-scrollbar-thumb:hover {
  background-color: #a8a8a8;
}

.custom-table :deep(.key-element-cell) {
  background-color: #ffffff;
  font-weight: bold;
  position: sticky;
  left: 0;
  z-index: 10;
}

.custom-table :deep(.header-row th:first-child) {
  position: sticky;
  left: 0;
  z-index: 20;
}

.submission-cell {
  cursor: pointer;
  transition: background-color 0.2s ease;
  background-color: white;
}

.submission-cell:hover {
  background-color: #f0f8ff !important;
}

.selected-cell {
  background-color: #ffffff !important;
  border: 2px solid #09677f !important;
}

.disabled-cell {
  opacity: 0.4;
  cursor: not-allowed !important;
  background-color: #f5f5f5 !important;
}

.disabled-cell:hover {
  background-color: #f5f5f5 !important;
}

.fullscreen-table {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9999;
  background-color: white;
  padding: 24px;
  overflow: auto;
}

.fullscreen-table .v-data-table {
  height: calc(100vh - 235px);
}
</style>
