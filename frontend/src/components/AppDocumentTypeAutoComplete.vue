<template>
  <v-autocomplete
    v-model="selectedDocumentType"
    :items="documentType"
    :rules="[(v) => v.length > 0 || 'Please select a document type']"
    item-value="value"
    item-title="title"
    label="Document Type"
    variant="solo-filled"
    flat
  >
    <template #item="{ props, item }">
      <v-list-item v-bind="props" :title="item.title"> </v-list-item>
    </template>
    <template v-slot:selection="{ item }">
      <v-chip size="small" rounded="lg" color="primary">
        <span>{{ item.title }}</span>
      </v-chip>
    </template>
  </v-autocomplete>
</template>

<script setup lang="ts">
import { SubmissionsDocumentTypeOptions } from "@/composables/pocketbase/types";

const selectedDocumentType = defineModel<SubmissionsDocumentTypeOptions>();
const documentType = Object.values(SubmissionsDocumentTypeOptions);
</script>
