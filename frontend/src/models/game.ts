export interface Game {
  id: number;
  name: string;
  description: string;
  image: string;
  price: number;
  requirements: GameRequirements;
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
  description: string;
  image: string;
  price: number;
}

export interface Memory {
  id: number;
  name: string;
  description: string;
  image: string;
  price: number;
}

export interface Gpu {
  id: number;
  name: string;
  description: string;
  image: string;
  price: number;
}

export interface Storage {
  id: number;
  name: string;
}

export interface OS {
  id: number;
  name: string;
  description: string;
  image: string;
}
