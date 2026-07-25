export interface FertilizerPredictionMetadata {
  alternatives?: { fertilizer: string; confidence: number }[];
  model_version?: string;
}

export interface FertilizerRecommendation {
  id: string;
  user: number;
  farm: string | null;
  crop_type: string;
  nitrogen: number;
  phosphorus: number;
  potassium: number;
  ph_level: number;
  temperature: number;
  humidity: number;
  rainfall: number;
  soil_type: string | null;
  recommended_fertilizer: string;
  confidence_score: number;
  explanation: string | null;
  application_guidance: string | null;
  warnings: string | null;
  metadata?: FertilizerPredictionMetadata;
  is_correct: boolean | null;
  created_at: string;
}

export interface FertilizerPredictionCreate {
  farm?: string;
  crop_type: string;
  nitrogen: number;
  phosphorus: number;
  potassium: number;
  ph_level: number;
  temperature: number;
  humidity: number;
  rainfall: number;
  soil_type?: string;
  confidence_threshold?: number;
}
