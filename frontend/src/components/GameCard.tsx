'use client';

import { useState } from 'react';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Eye } from 'lucide-react';

interface Game {
  id: number;
  name: string;
  price: string;
  image: string;
  tags: string[];
}

export default function GameCard({ game }: { game: Game }) {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <Card
      className="overflow-hidden border-border/50 transition-all duration-300 hover:border-primary/50 hover:shadow-lg hover:shadow-primary/10 bg-card/50"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="relative aspect-[3/2] overflow-hidden">
        <img
          src={game.image || '/placeholder.svg'}
          alt={game.name}
          className={`object-cover transition-transform duration-500 ${
            isHovered ? 'scale-110' : 'scale-100'
          }`}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent opacity-60"></div>

        {/* Overlay content that appears on hover */}
        <div
          className={`absolute inset-0 flex items-center justify-center transition-opacity duration-300 ${
            isHovered ? 'opacity-100' : 'opacity-0'
          }`}
        >
          <Button variant="secondary" size="sm" className="gap-2">
            <Eye className="h-4 w-4" />
            Voir détails
          </Button>
        </div>

        {/* Price badge */}
        <Badge className="absolute top-3 right-3 bg-primary/80 hover:bg-primary">
          {game.price}
        </Badge>
      </div>

      <CardContent className="p-4">
        <h3 className="font-bold text-lg truncate">{game.name}</h3>
        <div className="flex flex-wrap gap-2 mt-2">
          {game.tags.map((tag, index) => (
            <Badge key={index} variant="outline" className="text-xs">
              {tag}
            </Badge>
          ))}
        </div>
      </CardContent>

      <CardFooter className="p-4 pt-0 flex justify-between">
        <div className="flex items-center text-sm text-muted-foreground">
          <span>{'★'.repeat(Math.floor(3 + Math.random() * 3))}</span>
          <span className="ml-1">{(3 + Math.random() * 2).toFixed(1)}</span>
        </div>
        <span className="text-xs text-muted-foreground">
          {2020 + Math.floor(Math.random() * 4)}
        </span>
      </CardFooter>
    </Card>
  );
}
