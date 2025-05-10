import { useQuery } from '@tanstack/react-query';
import type { GameFilter, JsonResponse } from '@/models/utils';
import { gamesService } from '../gamesService';
import type { Game } from '@/models/game';

export const useGetGames = (params: GameFilter) => {
  return useQuery<JsonResponse<Game[]>>({
    queryKey: ['games', params],
    queryFn: async () => {
      return await gamesService.getGames(params);
    },
  });
};
