<script setup lang="ts">
import { RouterView } from "vue-router";
import { useBrewStore } from "./stores/brew";
import { STATE_URL } from "./urls";
import Footer from "./components/Footer.vue";

const brewState = useBrewStore();

let intervalId: number | undefined = undefined;

const stateTick = (ws: WebSocket) => {
  intervalId = setInterval(() => {
    if (ws.readyState !== WebSocket.OPEN) {
      clearInterval(intervalId);
      brewState.error = true;
      connectWebsocket();
    }
    ws.send("{}");
  }, 1000);
};

const connectWebsocket = () => {
  const ws = new WebSocket(STATE_URL);
  ws.onmessage = (event) => {
    brewState.state = JSON.parse(event.data);
    brewState.error = false;
  };
  ws.onerror = () => {
    brewState.error = true;
  };
  ws.onopen = () => {
    stateTick(ws);
  };
};

connectWebsocket();

const links = [
  {
    title: "Home",
    value: "home",
    to: "/",
    icon: "mdi-home",
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
    <v-main class="h-screen">
      <v-container class="pb-12" fluid>
        <RouterView />
      </v-container>
    </v-main>
    <Footer app />
  </v-app>
</template>
