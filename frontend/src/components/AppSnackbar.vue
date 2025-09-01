<template>
  <v-snackbar v-model="model" :color="color" :timeout="timeout">
    <slot name="default"></slot>
  </v-snackbar>
</template>

<script setup lang="ts">
const model = defineModel<boolean>()

const props = withDefaults(
  defineProps<{
    color?: string
    timeout?: string
  }>(),
  {
    color: 'success',
    timeout: '3000',
  },
)
</script>
