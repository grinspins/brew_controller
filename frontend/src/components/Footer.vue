<script setup lang="ts">
import { computed } from "vue";
import { useBrewStore } from "@/stores/brew";
import { useProgramStore } from "@/stores/program";

const brewState = useBrewStore();
const program = useProgramStore();

const temperature = computed(() => {
  if (!brewState.state.temperature) {
    return "N/A";
  }
  return `${brewState.state.temperature.toFixed(2)} ℃`;
});

const remaining = computed(() => {
  if (!brewState.state.remainingTime) {
    return "N/A";
  }
  return `${brewState.state.remainingTime.toFixed(2)} min`;
});

const step = computed(() => {
  const idx = brewState.state.step;
  if (typeof idx === "number") {
    return program.step(idx)?.name;
  }
  return "N/A";
});
</script>

<template>
  <v-footer class="bg-grey-lighten-1">
    <!-- TODO alert larger than footer -->
    <div v-if="brewState.error">
      <v-alert density="compact" type="error"
        >Connection to server lost.</v-alert
      >
    </div>
    <v-row v-else justify="center">
      <v-col> <strong>Temperature:</strong> {{ temperature }} </v-col>
      <v-col
        ><strong>Pump:</strong>
        &nbsp;
        <v-icon
          v-if="brewState.state.pumpState"
          icon="mdi-water-pump"
          color="green"
        />
        <v-icon v-else icon="mdi-water-pump-off" color="red" />
      </v-col>
      <v-col> <strong>Step:</strong> {{ step }} </v-col>
      <v-col> <strong>Remaining:</strong> {{ remaining }} </v-col>
    </v-row>
  </v-footer>
</template>
