<template>
  <v-card
    :border="true"
    variant="flat"
    color="surface"
    class="my-2 pa-2"
    :to="{
      name: 'DocumentDetail',
      params: { id: props.submission.id },
      query: { ...route.query },
    }"
  >
    <template v-slot:title>
      <span class="fontsize-h6 font-weight-bold">
        {{ submission.title }}
      </span>
    </template>

    <template v-slot:text>
      <div class="d-flex align-center justify-space-between">
        <div class="w-100">
          <div class="mb-2">
            <v-chip
              :color="!!submission?.expand?.author ? 'primary' : 'error'"
              class="mb-2 mr-1"
              rounded="lg"
            >
              {{ authorTag }}
            </v-chip>
            <v-chip color="primary" class="mb-2 mr-1" rounded="lg">
              Session: {{ submission.session }}
            </v-chip>
            <v-chip
              v-if="!!topics && topics?.length > 0"
              color="primary"
              class="mb-2 mr-1"
              rounded="lg"
            >
              Topics: {{ topics }}
            </v-chip>
            <v-chip
              v-if="isAuthenticated"
              :color="submission.verified ? 'success' : 'warning'"
              class="mb-2 mr-1"
              rounded="lg"
            >
              Verified: {{ submission.verified }}
            </v-chip>
          </div>
        </div>
      </div>
      <div class="mb-1 d-flex justify-space-between align-center">
        <p>{{ submission.description }}</p>
      </div>
    </template>
  </v-card>
</template>

<script setup lang="ts">
import { usePocketBase } from "@/composables/pocketbase";
import {
  type AuthorsResponse,
  type SubmissionsResponse,
  type TopicsResponse,
} from "@/composables/pocketbase/types";
import { useRoute } from "vue-router";

const route = useRoute();
const { isAuthenticated } = await usePocketBase();

const props = defineProps<{
  submission: SubmissionsResponse & {
    expand?: {
      author?: AuthorsResponse[];
      topic?: TopicsResponse[];
    };
  };
}>();

const authorTag = computed(() => {
  return props.submission.expand?.author
    ? `Delegations/Groups of States : ${props.submission.expand.author.map((a) => a.name).join(", ")}`
    : "Delegations/Groups of States Not provided";
});

const topics = computed(() => {
  return props.submission.expand?.topic?.reduce((acc, topic) => {
    return acc ? `${acc}, ${topic.name}` : topic.name;
  }, "");
});
</script>
