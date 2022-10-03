import { reactive } from "vue";
import { defineStore } from "pinia";

export const useProgramStore = defineStore("program", () => {
  
  const program = reactive([]);
  const step = (idx: number) => program[idx];

  return { program, step };
});

