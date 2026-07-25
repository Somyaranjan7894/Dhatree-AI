export interface DiseasePredictionMetadata {
  top_predictions?: { class: string; confidence: number }[];
  heatmap_base64?: string | null;
}

export interface DiseasePrediction {
  id: string;
  user: number;
  farm: string | null;
  image: string;
  predicted_class: string;
  confidence_score: number;
  metadata?: DiseasePredictionMetadata;
  is_correct: boolean | null;
  created_at: string;
}

export interface DiseasePredictionCreate {
  image: File;
  farm?: string;
}
