import { ref } from "vue";
import type { Ref } from "vue";
import { defineStore } from "pinia";

export interface Step {
  name: string,
  temperature: number,
  time: number,
  pumpState: boolean,
  wait: boolean
}

export const useProgramStore = defineStore("program", () => {
  
  const program: Ref<Step[]> = ref([]);
  let error = ref(false); 
  let loaded = ref(false)

  function addStep() {
    const emptyStep = {
      name: "",
      temperature: 20,
      time: 15,
      wait: false,
      pumpState: true
    }
    this.program.push(emptyStep)
  }

  function removeStep (idx: number) {
    this.program = this.program.filter((_, i) => i !== idx);
  };

  return { program, error, loaded, addStep, removeStep };
});

