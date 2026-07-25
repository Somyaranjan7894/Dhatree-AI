import { apiClient } from './client';
import { CropRecommendation, CropRecommendationCreate } from '../types/crop_recommendation.types';

export const cropRecommendationService = {
  predictCrop: async (data: CropRecommendationCreate): Promise<CropRecommendation> => {
    const response = await apiClient.post<{status: string, data: CropRecommendation}>('/crop-recommendation/predictions/', data) as any;
    return response.data;
  },

  getPredictionHistory: async (): Promise<CropRecommendation[]> => {
    const response = await apiClient.get<{status: string, data: CropRecommendation[]}>('/crop-recommendation/predictions/') as any;
    return response.data;
  },
};
