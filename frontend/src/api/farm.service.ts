import { apiClient } from "./client";
import { ENDPOINTS } from "./endpoints";
import { Farm, FarmCrop, SoilSample, WeatherSnapshot } from "../types";

export const farmService = {
  getFarms: async () => {
    const response = await apiClient.get<any>(ENDPOINTS.FARMS.LIST);
    const res = response as any;
    return res.data?.results || res.data || [];
  },

  getFarm: async (id: string) => {
    const response = await apiClient.get<any>(ENDPOINTS.FARMS.DETAIL(id));
    const res = response as any;
    return res.data;
  },

  createFarm: async (data: Partial<Farm>) => {
    const response = await apiClient.post<any>(ENDPOINTS.FARMS.LIST, data);
    const res = response as any;
    return res.data;
  },

  getSoilSamples: async (farmId: string) => {
    const response = await apiClient.get<any>(ENDPOINTS.FARMS.SOIL_SAMPLES(farmId));
    const res = response as any;
    return res.data?.results || res.data || [];
  },

  addSoilSample: async (farmId: string, data: Partial<SoilSample>) => {
    const response = await apiClient.post<any>(ENDPOINTS.FARMS.SOIL_SAMPLES(farmId), data);
    const res = response as any;
    return res.data;
  },

  getWeatherSnapshots: async (farmId: string) => {
    const response = await apiClient.get<any>(ENDPOINTS.FARMS.WEATHER_SNAPSHOTS(farmId));
    const res = response as any;
    return res.data?.results || res.data || [];
  },

  addWeatherSnapshot: async (farmId: string, data: Partial<WeatherSnapshot>) => {
    const response = await apiClient.post<any>(ENDPOINTS.FARMS.WEATHER_SNAPSHOTS(farmId), data);
    const res = response as any;
    return res.data;
  },

  getFarmCrops: async (farmId: string) => {
    const response = await apiClient.get<any>(ENDPOINTS.FARMS.CROPS(farmId));
    const res = response as any;
    return res.data?.results || res.data || [];
  },
  
  addFarmCrop: async (farmId: string, data: Partial<FarmCrop>) => {
    const response = await apiClient.post<any>(ENDPOINTS.FARMS.CROPS(farmId), data);
    const res = response as any;
    return res.data;
  }
};
