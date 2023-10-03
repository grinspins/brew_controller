import { ref } from "vue";
import type {Ref} from "vue";
import { defineStore } from "pinia";

export const useSetStateStore = defineStore("setState", () => {
  const temperature = ref(0.0)
  const pumpState = ref(false)
  const duration: Ref<number | null> = ref(0)
  const error = ref(false);
  const loaded = ref(false);

  return { temperature, pumpState, duration, error, loaded };
});

