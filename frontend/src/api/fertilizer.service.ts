import { apiClient } from './client';
import { FertilizerPredictionCreate, FertilizerRecommendation } from '../types/fertilizer.types';

export const fertilizerService = {
  predictFertilizer: async (data: FertilizerPredictionCreate): Promise<FertilizerRecommendation> => {
    const response = await apiClient.post('/fertilizer-recommendation/predictions/', data);
    return response as unknown as FertilizerRecommendation;
  },

  getPredictionHistory: async (): Promise<FertilizerRecommendation[]> => {
    const response = await apiClient.get('/fertilizer-recommendation/predictions/');
    return response as unknown as FertilizerRecommendation[];
  }
};
