<script setup lang="ts">
import { computed } from "vue";
import { useStateStore } from "@/stores/state";
import { useProgramStore } from "@/stores/program";

const state = useStateStore();
const program = useProgramStore();

const temperature = computed(() => {
  if (state.temperature === null) {
    return "N/A";
  }
  return `${state.temperature.toFixed(2)} ℃`;
});

const remaining = computed(() => {
  if (!state.remainingTime) {
    return "N/A";
  }
  return `${state.remainingTime.toFixed(2)} min`;
});

const step = computed(() => {
  const idx = state.step;
  if (typeof idx === "number") {
    const name = program.program[idx]?.name;
    if (state.heating) {
      return `Heating to ${name}`;
    }
    return name;
  }
  return "N/A";
});
</script>

<template>
  <v-footer class="bg-grey-lighten-1">
    <div v-if="state.error">
      <v-alert density="compact" type="error"
        >Connection to server lost.</v-alert
      >
    </div>
    <v-row v-else justify="center">
      <v-col> <strong>Temperature:</strong> {{ temperature }} </v-col>
      <v-col
        ><strong>Pump:</strong>
        &nbsp;
        <v-icon v-if="state.pumpState" icon="mdi-water-pump" color="green" />
        <v-icon v-else icon="mdi-water-pump-off" color="red" />
      </v-col>
      <v-col> <strong>Step:</strong> {{ step }} </v-col>
      <v-col> <strong>Remaining:</strong> {{ remaining }} </v-col>
    </v-row>
  </v-footer>
</template>
