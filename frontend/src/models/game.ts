export interface Game {
  id: number;
  name: string;
  description: string;
  image_url: string;
  price: number;
  store_url: string;
  app_id: number;
  developer: string;
  supported_systems: string;
  requirements: GameRequirements;
  release_date: string;
  publisher: string;
}

export interface GameRequirements {
  cpu: Cpu;
  memory: Memory;
  gpu: Gpu;
  storage: Storage;
  os: OS;
}

export interface Cpu {
  id: number;
  name: string;
}

export interface Memory {
  id: number;
  name: string;
}

export interface Gpu {
  id: number;
  name: string;
}

export interface Storage {
  id: number;
  name: string;
}

export interface OS {
  id: number;
  name: string;
}
