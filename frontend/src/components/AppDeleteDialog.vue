<template>
  <v-dialog v-model="isDialog" max-width="500" persistent>
    <template v-slot:activator="{ props: activatorProps }">
      <v-btn
        v-if="isButton"
        v-bind="activatorProps"
        variant="tonal"
        :size="props.buttonSize"
        color="error"
        :disabled="props.isDisabled"
      >
        {{ props.buttonText }}
      </v-btn>
      <v-btn
        v-else-if="isIcon"
        v-bind="activatorProps"
        :size="props.buttonSize"
        :variant="props.isVariantText ? 'text' : 'tonal'"
        :icon="props.isVariantText ? true : false"
        color="error"
        :disabled="props.isDisabled"
      >
        <v-icon>{{ 'mdi-delete-outline' }}</v-icon>
      </v-btn>
      <v-list-item v-else v-bind="activatorProps" :disabled="props.isDisabled">
        <v-list-item-title class="text-error">
          {{ props.title }} {{ props.buttonText }}
        </v-list-item-title>
      </v-list-item>
    </template>
    <template v-slot:default>
      <v-card>
        <app-alert :is-alert="isError">
          {{ props.title }} konnte nicht gelöscht werden.
        </app-alert>
        <v-card-title>
          <slot name="title"></slot>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <slot name="default"></slot>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="medium-emphasis"
            variant="tonal"
            @click="isDialog = false"
          >
            Abbrechen
          </v-btn>
          <v-btn
            variant="flat"
            color="error"
            :loading="isPending"
            @click="mutate()"
          >
            {{ props.buttonText }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>

<script setup lang="ts">
import { useMutation } from '@tanstack/vue-query'
import { ref } from 'vue'

const props = withDefaults(
  defineProps<{
    buttonText: string
    isButton?: boolean
    isIcon?: boolean
    isVariantText?: boolean
    buttonSize?: string
    title: string
    mutationFn: Function
    onSuccess: Function
    isDisabled?: boolean
  }>(),
  {
    isVariantText: false,
    buttonSize: 'default',
  },
)

const isDialog = ref<boolean>(false)

const { isPending, isError, mutate } = useMutation({
  mutationFn: async () => await props.mutationFn(),
  onSuccess: async () => {
    await props.onSuccess()
    isDialog.value = false
  },
})
</script>
