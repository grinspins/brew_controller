<script setup lang="ts">
import { RouterView } from "vue-router";
import Footer from "./components/Footer.vue";
import WebSocketProvider from "./components/Websocket.vue";

const links = [
  {
    title: "Control",
    value: "control",
    to: "/",
    icon: "mdi-controller",
  },
  {
    title: "Program",
    value: "program",
    to: "/program",
    icon: "mdi-list-box",
  },
];
</script>

<template>
  <v-app>
    <WebSocketProvider />
    <v-app-bar color="amber" density="compact">
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
    <v-main class="h-screen">
      <v-container class="pb-12" fluid>
        <RouterView />
      </v-container>
    </v-main>
    <Footer app />
  </v-app>
</template>
