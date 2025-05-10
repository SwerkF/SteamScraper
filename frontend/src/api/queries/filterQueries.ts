import type { Filters, JsonResponse } from "@/models/utils";
import { filterService } from "../filterService";
import { useQuery } from "@tanstack/react-query";

export const useGetFilters = () => {
  return useQuery<JsonResponse<Filters>>({
    queryKey: ['filters'],
    queryFn: async () => {
      return await filterService.getFilters();
    },
  });
};


