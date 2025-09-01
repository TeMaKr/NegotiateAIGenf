<template>
  <document-dialog
    :title="'Edit document'"
    :mutateErrorMessage="'The document could not be updated. Please try again later.'"
    :mutationFn="updateDocument"
    :resetFormOnSuccess="false"
    :successFn="successFn"
    :document="documentToBeUpdated"
    :hasFile="!!props.document.file"
  >
    <template v-slot:activator="{ props }">
      <slot :props="props" name="activator"></slot>
    </template>
  </document-dialog>
</template>

<script setup lang="ts">
import DocumentDialog from "@/components/DocumentDialog.vue";
import { Collections, pb, QueryEnumKeys } from "@/composables/pocketbase";
import type {
  SubmissionsRecord,
  SubmissionsResponse,
} from "@/composables/pocketbase/types";
import { useSnackbarQueueStore } from "@/stores/snackbar-queue";
import { useQueryClient } from "@tanstack/vue-query";
import { reactive, watch } from "vue";
const props = defineProps<{
  document: SubmissionsResponse;
}>();

const store = useSnackbarQueueStore();
const queryClient = useQueryClient();

const documentToBeUpdated = reactive<SubmissionsRecord>({
  title: props.document.title,
  description: props.document.description,
  author: props.document.author,
  session: props.document.session,
  verified: props.document.verified,
  topic: props.document.topic,
  id: props.document.id,
  href: props.document.href,
  document_type: props.document.document_type,
});

const updateDocument = async () => {
  return await pb
    .collection(Collections.Submissions)
    .update(props.document.id, documentToBeUpdated);
};

const successFn = async (data: SubmissionsResponse) => {
  queryClient.invalidateQueries({
    queryKey: [QueryEnumKeys.Submissions, props.document.id],
  });

  store.appendSuccess(`Document "${data.title}" updated successfully`);
};

watch(
  () => props.document,
  (newDocument: SubmissionsResponse) => {
    documentToBeUpdated.title = newDocument.title;
    documentToBeUpdated.description = newDocument.description;
    documentToBeUpdated.author = newDocument.author;
    documentToBeUpdated.session = newDocument.session;
    documentToBeUpdated.topic = newDocument.topic;
    documentToBeUpdated.verified = newDocument.verified;
    documentToBeUpdated.id = newDocument.id;
    documentToBeUpdated.href = newDocument.href;
    documentToBeUpdated.document_type = newDocument.document_type;
  },
);
</script>
