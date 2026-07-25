import { apiClient } from './client';
import { ENDPOINTS } from "./endpoints";

export const cropService = {
  getCrops: async () => {
    const response = await apiClient.get<{ data: any[] }>(ENDPOINTS.CROPS.LIST);
    return response.data.data;
  },
};
