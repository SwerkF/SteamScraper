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

export default function FilterSidebar() {
  return (
    <div className="space-y-6 pr-4">
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
                  <SelectContent>
                    <SelectItem value="intel-i5">Intel Core i5</SelectItem>
                    <SelectItem value="intel-i7">Intel Core i7</SelectItem>
                    <SelectItem value="intel-i9">Intel Core i9</SelectItem>
                    <SelectItem value="amd-ryzen5">AMD Ryzen 5</SelectItem>
                    <SelectItem value="amd-ryzen7">AMD Ryzen 7</SelectItem>
                    <SelectItem value="amd-ryzen9">AMD Ryzen 9</SelectItem>
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
                  <SelectContent>
                    <SelectItem value="nvidia-1650">NVIDIA GTX 1650</SelectItem>
                    <SelectItem value="nvidia-1660">NVIDIA GTX 1660</SelectItem>
                    <SelectItem value="nvidia-2060">NVIDIA RTX 2060</SelectItem>
                    <SelectItem value="nvidia-3060">NVIDIA RTX 3060</SelectItem>
                    <SelectItem value="nvidia-3070">NVIDIA RTX 3070</SelectItem>
                    <SelectItem value="nvidia-4070">NVIDIA RTX 4070</SelectItem>
                    <SelectItem value="amd-6600">AMD RX 6600</SelectItem>
                    <SelectItem value="amd-6700">AMD RX 6700</SelectItem>
                    <SelectItem value="amd-7600">AMD RX 7600</SelectItem>
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
                  <SelectContent>
                    <SelectItem value="4gb">4 GB</SelectItem>
                    <SelectItem value="8gb">8 GB</SelectItem>
                    <SelectItem value="16gb">16 GB</SelectItem>
                    <SelectItem value="32gb">32 GB</SelectItem>
                    <SelectItem value="64gb">64 GB</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="os" className="flex items-center gap-2">
                  <Monitor className="h-4 w-4" />
                  Système d'exploitation
                </Label>
                <div className="space-y-2">
                  <div className="flex items-center space-x-2">
                    <Checkbox id="windows" />
                    <label htmlFor="windows" className="text-sm">
                      Windows
                    </label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Checkbox id="macos" />
                    <label htmlFor="macos" className="text-sm">
                      macOS
                    </label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Checkbox id="linux" />
                    <label htmlFor="linux" className="text-sm">
                      Linux
                    </label>
                  </div>
                </div>
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

      <Button className="w-full mt-4">Appliquer les filtres</Button>
    </div>
  );
}
