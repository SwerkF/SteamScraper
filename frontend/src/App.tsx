import { Search } from 'lucide-react';
import GameCard from '@/components/GameCard';
import FilterSidebar from '@/components/FilterSidebar';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';

export default function App() {
  // Données de jeux fictives pour la démo
  const games = [
    {
      id: 1,
      name: 'Cyberpunk 2077',
      price: '59.99€',
      image: 'https://placehold.co/600x800',
      tags: ['RPG', 'Open World'],
    },
    {
      id: 2,
      name: 'Half-Life: Alyx',
      price: '49.99€',
      image: 'https://placehold.co/600x800',
      tags: ['VR', 'FPS'],
    },
    {
      id: 3,
      name: 'Elden Ring',
      price: '59.99€',
      image: 'https://placehold.co/600x800',
      tags: ['Souls-like', 'Open World'],
    },
    {
      id: 4,
      name: 'Red Dead Redemption 2',
      price: '39.99€',
      image: 'https://placehold.co/600x800',
      tags: ['Action', 'Adventure'],
    },
    {
      id: 5,
      name: 'The Witcher 3',
      price: '29.99€',
      image: 'https://placehold.co/600x800',
      tags: ['RPG', 'Fantasy'],
    },
    {
      id: 6,
      name: "Baldur's Gate 3",
      price: '59.99€',
      image: 'https://placehold.co/600x800',
      tags: ['RPG', 'D&D'],
    },
    {
      id: 7,
      name: 'Hollow Knight',
      price: '14.99€',
      image: 'https://placehold.co/600x800',
      tags: ['Metroidvania', 'Indie'],
    },
    {
      id: 8,
      name: 'Hades',
      price: '24.99€',
      image: 'https://placehold.co/600x800',
      tags: ['Roguelike', 'Action'],
    },
    {
      id: 9,
      name: 'Disco Elysium',
      price: '39.99€',
      image: 'https://placehold.co/600x800',
      tags: ['RPG', 'Detective'],
    },
  ];

  return (
    <div className="min-h-screen bg-background m-6">
      {/* Header */}
      <header className="border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-10">
        <div className="container py-6">
          <div className="flex flex-col space-y-4">
            <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-purple-500 to-cyan-500 bg-clip-text text-transparent glitch-text">
              SCRAPYDB
            </h1>
            <p className="text-muted-foreground max-w-2xl">
              Explorez la base de données ultime des jeux Steam. Trouvez les
              titres qui correspondent parfaitement à votre configuration et à
              vos préférences.
            </p>
            <div className="relative">
              <Input
                type="search"
                placeholder="Rechercher un jeu..."
                className="pl-10 w-full md:w-96"
              />
              <Search className="absolute left-3 top-2.5 h-5 w-5 text-muted-foreground" />
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container py-8">
        <div className="flex flex-col md:flex-row gap-8">
          {/* Mobile Filter Toggle */}
          <Sheet>
            <SheetTrigger asChild>
              <Button
                variant="outline"
                className="md:hidden flex items-center gap-2 mb-4"
              >
                <Search className="h-4 w-4" />
                Filtres
              </Button>
            </SheetTrigger>
            <SheetContent side="left" className="w-[300px] sm:w-[400px]">
              <div className="py-4">
                <FilterSidebar />
              </div>
            </SheetContent>
          </Sheet>

          {/* Sidebar */}
          <div className="hidden md:block md:w-1/4 lg:w-1/5">
            <FilterSidebar />
          </div>

          {/* Game Grid */}
          <div className="md:w-3/4 lg:w-4/5">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {games.map(game => (
                <GameCard key={game.id} game={game} />
              ))}
            </div>
            <div className="flex justify-center mt-8">
              <Button variant="outline">Charger plus</Button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
