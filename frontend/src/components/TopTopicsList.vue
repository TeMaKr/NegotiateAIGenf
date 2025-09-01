<template>
  <v-card :border="true" variant="flat" color="surface" class="my-2 pa-2">
    <template #title
      ><div class="d-flex align-center">
        Top Topics
        <v-chip color="primary" size="small" class="ml-2" rounded="lg">
          By Number of Submissions
        </v-chip>
      </div>
    </template>

    <v-list class="pa-0">
      <v-list-item
        v-for="(topic, index) in aggregatedTopicsData.slice(0, 10)"
        :key="topic.id"
        class="align-start"
      >
        <template #prepend>
          <v-avatar size="small" color="secondary">
            {{ index + 1 }}
          </v-avatar>
        </template>

        <v-list-item-title>
          {{ topic.name }}
        </v-list-item-title>

        <v-list-item-subtitle>
          <div class="d-flex align-center">
            Number of Submissions: {{ topic.submissionsCount.toLocaleString() }}
            <v-tooltip location="bottom">
              <template #activator="{ props }">
                <v-btn
                  v-bind="props"
                  icon="mdi-information-outline"
                  size="x-small"
                  variant="text"
                  class="ml-1"
                />
              </template>
              <div class="pa-2">
                <div class="font-weight-bold mb-1">Topic: {{ topic.name }}</div>
                <div>Total Submissions: {{ topic.submissionsCount }}</div>
                <div>Direct Submissions: {{ topic.directSubmissions }}</div>
                <div v-if="topic.childTopics.length > 0" class="mt-2">
                  <div class="font-weight-medium">Subtopics:</div>
                  <div
                    v-for="child in topic.childTopics"
                    :key="child.id"
                    class="text-caption"
                  >
                    • {{ child.name }}: {{ child.submissionsCount }}
                  </div>
                </div>
              </div>
            </v-tooltip>
          </div>
        </v-list-item-subtitle>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useQuery } from "@tanstack/vue-query";
import { Collections, pb, QueryEnumKeys } from "@/composables/pocketbase";
import type {
  SubmissionsResponse,
  TopicsResponse,
} from "@/composables/pocketbase/types";

const { data: topics } = useQuery({
  queryKey: [QueryEnumKeys.Topics, "submissionsPerTopic"],
  queryFn: async () => {
    return await pb.collection(Collections.Topics).getFullList<
      TopicsResponse & {
        expand: {
          submissions_via_topic: SubmissionsResponse[];
          child: TopicsResponse[];
        };
      }
    >({ expand: "submissions_via_topic,child", sort: "-name" });
  },
});

const aggregatedTopicsData = computed(() => {
  if (!topics.value) return [];

  const childTopicIds = new Set<string>(
    topics.value
      .filter((topic) => topic.expand?.child)
      .flatMap((topic) => topic.expand.child.map((child) => child.id)),
  );

  const topicSubmissionMap = new Map<string, number>();

  topics.value.forEach((topic) => {
    const directSubmissions = topic.expand?.submissions_via_topic?.length || 0;
    topicSubmissionMap.set(topic.id, directSubmissions);
  });

  topics.value.forEach((topic) => {
    if (topic.expand?.child) {
      topic.expand.child.forEach((childTopic) => {
        const childSubmissions =
          topics.value?.find((t) => t.id === childTopic.id)?.expand
            ?.submissions_via_topic?.length || 0;

        const currentParentCount = topicSubmissionMap.get(topic.id) || 0;
        topicSubmissionMap.set(topic.id, currentParentCount + childSubmissions);
      });
    }
  });

  return topics.value
    .filter((topic) => !childTopicIds.has(topic.id))
    .map((topic) => ({
      id: topic.id,
      name: topic.name,
      submissionsCount: topicSubmissionMap.get(topic.id) || 0,
      directSubmissions: topic.expand?.submissions_via_topic?.length || 0,
      childTopics:
        topic.expand?.child?.map((childTopic) => {
          const childSubmissionCount =
            topics.value?.find((t) => t.id === childTopic.id)?.expand
              ?.submissions_via_topic?.length || 0;
          return {
            id: childTopic.id,
            name: childTopic.name,
            submissionsCount: childSubmissionCount,
          };
        }) || [],
    }))
    .sort((a, b) => {
      // Sort by total submissions count in descending order
      return b.submissionsCount - a.submissionsCount;
    });
});
</script>
