<template>
  <v-autocomplete
    v-model="selectedSession"
    :items="sessions"
    :rules="[(v) => v.length > 0 || 'Please select a session']"
    item-value="value"
    item-title="title"
    label="Session"
    variant="solo-filled"
    flat
  >
    <template #item="{ props, item }">
      <v-list-item v-bind="props" :title="item.title"> </v-list-item>
    </template>
    <template v-slot:selection="{ item, index }">
      <v-chip v-if="index < 2" size="small" rounded="lg" color="primary">
        <span>{{ item.title }}</span>
      </v-chip>
    </template>
  </v-autocomplete>
</template>

<script setup lang="ts">
import { SubmissionsSessionOptions } from "@/composables/pocketbase/types";

const selectedSession = defineModel<SubmissionsSessionOptions>();
const sessions = Object.values(SubmissionsSessionOptions);
</script>
