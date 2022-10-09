<script setup lang="ts">
import axios from "axios";
import { useProgramStore } from "@/stores/program";
import { PROGRAM_URL } from "@/urls";
import ProgramFormStep from "./ProgramFormStep.vue";

interface StepResponse {
  name: string;
  temperature: number;
  time: number;
  pump_state: boolean;
  fixed: boolean;
  wait: boolean;
}

const programStore = useProgramStore();

axios
  .get<StepResponse[]>(PROGRAM_URL)
  .then((response) => {
    const program = response.data.map((step) => ({
      name: step.name,
      temperature: step.temperature,
      time: step.time,
      pumpState: step.pump_state,
      fixed: step.fixed,
      wait: step.wait,
    }));
    programStore.program = program;
    programStore.error = false;
    programStore.loaded = true;
  })
  .catch((error) => {
    programStore.error = true;
    programStore.loaded = true;
  });

const removeStep = (idx: number) => {
  // TODO can't get $patch to work for this
  programStore.program = programStore.program.filter((_, i) => i !== idx);
};
</script>
<template>
  <v-card title="Program" subtitle="Create a program to run">
    <v-card-item v-if="!programStore.loaded">
      <div class="text-center">
        <v-progress-circular
          indeterminate
          color="primary"
        ></v-progress-circular>
      </div>
    </v-card-item>
    <v-card-item v-else-if="programStore.error">
      <v-alert density="compact" type="error">Unable to load program.</v-alert>
    </v-card-item>
    <div v-else>
      <v-form>
        <ProgramFormStep
          v-for="(step, idx) in programStore.program"
          :key="step.name"
          @change="(value: string | number, name: string) => {programStore.program[idx][name] = value}"
          @delete="removeStep(idx)"
          :name="step.name"
          :temperature="step.temperature"
          :time="step.time"
          :fixed="step.fixed"
          :pumpState="step.pumpState"
        >
        </ProgramFormStep>
        <v-card-actions>
          <v-btn
            variant="outlined"
            color="info"
            size="x-small"
            icon
            @click="programStore.addStep()"
          >
            <v-icon>mdi-plus</v-icon>
          </v-btn>
          <v-btn type="submit">Submit</v-btn>
        </v-card-actions>
      </v-form>
    </div>
  </v-card>
</template>
