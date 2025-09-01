<template>
  <v-container>
    <app-alert :is-alert="isError"> Accounts could not be loaded.</app-alert>
    <app-snackbar v-model="createSuccessful">
      Account successfully created.
    </app-snackbar>
    <app-snackbar v-model="updateSuccessful">
      Account successfully updated.
    </app-snackbar>
    <h1 class="mb-8">All accounts</h1>
    <v-row>
      <v-col cols="12">
        <v-text-field
          v-model="search"
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          density="compact"
          placeholder="Search accounts"
          hide-details
          clearable
        >
        </v-text-field>
      </v-col>
      <v-col cols="12" class="d-flex justify-end mb-1">
        <user-create @created="createSuccessful = true" />
      </v-col>
    </v-row>
    <div v-if="isFetching">
      <v-skeleton-loader color="transparent" type="heading" class="my-2" />
    </div>
    <v-data-table
      v-else
      :search="search"
      :items="users"
      :headers="headers"
      items-per-page="10"
      no-data-text="No accounts found"
      items-per-page-text="Users per page"
      style="border-radius: 4px"
    >
      <template v-slot:item.name="{ item }">
        {{ item.first_name }} {{ item.last_name }}
      </template>
      <template v-slot:item.actions="{ item }">
        <UserUpdate :user="item" @updated="updateSuccessful = true" />
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import type { VDataTable } from "vuetify/components";
type ReadonlyHeaders = VDataTable["$props"]["headers"];
import { useQuery } from "@tanstack/vue-query";
import { pb, QueryEnumKeys } from "@/composables/pocketbase";
import { Collections } from "@/composables/pocketbase/types";

const search = ref<string>("");
const createSuccessful = ref<boolean>(false);
const updateSuccessful = ref<boolean>(false);
const headers = computed<ReadonlyHeaders>(() => {
  return [
    {
      title: "E-Mail",
      key: "email",
      align: "start",
    },
    {
      title: "Name",
      key: "name",
    },
    {
      title: "",
      key: "actions",
      align: "end",
    },
  ];
});

const {
  isFetching,
  data: users,
  isError,
} = useQuery({
  queryKey: [QueryEnumKeys.Users],
  queryFn: async () => {
    return await pb
      .collection(Collections.Users)
      .getFullList({ sort: "-created" });
  },
  initialData: [],
});
</script>
