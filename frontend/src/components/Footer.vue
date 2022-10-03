<script setup lang="ts">
import { computed } from "vue";
import { useBrewStore } from "../stores/brew";
const brewState = useBrewStore();

const temperature = computed(() => {
  if (!brewState.state.temperature) {
    return "N/A";
  }
  return `${brewState.state.temperature} ℃`;
});
</script>

<template>
  <v-footer>
    <v-alert v-if="brewState.error" density="compact" type="error">
      Connection to server lost.
    </v-alert>
    <v-row justify="center">
      <v-col>
        <strong>Temperature:</strong>
      </v-col>
      <v-col>
        <strong>{{ temperature }}</strong>
      </v-col>
      <v-col> <strong>Pump:</strong> </v-col>>
      <v-col>
        <v-icon
          v-if="brewState.state.pumpState"
          icon="mdi-water-pump"
          color="green"
        />
        <v-icon v-else icon="mdi-water-pump-off" color="red" />
      </v-col>
    </v-row>
  </v-footer>
</template>
