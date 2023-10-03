<script setup lang="ts">
import axios from "axios";
import { ref } from "vue";
import { useProgramStore } from "@/stores/program";
import { PROGRAM_URL } from "@/urls";
import ProgramFormStep from "./ProgramFormStep.vue";

interface Step {
  name: string;
  temperature: number;
  time: number;
  pump_state: boolean;
  wait: boolean;
}

const programStore = useProgramStore();
const formValid = ref(true);

const patchProgram = (data: Step[]) => {
  const program = data.map((step) => ({
    name: step.name,
    temperature: step.temperature,
    time: step.time,
    pumpState: step.pump_state,
    wait: step.wait,
  }));
  programStore.program = program;
  programStore.error = false;
  programStore.loaded = true;
};

axios
  .get<Step[]>(PROGRAM_URL)
  .then((response) => {
    patchProgram(response.data);
  })
  .catch((error) => {
    programStore.error = true;
    programStore.loaded = true;
  });

const submit = async (evt: SubmitEvent) => {
  if (!formValid.value) return;
  programStore.loaded = false;
  const formData = new FormData(evt.target as HTMLFormElement);
  const data: { [key: string]: string }[] = [];
  for (const [nameIdx, value] of formData.entries()) {
    const [name, idxStr] = nameIdx.split(".");
    const idx = Number(idxStr);
    const stepData = data[idx] || {};
    stepData[name] = value as string;
    data[idx] = stepData;
  }
  const newProgram: Step[] = data.map((stepData) => ({
    name: stepData.name,
    temperature: Number(stepData.temperature),
    time: Number(stepData.time),
    pump_state: Boolean(stepData.pump_state),
    wait: Boolean(stepData.wait),
  }));
  try {
    const resp = await axios.post<Step[]>(PROGRAM_URL, newProgram);
    patchProgram(resp.data);
  } catch (errors) {
    programStore.error = true;
  }
  programStore.loaded = true;
};
</script>
<template>
  <v-card title="Program" subtitle="Create a program to run">
    <v-card-item v-if="programStore.error">
      <v-alert density="compact" type="error">Unable to load program.</v-alert>
    </v-card-item>
    <v-card-text v-else>
      <v-form @submit.prevent="submit" v-model="formValid">
        <ProgramFormStep
          v-for="(step, idx) in programStore.program"
          :key="`${step.name}.${idx}`"
          @delete="programStore.removeStep(idx)"
          :idx="idx"
          :name="step.name"
          :temperature="step.temperature"
          :time="step.time"
          :pumpState="step.pumpState"
          :loading="!programStore.loaded"
          :wait="step.wait"
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
          <v-btn type="submit" variant="outlined">Submit</v-btn>
        </v-card-actions>
      </v-form>
    </v-card-text>
  </v-card>
</template>
