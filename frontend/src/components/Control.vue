<script setup lang="ts">
import axios from "axios";
import { ref } from "vue";
import { SET_STATE_URL, START_URL, STOP_URL } from "@/urls";
import { useSetStateStore } from "@/stores/setState";
import { useStateStore } from "@/stores/state";

interface SetStateResponse {
  temperature: number | null;
  pump_state: boolean;
  duration: number | null;
}

const formValid = ref(true);

const setStateStore = useSetStateStore();
const stateStore = useStateStore();

const durationValidation = (value: number | null) => {
  if (value == null) return true;
  const valid = value >= 0 && value <= 120;
  return valid || "Must be between 0 and 120";
};

const patchStore = (data: SetStateResponse) => {
  setStateStore.$patch({
    temperature: data.temperature,
    pumpState: data.pump_state,
    duration: data.duration,
  });
  setStateStore.error = false;
  setStateStore.loaded = true;
};

axios
  .get<SetStateResponse>(SET_STATE_URL)
  .then((response) => {
    patchStore(response.data);
  })
  .catch((error) => {
    setStateStore.error = true;
    setStateStore.loaded = true;
  });

const submit = async (evt: SubmitEvent) => {
  if (!formValid.value) return;
  setStateStore.loaded = false;
  const formData = new FormData(evt.target);
  const data = {
    pump_state: false,
    duration: null,
    ...Object.fromEntries(formData.entries()),
  };
  try {
    const resp = await axios.post<SetStateResponse>(SET_STATE_URL, data);
    patchStore(resp.data);
  } catch (errors) {
    setStateStore.error = true;
    setStateStore.loaded = true;
  }
};

// TODO error handling and such
const startProgram = async () => {
  setStateStore.loaded = false;
  try {
    const resp = await axios.post<SetStateResponse>(START_URL);
    patchStore(resp.data);
  } catch (errors) {
    setStateStore.error = true;
    setStateStore.loaded = true;
  }
};

const stopProgram = async () => {
  setStateStore.loaded = false;
  try {
    const resp = await axios.post<SetStateResponse>(STOP_URL);
    patchStore(resp.data);
  } catch (errors) {
    setStateStore.error = true;
    setStateStore.loaded = true;
  }
};
</script>

<template>
  <v-card title="Control" subtitle="Control target state">
    <v-card-item v-if="setStateStore.error">
      <v-alert density="compact" type="error"
        >Unable to load target state.</v-alert
      >
    </v-card-item>
    <v-card-text v-else>
      <v-form @submit.prevent="submit" v-model="formValid">
        <v-container>
          <v-row dense>
            <v-col cols="8" sm="3">
              <v-text-field
                label="Temperature"
                :model-value="setStateStore.temperature"
                type="number"
                step="0.1"
                suffix="℃"
                :rules="[
                  (v) => (v >= 0 && v <= 100) || 'Must be between 0 and 100',
                ]"
                name="temperature"
                :loading="!setStateStore.loaded"
              ></v-text-field>
            </v-col>
            <v-col cols="8" sm="3">
              <v-text-field
                label="Time"
                :model-value="setStateStore.duration"
                type="number"
                suffix="min"
                :rules="[durationValidation]"
                step="1"
                :disabled="!stateStore.running"
                name="duration"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row dense>
            <v-col cols="8" sm="3">
              <v-switch
                :model-value="setStateStore.pumpState"
                label="Pump"
                color="success"
                name="pump_state"
              ></v-switch>
            </v-col>
            <v-col cols="8" sm="3" align-self="center">
              <v-btn type="submit">Submit</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
      <v-card-actions>
        <v-btn
          variant="outlined"
          v-if="stateStore.running"
          color="red"
          @click="stopProgram"
          >Abort</v-btn
        >
        <v-btn v-else variant="outlined" @click="startProgram"
          >Start Program</v-btn
        >
      </v-card-actions>
    </v-card-text>
  </v-card>
</template>
