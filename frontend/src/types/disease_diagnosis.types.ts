export interface Treatment {
  id: string;
  type: string;
  method: string;
  application_frequency: string | null;
  safety_precautions: string | null;
}

export interface Prevention {
  id: string;
  measure: string;
  timing: string | null;
}

export interface Reference {
  id: string;
  source_name: string;
  url: string | null;
}

export interface DiseaseKnowledge {
  id: string;
  name: string;
  crop: string;
  description: string;
  symptoms: string;
  possible_causes: string | null;
  severity: string;
  version: string;
  metadata: Record<string, any>;
  treatments: Treatment[];
  preventions: Prevention[];
  references: Reference[];
  created_at: string;
  updated_at: string;
}
