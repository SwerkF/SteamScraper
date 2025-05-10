import type { Cpu, Gpu, Memory, OS } from "./game";

export interface JsonResponse<T> {
  success: boolean;
  message?: string;
  data?: T;
}

export interface GameFilter {
  search: string;
  cpu: string;
  memory: string;
  gpu: string;
  storage: string;
  os: string;
  pricelow: number;
  pricehigh: number;
}

export interface Filters {
  cpu: Cpu[];
  memory: Memory[];
  gpu: Gpu[];
  os: OS[];
}
