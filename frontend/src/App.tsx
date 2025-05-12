import { Search } from 'lucide-react';
import GameCard from '@/components/GameCard';
import FilterSidebar from '@/components/FilterSidebar';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { useGetGames } from './api/queries/gamesQueries';
import { useEffect, useState } from 'react';
import type { GameFilter } from '@/models/utils';
import type { Game } from '@/models/game';

export default function App() {
  const [filters, setFilters] = useState<GameFilter>({
    search: '',
    cpu: '',
    memory: '',
    gpu: '',
    os: '',
    storage: '',
    pricelow: 0,
    pricehigh: 150,
    page: 1,
  });
  const [allGames, setAllGames] = useState<Game[]>([]);
  const { data: games, refetch } = useGetGames(filters);

  useEffect(() => {
    if (games?.data) {
      if (filters.page && filters.page > 1) {
        setAllGames(prev => [...prev, ...(games.data || [])]);
      } else {
        setAllGames(games.data || []);
      }
    }
  }, [games]);

  useEffect(() => {
    if (filters.page === 1) {
      setAllGames([]);
    }
    refetch();
  }, [filters]);

  const handleLoadMore = () => {
    setFilters({ ...filters, page: filters.page ? filters.page + 1 : 1 });
  };

  return (
    <div className="min-h-screen bg-background m-6">
      <header className="border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-10">
        <div className="container py-6">
          <div className="flex flex-col space-y-4">
            <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-purple-500 to-cyan-500 bg-clip-text text-transparent glitch-text">
              LET ME PLAY
            </h1>
            <p className="text-muted-foreground max-w-2xl">
              Explorez la base de données ultime des jeux Steam. Trouvez les
              titres qui correspondent parfaitement à votre configuration et à
              vos préférences.
            </p>
            <div className="flex justify-between">
              <div className="relative">
                <Input
                  type="search"
                  placeholder="Rechercher un jeu..."
                  className="pl-10 w-full md:w-96"
                />
                <Search className="absolute left-3 top-2.5 h-5 w-5 text-muted-foreground" />
              </div>
              <p className="text-muted-foreground text-right">
                Affichage de {allGames.length} jeux sur {games?.count}
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="container py-8">
        <div className="flex flex-col md:flex-row gap-8">
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
                <FilterSidebar onApplyFilters={setFilters} />
              </div>
            </SheetContent>
          </Sheet>

          <div className="hidden md:block md:w-1/4 lg:w-1/5">
            <FilterSidebar onApplyFilters={setFilters} />
          </div>

          <div className="md:w-3/4 lg:w-4/5">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {allGames.map((game, index) => (
                <GameCard
                  key={`${game.app_id || game.id}-${index}`}
                  game={game}
                />
              ))}
            </div>
            {allGames.length < (games?.count || 0) && (
              <div className="flex justify-center mt-8">
                <Button
                  variant="outline"
                  onClick={handleLoadMore}
                  disabled={!games?.data || games.data.length === 0}
                >
                  Charger plus
                </Button>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
