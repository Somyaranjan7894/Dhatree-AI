export interface CropRecommendationAlternative {
  crop: string;
  confidence: number;
  explanation: string;
}

export interface CropRecommendation {
  id: string;
  user: number;
  farm: string | null;
  nitrogen: number;
  phosphorus: number;
  potassium: number;
  ph: number;
  temperature: number;
  humidity: number;
  rainfall: number;
  recommended_crop: string;
  confidence_score: number;
  alternatives: CropRecommendationAlternative[];
  explanation: string;
  model_version: string;
  created_at: string;
}

export interface CropRecommendationCreate {
  farm?: string;
  nitrogen: number;
  phosphorus: number;
  potassium: number;
  ph: number;
  temperature: number;
  humidity: number;
  rainfall: number;
}
