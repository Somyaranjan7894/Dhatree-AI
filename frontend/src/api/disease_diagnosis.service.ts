import { apiClient } from './client';
import { DiseaseKnowledge } from '../types/disease_diagnosis.types';

export const diseaseDiagnosisService = {
  getDiseaseKnowledge: async (diseaseIdOrName: string): Promise<DiseaseKnowledge> => {
    const response = await apiClient.get(`/disease_diagnosis/knowledge/${diseaseIdOrName}/`);
    return response as unknown as DiseaseKnowledge;
  },

  searchDiseases: async (query?: string, crop?: string, severity?: string): Promise<DiseaseKnowledge[]> => {
    let url = '/disease_diagnosis/knowledge/';
    const params = new URLSearchParams();
    
    if (query) params.append('search', query);
    if (crop) params.append('crop', crop);
    if (severity) params.append('severity', severity);
    
    if (params.toString()) {
      url += `?${params.toString()}`;
    }
    
    const response = await apiClient.get(url);
    // apiClient unwraps response.data, so if it's paginated it might be in .results
    const anyRes = response as any;
    return anyRes.results || anyRes;
  }
};
