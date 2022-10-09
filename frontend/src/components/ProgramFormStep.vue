<script setup lang="ts">
const props = defineProps({
  name: String,
  temperature: Number,
  time: Number,
  fixed: Boolean,
  pumpState: Boolean,
});

const emit = defineEmits(["change", "delete"]);

const checkHandler = (evt: Event, name: string) => {
  const target = evt.target as HTMLInputElement;
  emit("change", Boolean(target.checked), name);
};

const changeHandler = (evt: Event, name: string) => {
  const target = evt.target as HTMLInputElement;
  emit("change", target.value, name);
};

const numberChangeHandler = (evt: Event, name: string) => {
  const target = evt.target as HTMLInputElement;
  emit("change", Number(target.value), name);
};
</script>

<template>
  <v-row>
    <v-col cols="8" md="2">
      <v-text-field
        label="Name"
        :model-value="props.name"
        @change="changeHandler($event, 'name')"
        :rules="[(v) => !!v || 'Name is required']"
        :disabled="props.fixed"
      ></v-text-field>
    </v-col>
    <v-col cols="8" md="2">
      <v-text-field
        label="Temperature"
        @change="numberChangeHandler($event, 'temperature')"
        :model-value="props.temperature"
        type="number"
        step="0.1"
        suffix="℃"
        max="100"
        min="0"
      ></v-text-field>
    </v-col>
    <v-col cols="8" md="2">
      <v-text-field
        label="Time"
        @change="numberChangeHandler($event, 'time')"
        :model-value="props.time"
        type="number"
        suffix="min"
        step="1"
        min="5"
        max="120"
      ></v-text-field>
    </v-col>
    <v-col cols="8" md="1">
      <v-switch
        @change="checkHandler($event, 'pumpState')"
        :model-value="props.pumpState"
        label="Pump"
        color="success"
        :disabled="props.fixed"
      ></v-switch>
    </v-col>
    <v-col cols="8" md="1">
      <v-btn
        variant="outlined"
        color="error"
        size="x-small"
        icon
        :disabled="props.fixed"
        @click="$emit('delete')"
      >
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-col>
  </v-row>
</template>
