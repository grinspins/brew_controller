<script setup lang="ts">
import { RouterView } from "vue-router";

const links = [
  {
    title: "Home",
    value: "home",
    to: "/",
    icon: "mdi-home",
  },
  {
    title: "About",
    value: "about",
    to: "/about",
    icon: "mdi-information",
  },
];
</script>

<template>
  <v-app>
    <v-app-bar color="primary" density="compact">
      <template v-slot:prepend>
        <v-icon icon="mdi-glass-mug-variant"></v-icon>
      </template>
      <v-app-bar-title>Beer</v-app-bar-title>
    </v-app-bar>
    <v-navigation-drawer expand-on-hover rail>
      <v-list density="compact" nav>
        <v-list-item
          v-for="(link, idx) in links"
          :to="link.to"
          :title="link.title"
          :value="link.value"
          :prepend-icon="link.icon"
          :key="idx"
        >
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-main>
      <v-container fluid>
        <RouterView />
      </v-container>
    </v-main>
  </v-app>
</template>
