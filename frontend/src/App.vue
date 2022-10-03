<script setup lang="ts">
import { RouterView } from "vue-router";
import { useBrewStore } from "./stores/brew";

const brewState = useBrewStore();

const ws = new WebSocket("ws:app/state");
ws.onmessage = (event) => {
  brewState.state = JSON.parse(event.data);
  brewState.error = false;
};
ws.onerror = () => {
  brewState.error = true;
};

setInterval(() => {
  ws.send("");
}, 1000);

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
        <!-- Bottom nav for is state v-footer -->
      </v-container>
    </v-main>
  </v-app>
</template>
