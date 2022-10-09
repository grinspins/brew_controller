import { reactive, ref, computed } from "vue";
import { defineStore } from "pinia";

interface State {
  temperature: number,
  pumpState: boolean,
  remainingTime: number | null,
  step: number | null
}

export const useBrewStore = defineStore("brew", () => {

  const state: State = reactive({
    temperature: 0.0,
    pumpState: false,
    remainingTime: 0,
    step: null
  });
  const error = ref(false)
  const active = computed(() => !!state.step);

  return { state, error, active };
});

