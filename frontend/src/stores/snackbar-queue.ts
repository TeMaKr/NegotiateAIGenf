import { defineStore } from "pinia";
import { ref } from "vue";

interface Message {
  color: string;
  text: string;
  variant: "flat" | "tonal";
}

export const useSnackbarQueueStore = defineStore("snackbarQueue", () => {
  const queue = ref<Message[]>([]);

  const appendError = (message: string) => {
    queue.value.push({
      color: "error",
      text: message,
      variant: "tonal",
    });
  };

  const appendSuccess = (message: string) => {
    queue.value.push({
      color: "primary",
      text: message,
      variant: "tonal",
    });
  };

  return {
    queue,
    appendError,
    appendSuccess,
  };
});
