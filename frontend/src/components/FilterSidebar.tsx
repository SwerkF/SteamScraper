'use client';

import { Slider } from '@/components/ui/slider';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';
import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';
import {
  Cpu,
  CpuIcon as Gpu,
  MemoryStickIcon as Memory,
  Monitor,
  Building,
  Calendar,
  DollarSign,
} from 'lucide-react';
import { useGetFilters } from '@/api/queries/filterQueries';
import React from 'react';

export default function FilterSidebar() {
  const { data: filters, isLoading: isLoadingFilters } = useGetFilters();

  // State for searches
  const [cpuSearch, setCpuSearch] = React.useState("");
  const [gpuSearch, setGpuSearch] = React.useState("");
  const [ramSearch, setRamSearch] = React.useState("");
  const [osSearch, setOsSearch] = React.useState("");

  // Filtered data
  const filteredCpus = React.useMemo(() => {
    if (!filters?.data?.cpu) return [];
    if (!cpuSearch) return filters.data.cpu.slice(0, 50);

    return filters.data.cpu.filter(cpu =>
      cpu.name.toLowerCase().includes(cpuSearch.toLowerCase())
    );
  }, [filters?.data?.cpu, cpuSearch]);

  const filteredGpus = React.useMemo(() => {
    if (!filters?.data?.gpu) return [];
    if (!gpuSearch) return filters.data.gpu.slice(0, 50);

    return filters.data.gpu.filter(gpu =>
      gpu.name.toLowerCase().includes(gpuSearch.toLowerCase())
    );
  }, [filters?.data?.gpu, gpuSearch]);

  const filteredRam = React.useMemo(() => {
    if (!filters?.data?.memory) return [];
    if (!ramSearch) return filters.data.memory;

    return filters.data.memory.filter(ram =>
      ram.name.toLowerCase().includes(ramSearch.toLowerCase())
    );
  }, [filters?.data?.memory, ramSearch]);

  const filteredOs = React.useMemo(() => {
    if (!filters?.data?.os) return [];
    if (!osSearch) return filters.data.os;

    return filters.data.os.filter(os =>
      os.name.toLowerCase().includes(osSearch.toLowerCase())
    );
  }, [filters?.data?.os, osSearch]);

  if (isLoadingFilters) {
    return <div>Loading...</div>;
  }

  return (
    <div className="space-y-6 pr-4">
      {filters && filters.data && (
        <>
          <h2 className="text-xl font-bold mb-4 text-foreground">Filtres</h2>

          <Accordion type="multiple" defaultValue={['name', 'hardware', 'price']}>
            <AccordionItem value="name">
              <AccordionTrigger>Nom</AccordionTrigger>
              <AccordionContent>
                <div className="space-y-2">
                  <Input placeholder="Rechercher par nom..." />
                </div>
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="hardware">
              <AccordionTrigger>Configuration</AccordionTrigger>
              <AccordionContent>
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="cpu" className="flex items-center gap-2">
                      <Cpu className="h-4 w-4" />
                      CPU
                    </Label>
                    <Select>
                      <SelectTrigger id="cpu">
                        <SelectValue placeholder="Sélectionner CPU" />
                      </SelectTrigger>
                      <SelectContent withSearch onSearchChange={setCpuSearch}>
                        {filteredCpus.map((item) => (
                          <SelectItem key={item.id} value={item.name}>
                            {item.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="gpu" className="flex items-center gap-2">
                      <Gpu className="h-4 w-4" />
                      GPU
                    </Label>
                    <Select>
                      <SelectTrigger id="gpu">
                        <SelectValue placeholder="Sélectionner GPU" />
                      </SelectTrigger>
                      <SelectContent withSearch onSearchChange={setGpuSearch}>
                        {filteredGpus.map((item) => (
                          <SelectItem key={item.id} value={item.name}>
                            {item.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="ram" className="flex items-center gap-2">
                      <Memory className="h-4 w-4" />
                      RAM
                    </Label>
                    <Select>
                      <SelectTrigger id="ram">
                        <SelectValue placeholder="Sélectionner RAM" />
                      </SelectTrigger>
                      <SelectContent withSearch onSearchChange={setRamSearch}>
                        {filteredRam.map((item) => (
                          <SelectItem key={item.id} value={item.name}>
                            {item.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="os" className="flex items-center gap-2">
                      <Monitor className="h-4 w-4" />
                      Système d'exploitation
                    </Label>
                    <Select>
                      <SelectTrigger id="os">
                        <SelectValue placeholder="Sélectionner OS" />
                      </SelectTrigger>
                      <SelectContent withSearch onSearchChange={setOsSearch}>
                        {filteredOs.map((item) => (
                          <SelectItem key={item.id} value={item.name}>
                            {item.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="publisher">
              <AccordionTrigger className="flex items-center gap-2">
                <Building className="h-4 w-4" />
                Éditeur
              </AccordionTrigger>
              <AccordionContent>
                <div className="space-y-2">
                  <div className="flex items-center space-x-2">
                    <Checkbox id="valve" />
                    <label htmlFor="valve" className="text-sm">
                      Valve
                    </label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Checkbox id="ubisoft" />
                    <label htmlFor="ubisoft" className="text-sm">
                      Ubisoft
                    </label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Checkbox id="ea" />
                    <label htmlFor="ea" className="text-sm">
                      Electronic Arts
                    </label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Checkbox id="cdpr" />
                    <label htmlFor="cdpr" className="text-sm">
                      CD Projekt Red
                    </label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Checkbox id="bethesda" />
                    <label htmlFor="bethesda" className="text-sm">
                      Bethesda
                    </label>
                  </div>
                </div>
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="year">
              <AccordionTrigger className="flex items-center gap-2">
                <Calendar className="h-4 w-4" />
                Année de sortie
              </AccordionTrigger>
              <AccordionContent>
                <div className="space-y-4">
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">2010</span>
                    <span className="text-sm text-muted-foreground">2025</span>
                  </div>
                  <Slider
                    defaultValue={[2010, 2025]}
                    min={2010}
                    max={2025}
                    step={1}
                  />
                  <div className="flex gap-2">
                    <Input type="number" placeholder="Min" min={2010} max={2025} />
                    <Input type="number" placeholder="Max" min={2010} max={2025} />
                  </div>
                </div>
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="price">
              <AccordionTrigger className="flex items-center gap-2">
                <DollarSign className="h-4 w-4" />
                Prix
              </AccordionTrigger>
              <AccordionContent>
                <div className="space-y-4">
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">0€</span>
                    <span className="text-sm text-muted-foreground">100€</span>
                  </div>
                  <Slider defaultValue={[0, 100]} min={0} max={100} step={1} />
                  <div className="flex gap-2">
                    <Input type="number" placeholder="Min" min={0} max={100} />
                    <Input type="number" placeholder="Max" min={0} max={100} />
                  </div>
                </div>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </>
      )}
      <Button className="w-full mt-4">Appliquer les filtres</Button>
    </div>
  );
}
