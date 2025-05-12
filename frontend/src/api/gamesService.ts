import type { GameFilter, JsonResponse } from '@/models/utils';
import { api } from './interceptor';
import type { Game } from '@/models/game';

export class GamesService {
  private baseUrl = api.getUrl() + '/api/games';

  public async getGames(params: GameFilter): Promise<JsonResponse<Game[]>> {
    let paramsString = new URLSearchParams();
    if (params.search) paramsString.set('search', params.search);
    if (params.cpu) paramsString.set('cpu', params.cpu);
    if (params.memory) paramsString.set('memory', params.memory);
    if (params.gpu) paramsString.set('gpu', params.gpu);
    if (params.storage) paramsString.set('storage', params.storage);
    if (params.os) paramsString.set('os', params.os);
    if (params.pricelow)
      paramsString.set('pricelow', params.pricelow.toString());
    if (params.pricehigh)
      paramsString.set('pricehigh', params.pricehigh.toString());
    if (params.page) paramsString.set('page', params.page.toString());
    return api.fetchRequest(
      this.baseUrl + '?' + paramsString.toString(),
      'GET',
      null
    );
  }
}

export const gamesService = new GamesService();
