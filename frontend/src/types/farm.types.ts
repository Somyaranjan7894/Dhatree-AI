export interface Farm {
  id: string;
  farm_name: string;
  area: number;
  latitude: number | null;
  longitude: number | null;
  village: string;
  district: string;
  state: string;
  water_source: string;
  soil_type: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface FarmCrop {
  id: string;
  farm: string;
  crop: string;
  crop_name?: string;
  sowing_date: string;
  expected_harvest_date: string | null;
  actual_harvest_date: string | null;
  yield_quantity: number | null;
  area_allocated: number | null;
  status: string;
  status_display?: string;
}

export interface SoilSample {
  id: string;
  farm: string;
  sample_date: string;
  nitrogen: number | null;
  phosphorus: number | null;
  potassium: number | null;
  organic_carbon: number | null;
  ph_level: number | null;
  moisture: number | null;
  electrical_conductivity: number | null;
  texture: string | null;
  remarks: string | null;
}

export interface WeatherSnapshot {
  id: string;
  farm: string;
  date: string;
  temperature: number | null;
  humidity: number | null;
  rainfall: number | null;
  wind_speed: number | null;
  pressure: number | null;
  cloud_cover: number | null;
}

export interface Notification {
  id: string;
  title: string;
  description: string;
  notification_type: string;
  is_read: boolean;
  created_at: string;
}
