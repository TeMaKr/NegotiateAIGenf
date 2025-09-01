<template>
  <v-app>
    <suspense>
      <app-bar />
    </suspense>
    <v-main>
      <suspense>
        <router-view />
      </suspense>
    </v-main>
    <app-footer />
  </v-app>
</template>
