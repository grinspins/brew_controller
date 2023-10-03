import { ref, computed } from "vue";
import type { Ref } from "vue";
import { defineStore } from "pinia";


export const useStateStore = defineStore("state", () => {

  const temperature = ref(0.0)
  const pumpState = ref(false)
  const remainingTime: Ref<number | null> = ref(null)
  const step: Ref<number | null> = ref(null)
  const error = ref(false)
  const running = computed(() => !!step.value);

  return { temperature, pumpState, remainingTime, step, error, running };
});

