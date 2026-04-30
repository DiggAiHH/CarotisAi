import { useMutation } from "@tanstack/react-query";
import { apiClient } from "@/lib/apiClient";
import type { InferenceResponse } from "@/types";

export function useInference() {
  return useMutation<InferenceResponse, Error, File>({
    mutationFn: apiClient.predict,
  });
}
