import { apiClient } from './client';
import { ENDPOINTS } from "./endpoints";

export const cropService = {
  getCrops: async () => {
    const response: any = await apiClient.get(ENDPOINTS.CROPS.LIST);
    return response.data || response;
  },
};
