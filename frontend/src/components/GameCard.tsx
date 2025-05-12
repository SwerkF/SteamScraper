'use client';

import { useState } from 'react';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Eye } from 'lucide-react';
import type { Game } from '@/models/game';

export default function GameCard({ game }: { game: Game }) {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <Card
      className="overflow-hidden border-border/50 transition-all duration-300 hover:border-primary/50 hover:shadow-lg hover:shadow-primary/10 bg-card/50"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="relative object-fit overflow-hidden">
        <img
          src={game.image_url || '/placeholder.svg'}
          alt={game.name}
          className={`object-cover transition-all duration-500 ${
            isHovered ? 'scale-110 opacity-20' : 'scale-100 opacity-100'
          }`}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent opacity-60"></div>

        <div
          className={`absolute inset-0 flex items-center justify-center transition-opacity duration-300 ${
            isHovered ? 'opacity-100' : 'opacity-0'
          }`}
        >
          <Button
            variant="secondary"
            onClick={() => window.open(game.store_url, '_blank')}
            size="sm"
            className="gap-2 cursor-pointer"
          >
            <Eye className="h-4 w-4" />
            Direction Steam
          </Button>
        </div>

        <Badge className="absolute top-3 right-3 bg-primary/80 hover:bg-primary">
          {game.price === 0 ? 'Free to play' : game.price + ' €'}
        </Badge>
      </div>

      <CardContent className="p-4">
        <h3 className="font-bold text-lg truncate">{game.name}</h3>
        <p className="text-xs text-muted-foreground mb-2">Système</p>

        {game.supported_systems.split(' ').map(system => (
          <Badge key={system} variant="outline" className="text-xs">
            {system}
          </Badge>
        ))}
      </CardContent>

      <CardFooter className="p-4 pt-0 flex justify-between">
        <div className="flex flex-col gap-2">
          <p className="text-xs text-muted-foreground">Editeur</p>
          <Badge variant="outline" className="text-xs">
            {game.publisher}
          </Badge>
        </div>
        <div className="flex flex-col gap-2">
          <p className="text-xs text-muted-foreground">Date de sortie</p>
          <Badge variant="outline" className="text-xs">
            {game.release_date.split('–')[0]}
          </Badge>
        </div>
      </CardFooter>
    </Card>
  );
}
