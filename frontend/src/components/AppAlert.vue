<template>
  <v-expand-transition>
    <div>
      <v-alert
        v-if="isAlert"
        :closable="closable"
        :color="color"
        rounded
        :type="type"
      >
        <slot name="default" />
      </v-alert>
    </div>
  </v-expand-transition>
</template>

<script setup lang="ts">
  withDefaults(
    defineProps<{
      isAlert: boolean | string | undefined
      type?: 'error' | 'success' | 'info' | 'warning'
      color?: string
      closable?: boolean
    }>(),
    {
      type: 'error',
      color: 'error',
      closable: true,
    },
  )
</script>
