<template>
  <v-autocomplete
    v-model="selectedAuthors"
    :items="authors"
    :error-messages="
      isUserQueryError ? ['Error fetching Delegations/Groups of States'] : []
    "
    :rules="[
      (v) => v.length > 0 || 'Please select a Delegation/Group of States',
    ]"
    :loading="isUserQueryFetching"
    item-value="id"
    item-title="name"
    label="Delegations/Groups of States"
    variant="solo-filled"
    flat
    multiple
  >
    <template #item="{ props, item }">
      <v-list-item v-bind="props" :title="item.raw.name">
        <template #prepend>
          <v-icon
            class="mr-4"
            :icon="selectedIcon(selectedAuthors.includes(item.raw.id))"
          ></v-icon>
        </template>
      </v-list-item>
    </template>
    <template v-slot:selection="{ item, index }">
      <v-chip v-if="index < 2" size="small" rounded="lg" color="primary">
        <span>{{ item.raw.name }}</span>
      </v-chip>
      <span
        v-if="!!authors && index === 2"
        class="text-grey text-caption align-self-center"
      >
        (+{{ selectedAuthors.length - 2 }} others)
      </span>
    </template>
  </v-autocomplete>
</template>

<script setup lang="ts">
import { Collections, pb, QueryEnumKeys } from "@/composables/pocketbase";
import { useQuery } from "@tanstack/vue-query";
import type { RecordIdString } from "@/composables/pocketbase/types";

const selectedAuthors = defineModel<RecordIdString[]>({ default: () => [] });

const {
  data: authors,
  isFetching: isUserQueryFetching,
  isError: isUserQueryError,
} = useQuery({
  queryKey: [QueryEnumKeys.Authors],
  queryFn: async () => {
    return await pb.collection(Collections.Authors).getFullList({
      sort: "type,name",
    });
  },
});

const selectedIcon = (isAuthorSelected: boolean) => {
  return isAuthorSelected
    ? "mdi-checkbox-marked"
    : "mdi-checkbox-blank-outline";
};
</script>
