import { reactive, ref } from "vue";
import { defineStore } from "pinia";

export interface Step {
  name: string,
  temperature: number,
  time: number,
  pumpState: boolean,
  fixed: boolean,
  wait: boolean
}

export const useProgramStore = defineStore("program", () => {
  
  const program: Step[] = reactive([]);
  let error = ref(false); 
  let loaded = ref(false)

  function addStep() {
    const emptyStep = {
      name: "",
      temperature: 20,
      time: 15,
      fixed: false,
      wait: false,
      pumpState: true
    }
    const programLength = this.program.length
    this.program.splice(programLength - 2, 0, emptyStep)
  }

  return { program, error, loaded, addStep };
});

