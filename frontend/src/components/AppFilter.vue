<template>
  <div class="d-flex justify-center flex-column flex-lg-row ga-4">
    <v-row class="flex-grow-1">
      <v-col cols="12" :md="isFilterVerified ? 3 : 4">
        <v-autocomplete
          v-model="authors"
          :items="authorsResponse"
          item-title="name"
          item-value="id"
          label="Delegations/Groups of States"
          variant="outlined"
          prepend-inner-icon="mdi-account-group-outline"
          menu-icon="mdi-chevron-down"
          bg-color="white"
          color="primary"
          density="compact"
          :hint="
            isAuthorsRequired && !authors?.length
              ? 'You need to select Delegations/Groups of States to submit a question.'
              : ''
          "
          :persistent-hint="isAuthorsRequired && !authors?.length"
          clearable
          chips
          multiple
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
      <v-col cols="12" :md="isFilterVerified ? 3 : 4">
        <v-autocomplete
          v-model="sessions"
          :items="sessionValues"
          label="Sessions"
          variant="outlined"
          prepend-inner-icon="mdi-format-list-numbered"
          menu-icon="mdi-chevron-down"
          bg-color="white"
          color="primary"
          clearable
          chips
          multiple
          density="compact"
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
      <v-col cols="12" :md="isFilterVerified ? 3 : 4">
        <v-autocomplete
          v-model="selectedTopics"
          :items="topicsResponse"
          return-object
          label="Topics"
          item-title="name"
          variant="outlined"
          prepend-inner-icon="mdi-message-text-outline"
          menu-icon="mdi-chevron-down"
          bg-color="white"
          color="primary"
          clearable
          chips
          multiple
          density="compact"
          persistent-hint
        >
          <template #chip="{ item }">
            <v-chip rounded="lg">
              <p class="text-grey-darken-2">
                <strong>{{ item.title }}</strong>
              </p>
            </v-chip>
          </template>
          <template #item="{ props, item }">
            <v-list-item
              v-tooltip="getTopicTooltip(item.raw)"
              v-bind="props"
              :title="item.raw.name"
            />
          </template>
          <template v-slot:details>
            <span class="v-messages__message font-italic">
              See the
              <a href="/treaty-explorer" target="_blank" class="text-primary"
                >draft treaty explorer</a
              >
              for more details on the topics' structure.</span
            >
          </template>
        </v-autocomplete>
      </v-col>
      <v-col v-if="isFilterVerified" cols="12" md="3">
        <v-autocomplete
          v-model="verified"
          :items="verifiedOptions"
          item-title="text"
          item-value="value"
          label="Verified"
          variant="outlined"
          density="compact"
          clearable
          chips
          bg-color="white"
          color="primary"
          prepend-inner-icon="mdi-shield-check-outline"
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
    </v-row>
  </div>
</template>

<script setup lang="ts">
import { pb, QueryEnumKeys } from "@/composables/pocketbase";
import {
  Collections,
  SubmissionsSessionOptions,
  type TopicsResponse,
} from "@/composables/pocketbase/types";
import { useQuery } from "@tanstack/vue-query";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

interface Topics extends TopicsResponse {
  expand?: {
    child: TopicsResponse[];
  };
}

const props = withDefaults(
  defineProps<{
    isFilterVerified?: boolean;
    isAuthorsRequired?: boolean;
  }>(),
  {
    isFilterVerified: true,
    isAuthorsRequired: false,
  },
);

const selectedTopics = ref<Topics[]>([]);
const authors = defineModel<string[]>("authors");
const sessions = defineModel<SubmissionsSessionOptions[]>("sessions");
const topics = defineModel<string[]>("topics");
const verified = defineModel<boolean | null>("verified");

watch(
  selectedTopics,
  (newTopics) => {
    topics.value = [
      ...new Set(newTopics.flatMap((topic) => [topic.id, ...topic.child])),
    ];
    router.push({
      query: {
        ...route.query,
        topics: JSON.stringify([
          ...new Set(newTopics.flatMap((topic) => [topic.id, ...topic.child])),
        ]),
      },
    });
  },
  { immediate: true },
);
watch(topics, (newTopics) => {
  if (
    (!newTopics || newTopics.length === 0) &&
    selectedTopics.value.length > 0
  ) {
    selectedTopics.value = [];
  }
});
watch(authors, (newAuthors) => {
  router.push({
    query: {
      ...route.query,
      authors: JSON.stringify(newAuthors),
    },
  });
});
watch(sessions, (newSessions) => {
  router.push({
    query: {
      ...route.query,
      sessions: JSON.stringify(newSessions),
    },
  });
});

const sessionValues = computed(() => {
  return Object.values(SubmissionsSessionOptions);
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

const { data: topicsResponse } = useQuery({
  queryKey: [QueryEnumKeys.Topics, "app-filter"],
  queryFn: async () => {
    return await pb.collection(Collections.Topics).getFullList<Topics>({
      filter: "child:length > 0 || topics_via_child.child:length = 0",
      expand: "child",
      sort: "article",
    });
  },
  initialData: [],
});

const verifiedOptions = [
  { text: "true", value: true },
  { text: "false", value: false },
];

const getTopicTooltip = (topic: Topics) => {
  const subtopics = topic.expand?.child || [];

  if (subtopics.length === 0) {
    return `No subtopics available`;
  }

  const sampleSize = 2;
  const sortedSubtopics = subtopics.sort((a, b) =>
    a.name.localeCompare(b.name),
  );
  const firstTwoSubtopics = sortedSubtopics
    .slice(0, sampleSize)
    .map((st) => st.name);
  const tooltipText = `For example: ${firstTwoSubtopics.join(", ")}`;

  if (subtopics.length > sampleSize) {
    return `${tooltipText} (+${subtopics.length - sampleSize} more)`;
  }

  return tooltipText;
};

onMounted(() => {
  authors.value = route.query.authors
    ? JSON.parse(route.query.authors as string)
    : [];
  sessions.value = route.query.sessions
    ? JSON.parse(route.query.sessions as SubmissionsSessionOptions)
    : [];
  if (route.query.topics) {
    topics.value = JSON.parse(route.query.topics as string);
    setTimeout(() => {
      selectedTopics.value = topicsResponse.value.filter((t) =>
        JSON.parse(route.query.topics as string).includes(t.id),
      );
    }, 100);
  }
});
</script>
