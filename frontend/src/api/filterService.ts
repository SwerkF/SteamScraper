import type { Filters, JsonResponse } from '@/models/utils';
import { api } from './interceptor';

export class FilterService {
  private baseUrl = api.getUrl() + '/api/filters';

  public async getFilters(): Promise<JsonResponse<Filters>> {
    return api.fetchRequest(this.baseUrl, 'GET', null, false);
  }
}

export const filterService = new FilterService();
