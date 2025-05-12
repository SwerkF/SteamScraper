'use client';

import React, { useEffect } from 'react';
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
import { Button } from '@/components/ui/button';
import {
  Cpu,
  CpuIcon as Gpu,
  MemoryStickIcon as Memory,
  Monitor,
  Building,
  Calendar,
  DollarSign,
  X,
} from 'lucide-react';
import { useGetFilters } from '@/api/queries/filterQueries';
import type { GameFilter } from '@/models/utils';

export default function FilterSidebar({
  onApplyFilters,
}: {
  onApplyFilters: (filters: GameFilter) => void;
}) {
  const { data: filters, isLoading: isLoadingFilters } = useGetFilters();

  const [cpuSearch, setCpuSearch] = React.useState('');
  const [gpuSearch, setGpuSearch] = React.useState('');
  const [ramSearch, setRamSearch] = React.useState('');
  const [osSearch, setOsSearch] = React.useState('');

  const [cpuQuery, setCpuQuery] = React.useState('');
  const [gpuQuery, setGpuQuery] = React.useState('');
  const [ramQuery, setRamQuery] = React.useState('');
  const [osQuery, setOsQuery] = React.useState('');

  const [priceLow, setPriceLow] = React.useState(0);
  const [priceHigh, setPriceHigh] = React.useState(100);
  const [search, setSearch] = React.useState('');

  const handleClearFilter = (type: 'cpu' | 'gpu' | 'memory' | 'os') => {
    switch (type) {
      case 'cpu':
        setCpuSearch('');
        setCpuQuery('');
        break;
      case 'gpu':
        setGpuSearch('');
        setGpuQuery('');
        break;
      case 'memory':
        setRamSearch('');
        setRamQuery('');
        break;
      case 'os':
        setOsSearch('');
        setOsQuery('');
        break;
    }
  };

  if (isLoadingFilters) {
    return <div>Chargement des filtres...</div>;
  }

  const handleApplyFilters = () => {
    onApplyFilters({
      cpu: cpuSearch,
      gpu: gpuSearch,
      memory: ramSearch,
      os: osSearch,
      search: search,
      storage: '',
      pricelow: priceLow,
      pricehigh: priceHigh,
    });
  };

  return (
    <div className="space-y-6 pr-4">
      {filters && filters.data && (
        <>
          <h2 className="text-xl font-bold mb-4 text-foreground">Filtres</h2>

          <Accordion
            type="multiple"
            defaultValue={['name', 'hardware', 'price']}
          >
            <AccordionItem value="name">
              <AccordionTrigger>Nom</AccordionTrigger>
              <AccordionContent>
                <div className="space-y-2">
                  <Input
                    placeholder="Rechercher par nom..."
                    onChange={e => setSearch(e.target.value)}
                  />
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
                    {cpuSearch ? (
                      <div className="flex items-center justify-between border rounded-md p-2">
                        <span className="truncate">{cpuSearch}</span>
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => handleClearFilter('cpu')}
                          className="h-6 w-6"
                        >
                          <X className="h-4 w-4" />
                        </Button>
                      </div>
                    ) : (
                      <Select onValueChange={value => setCpuSearch(value)}>
                        <SelectTrigger id="cpu">
                          <SelectValue placeholder="Sélectionner CPU" />
                        </SelectTrigger>
                        <SelectContent
                          withSearch
                          onSearchChange={value => setCpuQuery(value)}
                        >
                          {filters.data.cpu
                            .filter(cpu =>
                              cpu.name
                                .toLowerCase()
                                .includes(cpuQuery.toLowerCase())
                            )
                            .slice(0, 20)
                            .map(item => (
                              <SelectItem key={item.id} value={item.name}>
                                {item.name}
                              </SelectItem>
                            ))}
                        </SelectContent>
                      </Select>
                    )}
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="gpu" className="flex items-center gap-2">
                      <Gpu className="h-4 w-4" />
                      GPU
                    </Label>
                    {gpuSearch ? (
                      <div className="flex items-center justify-between border rounded-md p-2">
                        <span className="truncate">{gpuSearch}</span>
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => handleClearFilter('gpu')}
                          className="h-6 w-6"
                        >
                          <X className="h-4 w-4" />
                        </Button>
                      </div>
                    ) : (
                      <Select onValueChange={value => setGpuSearch(value)}>
                        <SelectTrigger id="gpu">
                          <SelectValue placeholder="Sélectionner GPU" />
                        </SelectTrigger>
                        <SelectContent
                          withSearch
                          onSearchChange={value => setGpuQuery(value)}
                        >
                          {filters.data.gpu
                            .filter(gpu =>
                              gpu.name
                                .toLowerCase()
                                .includes(gpuQuery.toLowerCase())
                            )
                            .slice(0, 20)
                            .map(item => (
                              <SelectItem key={item.id} value={item.name}>
                                {item.name}
                              </SelectItem>
                            ))}
                        </SelectContent>
                      </Select>
                    )}
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="ram" className="flex items-center gap-2">
                      <Memory className="h-4 w-4" />
                      RAM
                    </Label>
                    {ramSearch ? (
                      <div className="flex items-center justify-between border rounded-md p-2">
                        <span className="truncate">{ramSearch}</span>
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => handleClearFilter('memory')}
                          className="h-6 w-6"
                        >
                          <X className="h-4 w-4" />
                        </Button>
                      </div>
                    ) : (
                      <Select onValueChange={value => setRamSearch(value)}>
                        <SelectTrigger id="ram">
                          <SelectValue placeholder="Sélectionner RAM" />
                        </SelectTrigger>
                        <SelectContent
                          withSearch
                          onSearchChange={value => setRamQuery(value)}
                        >
                          {filters.data.memory
                            .filter(ram =>
                              ram.name
                                .toLowerCase()
                                .includes(ramQuery.toLowerCase())
                            )
                            .slice(0, 20)
                            .map(item => (
                              <SelectItem key={item.id} value={item.name}>
                                {item.name}
                              </SelectItem>
                            ))}
                        </SelectContent>
                      </Select>
                    )}
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="os" className="flex items-center gap-2">
                      <Monitor className="h-4 w-4" />
                      Système d'exploitation
                    </Label>
                    {osSearch ? (
                      <div className="flex items-center justify-between border rounded-md p-2">
                        <span className="truncate">{osSearch}</span>
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => handleClearFilter('os')}
                          className="h-6 w-6"
                        >
                          <X className="h-4 w-4" />
                        </Button>
                      </div>
                    ) : (
                      <Select onValueChange={value => setOsSearch(value)}>
                        <SelectTrigger id="os">
                          <SelectValue placeholder="Sélectionner OS" />
                        </SelectTrigger>
                        <SelectContent
                          withSearch
                          onSearchChange={value => setOsQuery(value)}
                        >
                          {filters.data.os
                            .filter(os =>
                              os.name
                                .toLowerCase()
                                .includes(osQuery.toLowerCase())
                            )
                            .slice(0, 20)
                            .map(item => (
                              <SelectItem key={item.id} value={item.name}>
                                {item.name}
                              </SelectItem>
                            ))}
                        </SelectContent>
                      </Select>
                    )}
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
                    <span className="text-sm text-muted-foreground">500€</span>
                  </div>
                  <Slider
                    defaultValue={[0, 500]}
                    min={1}
                    max={500}
                    step={1}
                    value={[priceLow, priceHigh]}
                    onValueChange={value => {
                      setPriceLow(value[0]);
                      setPriceHigh(value[1] || 0);
                    }}
                  />
                  <div className="flex gap-2">
                    <Input
                      type="number"
                      placeholder="Min"
                      value={priceLow}
                      min={1}
                      max={500}
                      onChange={e => setPriceLow(Number(e.target.value))}
                    />
                    <Input
                      type="number"
                      placeholder="Max"
                      value={priceHigh}
                      min={1}
                      max={500}
                      onChange={e => setPriceHigh(Number(e.target.value))}
                    />
                  </div>
                </div>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </>
      )}
      <Button className="w-full mt-4" onClick={handleApplyFilters}>
        Appliquer les filtres
      </Button>
    </div>
  );
}
