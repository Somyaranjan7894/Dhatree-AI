import React, { useState, useEffect, useRef } from 'react';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Loader } from '../components/common/Loader';
import { diseaseDetectionService } from '../api/disease_detection.service';
import { diseaseDiagnosisService } from '../api/disease_diagnosis.service';
import { DiseasePrediction } from '../types/disease_detection.types';
import { DiseaseKnowledge } from '../types/disease_diagnosis.types';
import { Activity, ShieldAlert, HeartPulse } from "lucide-react";

export const DiseaseDetection: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [prediction, setPrediction] = useState<DiseasePrediction | null>(null);
  const [knowledge, setKnowledge] = useState<DiseaseKnowledge | null>(null);
  const [history, setHistory] = useState<DiseasePrediction[]>([]);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const data = await diseaseDetectionService.getPredictionHistory();
      const historyData = Array.isArray(data) ? data : (data as any).data || (data as any).results || [];
      setHistory(historyData);
    } catch (err) {
      console.error('Failed to fetch history', err);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setPrediction(null);
      setKnowledge(null);
      setError(null);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setPrediction(null);
      setKnowledge(null);
      setError(null);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;
    
    setIsLoading(true);
    setError(null);
    setKnowledge(null);
    try {
      const result = await diseaseDetectionService.predictDisease({ image: selectedFile });
      setPrediction(result);
      fetchHistory(); // Refresh history
      
      try {
        if (!result.predicted_class.toLowerCase().includes('healthy')) {
          const kb = await diseaseDiagnosisService.getDiseaseKnowledge(result.predicted_class);
          setKnowledge(kb);
        }
      } catch (kbErr) {
        console.warn("Disease not found in knowledge base or API error", kbErr);
      }
      
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze image. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const formatDiseaseName = (name: string) => {
    return name.replace(/___/g, ' - ').replace(/_/g, ' ');
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-slate-800 flex items-center gap-2">
          <Activity className="h-6 w-6 text-emerald-600" />
          Plant Disease Detection & Diagnosis
        </h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <div className="p-6">
            <h2 className="text-lg font-semibold text-slate-800 mb-4">Upload Crop Image</h2>
            
            <div 
              className="border-2 border-dashed border-slate-300 rounded-xl p-8 text-center hover:border-emerald-500 transition-colors cursor-pointer bg-slate-50"
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onClick={() => fileInputRef.current?.click()}
            >
              <input 
                type="file" 
                className="hidden" 
                ref={fileInputRef} 
                onChange={handleFileChange}
                accept="image/*"
              />
              
              {previewUrl ? (
                <div className="space-y-4">
                  <img src={previewUrl} alt="Crop preview" className="max-h-64 mx-auto rounded-lg shadow-sm" />
                  <p className="text-sm text-slate-500">Click or drag to change image</p>
                </div>
              ) : (
                <div className="space-y-2 py-8">
                  <div className="mx-auto h-12 w-12 text-slate-400 bg-slate-100 rounded-full flex items-center justify-center mb-4">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <p className="text-slate-700 font-medium">Click to upload or drag and drop</p>
                  <p className="text-slate-500 text-sm">PNG, JPG up to 5MB</p>
                </div>
              )}
            </div>

            {error && (
              <div className="mt-4 p-3 bg-red-50 text-red-700 rounded-lg text-sm">
                {error}
              </div>
            )}

            <div className="mt-6 flex justify-end">
              <Button 
                onClick={handleAnalyze} 
                disabled={!selectedFile || isLoading}
                isLoading={isLoading}
              >
                Analyze Image
              </Button>
            </div>
          </div>
        </Card>

        <Card>
          <div className="p-6 h-full flex flex-col">
            <h2 className="text-lg font-semibold text-slate-800 mb-4">Analysis Results</h2>
            
            {!prediction && !isLoading && (
              <div className="flex-1 flex flex-col items-center justify-center text-slate-400 space-y-4 py-12">
                <svg className="w-16 h-16 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p>Upload an image to see analysis results</p>
              </div>
            )}

            {isLoading && (
              <div className="flex-1 flex flex-col items-center justify-center py-12 space-y-4">
                <Loader />
                <p className="text-slate-500 animate-pulse">Our AI is analyzing your crop...</p>
              </div>
            )}

            {prediction && !isLoading && (
              <div className="space-y-6 flex-1">
                <div className={`p-5 rounded-xl border ${prediction.predicted_class.toLowerCase().includes('healthy') ? 'bg-emerald-50 border-emerald-200' : 'bg-amber-50 border-amber-200'}`}>
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-sm font-medium text-slate-500">Detected Condition</h3>
                    <span className="px-3 py-1 rounded-full text-xs font-semibold bg-white shadow-sm border border-slate-100">
                      {(prediction.confidence_score * 100).toFixed(1)}% Confidence
                    </span>
                  </div>
                  <p className="text-2xl font-bold text-slate-800">{formatDiseaseName(prediction.predicted_class)}</p>
                </div>
                
                {prediction.metadata?.heatmap_base64 && (
                  <div>
                    <h3 className="text-sm font-semibold text-slate-700 mb-2 uppercase tracking-wider">AI Focus Area (Grad-CAM)</h3>
                    <div className="bg-slate-50 p-2 rounded-lg border border-slate-200 text-center">
                      <span className="text-xs text-slate-400 italic block py-2">{prediction.metadata.heatmap_base64 === "mock_base64_heatmap_string" ? "(Heatmap visualization mock loaded)" : "Heatmap loaded"}</span>
                    </div>
                  </div>
                )}

                {Array.isArray(prediction.metadata?.top_predictions) && prediction.metadata.top_predictions.length > 1 && (
                  <div>
                    <h3 className="text-sm font-semibold text-slate-700 mb-2 uppercase tracking-wider">Top Alternatives</h3>
                    <ul className="space-y-2">
                      {prediction.metadata.top_predictions.slice(1).map((alt, idx) => (
                        <li key={idx} className="flex justify-between items-center text-sm bg-slate-50 p-2 rounded border border-slate-100">
                          <span className="text-slate-700">{formatDiseaseName(alt.class)}</span>
                          <span className="text-slate-500">{(alt.confidence * 100).toFixed(1)}%</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                <div>
                  <h3 className="text-sm font-semibold text-slate-700 mb-2 uppercase tracking-wider">Diagnosis & Treatment</h3>
                  {knowledge ? (
                    <div className="space-y-4">
                      <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">
                        <p className="text-sm text-slate-700 leading-relaxed mb-3">{knowledge.description}</p>
                        
                        <h4 className="text-xs font-semibold text-slate-700 uppercase tracking-wider flex items-center gap-1 mb-1 mt-4">
                          <ShieldAlert className="w-3 h-3 text-amber-500" /> Symptoms
                        </h4>
                        <p className="text-sm text-slate-600 mb-4">{knowledge.symptoms}</p>
                        
                        <h4 className="text-xs font-semibold text-slate-700 uppercase tracking-wider flex items-center gap-1 mb-2 mt-4">
                          <HeartPulse className="w-3 h-3 text-rose-500" /> Treatments
                        </h4>
                        {knowledge.treatments.length > 0 ? (
                          <div className="space-y-2">
                            {knowledge.treatments.map(t => (
                              <div key={t.id} className="text-sm bg-white p-2 rounded border border-slate-200">
                                <span className={`text-xs font-semibold px-2 py-0.5 rounded mr-2 ${t.type === 'Organic' ? 'bg-emerald-100 text-emerald-800' : 'bg-purple-100 text-purple-800'}`}>{t.type}</span>
                                <span className="text-slate-700">{t.method}</span>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <p className="text-sm text-slate-500 italic">No specific treatments recorded.</p>
                        )}
                        
                      </div>
                    </div>
                  ) : (
                    <div className="bg-slate-50 p-4 rounded-lg border border-slate-200 text-slate-700 leading-relaxed">
                      {prediction.predicted_class.toLowerCase().includes('healthy') 
                        ? "No treatment necessary. The crop is healthy." 
                        : "Detailed treatment plan is currently unavailable in the Knowledge Base. Please consult a local agricultural expert."}
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </Card>
      </div>

      <Card>
        <div className="p-6">
          <h2 className="text-lg font-semibold text-slate-800 mb-4">Prediction History</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-slate-500 uppercase bg-slate-50 border-y border-slate-200">
                <tr>
                  <th className="px-6 py-3 font-semibold">Date</th>
                  <th className="px-6 py-3 font-semibold">Condition</th>
                  <th className="px-6 py-3 font-semibold">Confidence</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {history.length === 0 ? (
                  <tr>
                    <td colSpan={3} className="px-6 py-8 text-center text-slate-500">
                      No prediction history available.
                    </td>
                  </tr>
                ) : (
                  history.map((item) => (
                    <tr key={item.id} className="hover:bg-slate-50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap text-slate-600">
                        {new Date(item.created_at).toLocaleDateString()} {new Date(item.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap font-medium text-slate-800">
                        {formatDiseaseName(item.predicted_class)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <div className="w-16 bg-slate-200 rounded-full h-2 mr-2">
                            <div className="bg-emerald-500 h-2 rounded-full" style={{ width: `${item.confidence_score * 100}%` }}></div>
                          </div>
                          <span className="text-slate-600">{(item.confidence_score * 100).toFixed(0)}%</span>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </Card>
    </div>
  );
};
