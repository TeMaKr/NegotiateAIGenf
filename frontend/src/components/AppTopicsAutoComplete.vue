<template>
  <v-autocomplete
    v-model="selectedTopics"
    :items="topics"
    :error-messages="isUserQueryError ? ['Error fetching topics'] : []"
    :rules="[(v) => v.length > 0 || 'Please select a topic']"
    :loading="isUserQueryFetching"
    item-value="id"
    item-title="name"
    label="Topics"
    variant="solo-filled"
    flat
    multiple
  >
    <template #append-inner>
      <v-icon
        v-tooltip="
          'Selecting a subtopic will automatically consider the parent topic for filtering.'
        "
        size="16"
        color="primary"
      >
        mdi-information-outline
      </v-icon>
    </template>
    <template v-slot:selection="{ item, index }">
      <v-chip v-if="index < 2" size="small" rounded="lg" color="primary">
        <span>{{ item.raw.name }}</span>
      </v-chip>
      <span
        v-if="!!topics && index === 2"
        class="text-grey text-caption align-self-center"
      >
        (+{{ selectedTopics.length - 2 }} others)
      </span>
    </template>
  </v-autocomplete>
</template>

<script setup lang="ts">
import { Collections, pb, QueryEnumKeys } from "@/composables/pocketbase";
import { useQuery } from "@tanstack/vue-query";
import type { RecordIdString } from "@/composables/pocketbase/types";

const selectedTopics = defineModel<RecordIdString[]>({ default: () => [] });

const {
  data: topics,
  isFetching: isUserQueryFetching,
  isError: isUserQueryError,
} = useQuery({
  queryKey: [QueryEnumKeys.Topics],
  queryFn: async () => {
    return await pb.collection(Collections.Topics).getFullList({
      sort: "article",
    });
  },
});
</script>
