<script setup lang="ts">
const props = defineProps({
  idx: Number,
  name: String,
  temperature: Number,
  time: Number,
  pumpState: Boolean,
  loading: Boolean,
  wait: Boolean,
});

const emit = defineEmits(["delete"]);
</script>

<template>
  <v-container>
    <v-row dense>
      <v-col cols="8" md="3">
        <v-text-field
          label="Name"
          :name="`name.${idx}`"
          :model-value="props.name"
          :rules="[(v) => !!v || 'Name is required']"
          :loading="props.loading"
          hide-details="auto"
        ></v-text-field>
      </v-col>
      <v-col cols="8" md="3">
        <v-text-field
          label="Temperature"
          :model-value="props.temperature"
          type="number"
          step="0.1"
          suffix="℃"
          :name="`temperature.${idx}`"
          :loading="props.loading"
          :rules="[(v) => v >= 0 || v <= 100 || 'Must be between 0 and 100']"
          hide-details="auto"
        ></v-text-field>
      </v-col>
      <v-col cols="8" md="3">
        <v-text-field
          label="Time"
          :model-value="props.time"
          type="number"
          suffix="min"
          step="1"
          :name="`time.${idx}`"
          :rules="[(v) => v > 1 || v <= 120 || 'Must be between 1 and 120']"
          :loading="props.loading"
          hide-details="auto"
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row dense>
      <v-col cols="3">
        <v-switch
          :model-value="props.pumpState"
          label="Pump"
          color="success"
          :loading="props.loading"
          :name="`pump_state.${idx}`"
          hide-details="auto"
        ></v-switch>
      </v-col>
      <v-col cols="3">
        <v-switch
          :model-value="props.wait"
          label="Wait"
          color="success"
          :loading="props.loading"
          :name="`wait.${idx}`"
          hide-details="auto"
        ></v-switch>
      </v-col>
      <v-col cols="3" class="d-flex justify-center">
        <v-btn
          variant="outlined"
          color="error"
          size="x-small"
          icon
          @click="$emit('delete')"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>
