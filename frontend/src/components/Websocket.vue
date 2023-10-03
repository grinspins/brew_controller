<script setup lang="ts">
import { useStateStore } from "../stores/state";
import { STATE_URL } from "../urls";

const state = useStateStore();

let intervalId: number | undefined = undefined;

const stateTick = (ws: WebSocket) => {
  intervalId = setInterval(() => {
    if (ws.readyState !== WebSocket.OPEN) {
      clearInterval(intervalId);
      state.error = true;
      connectWebsocket();
    }
    ws.send("");
  }, 1000);
};

const connectWebsocket = () => {
  const ws = new WebSocket(STATE_URL);
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    state.$patch({
      temperature: data.temperature,
      pumpState: data.pump_state,
      step: data.step_idx,
      remainingTime: data.remaining_time,
      error: false,
    });
  };
  ws.onerror = () => {
    state.error = true;
  };
  ws.onopen = () => {
    stateTick(ws);
  };
};

connectWebsocket();
</script>

<template></template>
