import { apiClient } from './client';
import { DiseasePrediction, DiseasePredictionCreate } from '../types/disease_detection.types';

export const diseaseDetectionService = {
  predictDisease: async (data: DiseasePredictionCreate): Promise<DiseasePrediction> => {
    const formData = new FormData();
    formData.append('image', data.image);
    if (data.farm) {
      formData.append('farm', data.farm);
    }
    
    const response = await apiClient.post<DiseasePrediction>('/disease-detection/predictions/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }) as any;
    return response.data;
  },

  getPredictionHistory: async (): Promise<DiseasePrediction[]> => {
    const response = await apiClient.get<DiseasePrediction[]>('/disease-detection/predictions/') as any;
    return response.data;
  },
};
