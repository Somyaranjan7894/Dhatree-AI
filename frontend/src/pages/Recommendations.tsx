import React, { useState, useEffect } from 'react';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Spinner } from '../components/feedback/Spinner';
import { Loader } from '../components/common/Loader';
import { cropRecommendationService } from '../api/crop_recommendation.service';
import { fertilizerService } from '../api/fertilizer.service';
import { CropRecommendation as CropRecommendationType, CropRecommendationCreate } from '../types/crop_recommendation.types';
import { FertilizerPredictionCreate, FertilizerRecommendation as FertilizerRecommendationType } from '../types/fertilizer.types';
import { Lightbulb, Sprout, Beaker, Thermometer, Droplets, Leaf } from "lucide-react";

type Tab = 'crop' | 'fertilizer';

export const Recommendations: React.FC = () => {
  const [activeTab, setActiveTab] = useState<Tab>('crop');

  // Crop State
  const [cropFormData, setCropFormData] = useState<CropRecommendationCreate>({
    nitrogen: 0,
    phosphorus: 0,
    potassium: 0,
    ph: 6.5,
    temperature: 25,
    humidity: 60,
    rainfall: 150
  });
  const [isCropLoading, setIsCropLoading] = useState(false);
  const [cropPrediction, setCropPrediction] = useState<CropRecommendationType | null>(null);
  const [cropError, setCropError] = useState<string | null>(null);

  // Fertilizer State
  const [fertFormData, setFertFormData] = useState<FertilizerPredictionCreate>({
    crop_type: '',
    nitrogen: 0,
    phosphorus: 0,
    potassium: 0,
    ph_level: 6.5,
    temperature: 25,
    humidity: 50,
    rainfall: 100,
    soil_type: 'Loamy'
  });
  const [isFertLoading, setIsFertLoading] = useState(false);
  const [fertPrediction, setFertPrediction] = useState<FertilizerRecommendationType | null>(null);
  const [fertError, setFertError] = useState<string | null>(null);

  // Combined History
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const cropData = await cropRecommendationService.getPredictionHistory();
      const fertDataRaw = await fertilizerService.getPredictionHistory();
      const fertData = Array.isArray(fertDataRaw) ? fertDataRaw : (fertDataRaw as any).data || (fertDataRaw as any).results || [];
      
      const merged = [
        ...cropData.map((item: any) => ({ ...item, _type: 'Crop' })),
        ...fertData.map((item: any) => ({ ...item, _type: 'Fertilizer' }))
      ];
      
      merged.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
      setHistory(merged);
    } catch (err) {
      console.error('Failed to fetch recommendation history', err);
    }
  };

  const handleCropInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCropFormData(prev => ({
      ...prev,
      [name]: parseFloat(value) || 0
    }));
  };

  const handleFertInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    setFertFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? Number(value) : value
    }));
  };

  const handleCropSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsCropLoading(true);
    setCropError(null);
    try {
      const result = await cropRecommendationService.predictCrop(cropFormData);
      setCropPrediction(result);
      fetchHistory(); // Refresh history
    } catch (err: any) {
      setCropError(err.response?.data?.detail || 'Failed to get recommendation. Please check your inputs.');
    } finally {
      setIsCropLoading(false);
    }
  };

  const handleFertSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsFertLoading(true);
    setFertError(null);
    setFertPrediction(null);
    
    try {
      const result = await fertilizerService.predictFertilizer(fertFormData);
      setFertPrediction(result);
      fetchHistory();
    } catch (err: any) {
      setFertError(err.response?.data?.detail || 'Failed to generate recommendation. Please check your inputs.');
    } finally {
      setIsFertLoading(false);
    }
  };

  const formatCropName = (name: string) => {
    if (!name) return "";
    return name.charAt(0).toUpperCase() + name.slice(1);
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-slate-800 flex items-center gap-2">
          <Lightbulb className="h-6 w-6 text-emerald-600" />
          AI Recommendations
        </h1>
      </div>

      <div className="bg-white p-1 rounded-lg border border-slate-200 inline-flex shadow-sm">
        <button
          onClick={() => setActiveTab('crop')}
          className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
            activeTab === 'crop' 
              ? 'bg-emerald-50 text-emerald-700 shadow-sm border border-emerald-100' 
              : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50'
          }`}
        >
          <Sprout className="w-4 h-4" />
          Crop Recommendation
        </button>
        <button
          onClick={() => setActiveTab('fertilizer')}
          className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
            activeTab === 'fertilizer' 
              ? 'bg-emerald-50 text-emerald-700 shadow-sm border border-emerald-100' 
              : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50'
          }`}
        >
          <Beaker className="w-4 h-4" />
          Fertilizer Recommendation
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <div className="p-6 h-full flex flex-col">
            <h2 className="text-lg font-semibold text-slate-800 mb-6">
              {activeTab === 'crop' ? 'Soil & Weather Inputs' : 'Soil & Environment Data'}
            </h2>
            
            {activeTab === 'crop' && (
              <form onSubmit={handleCropSubmit} className="space-y-4">
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Nitrogen (N)</label>
                    <input type="number" name="nitrogen" value={cropFormData.nitrogen} onChange={handleCropInputChange} min="0" max="300" step="0.1" className="w-full rounded-lg border-slate-300 border p-2 focus:border-emerald-500 focus:ring-emerald-500" required />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Phosphorus (P)</label>
                    <input type="number" name="phosphorus" value={cropFormData.phosphorus} onChange={handleCropInputChange} min="0" max="300" step="0.1" className="w-full rounded-lg border-slate-300 border p-2 focus:border-emerald-500 focus:ring-emerald-500" required />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Potassium (K)</label>
                    <input type="number" name="potassium" value={cropFormData.potassium} onChange={handleCropInputChange} min="0" max="300" step="0.1" className="w-full rounded-lg border-slate-300 border p-2 focus:border-emerald-500 focus:ring-emerald-500" required />
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Soil pH</label>
                    <input type="number" name="ph" value={cropFormData.ph} onChange={handleCropInputChange} min="0" max="14" step="0.1" className="w-full rounded-lg border-slate-300 border p-2 focus:border-emerald-500 focus:ring-emerald-500" required />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Temperature (°C)</label>
                    <input type="number" name="temperature" value={cropFormData.temperature} onChange={handleCropInputChange} min="-20" max="60" step="0.1" className="w-full rounded-lg border-slate-300 border p-2 focus:border-emerald-500 focus:ring-emerald-500" required />
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Humidity (%)</label>
                    <input type="number" name="humidity" value={cropFormData.humidity} onChange={handleCropInputChange} min="0" max="100" step="0.1" className="w-full rounded-lg border-slate-300 border p-2 focus:border-emerald-500 focus:ring-emerald-500" required />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Rainfall (mm)</label>
                    <input type="number" name="rainfall" value={cropFormData.rainfall} onChange={handleCropInputChange} min="0" max="1000" step="0.1" className="w-full rounded-lg border-slate-300 border p-2 focus:border-emerald-500 focus:ring-emerald-500" required />
                  </div>
                </div>

                {cropError && (
                  <div className="mt-4 p-3 bg-red-50 text-red-700 rounded-lg text-sm">
                    {cropError}
                  </div>
                )}

                <div className="mt-6 pt-4 border-t border-slate-100 flex justify-end">
                  <Button type="submit" disabled={isCropLoading} isLoading={isCropLoading}>
                    Get Recommendation
                  </Button>
                </div>
              </form>
            )}

            {activeTab === 'fertilizer' && (
              <form onSubmit={handleFertSubmit} className="flex flex-col flex-1">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-5 flex-1">
                  <div className="space-y-1">
                    <label className="text-sm font-medium text-slate-700">Crop Type</label>
                    <input 
                      type="text" 
                      name="crop_type" 
                      required 
                      value={fertFormData.crop_type} 
                      onChange={handleFertInputChange} 
                      className="w-full rounded-md border border-slate-300 p-2 shadow-sm focus:border-emerald-500 focus:ring-emerald-500" 
                      placeholder="e.g. Rice, Wheat"
                    />
                  </div>

                  <div className="space-y-1">
                    <label className="text-sm font-medium text-slate-700">Soil Type</label>
                    <select 
                      name="soil_type" 
                      value={fertFormData.soil_type} 
                      onChange={handleFertInputChange} 
                      className="w-full rounded-md border border-slate-300 p-2 shadow-sm focus:border-emerald-500 focus:ring-emerald-500"
                    >
                      <option value="Loamy">Loamy</option>
                      <option value="Sandy">Sandy</option>
                      <option value="Clayey">Clayey</option>
                      <option value="Black">Black</option>
                      <option value="Red">Red</option>
                    </select>
                  </div>

                  <div className="space-y-1">
                    <label className="text-sm font-medium text-slate-700 flex items-center gap-1"><Leaf className="w-4 h-4 text-emerald-500"/> Nitrogen (N)</label>
                    <input type="number" name="nitrogen" required min="0" max="500" value={fertFormData.nitrogen} onChange={handleFertInputChange} className="w-full border p-2 rounded-md border-slate-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500" />
                  </div>
                  <div className="space-y-1">
                    <label className="text-sm font-medium text-slate-700 flex items-center gap-1"><Leaf className="w-4 h-4 text-amber-500"/> Phosphorus (P)</label>
                    <input type="number" name="phosphorus" required min="0" max="500" value={fertFormData.phosphorus} onChange={handleFertInputChange} className="w-full border p-2 rounded-md border-slate-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500" />
                  </div>
                  <div className="space-y-1">
                    <label className="text-sm font-medium text-slate-700 flex items-center gap-1"><Leaf className="w-4 h-4 text-rose-500"/> Potassium (K)</label>
                    <input type="number" name="potassium" required min="0" max="500" value={fertFormData.potassium} onChange={handleFertInputChange} className="w-full border p-2 rounded-md border-slate-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500" />
                  </div>
                  <div className="space-y-1">
                    <label className="text-sm font-medium text-slate-700 flex items-center gap-1"><Droplets className="w-4 h-4 text-blue-500"/> Soil pH</label>
                    <input type="number" name="ph_level" required min="0" max="14" step="0.1" value={fertFormData.ph_level} onChange={handleFertInputChange} className="w-full border p-2 rounded-md border-slate-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500" />
                  </div>

                  <div className="space-y-1">
                    <label className="text-sm font-medium text-slate-700 flex items-center gap-1"><Thermometer className="w-4 h-4 text-orange-500"/> Temperature (°C)</label>
                    <input type="number" name="temperature" required min="-50" max="60" value={fertFormData.temperature} onChange={handleFertInputChange} className="w-full border p-2 rounded-md border-slate-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500" />
                  </div>
                  <div className="space-y-1">
                    <label className="text-sm font-medium text-slate-700 flex items-center gap-1"><Droplets className="w-4 h-4 text-cyan-500"/> Humidity (%)</label>
                    <input type="number" name="humidity" required min="0" max="100" value={fertFormData.humidity} onChange={handleFertInputChange} className="w-full border p-2 rounded-md border-slate-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500" />
                  </div>
                </div>

                {fertError && (
                  <div className="mt-4 p-3 bg-red-50 text-red-700 rounded-lg text-sm">
                    {fertError}
                  </div>
                )}

                <div className="mt-8 flex justify-end">
                  <Button type="submit" disabled={isFertLoading} isLoading={isFertLoading}>
                    Generate Recommendation
                  </Button>
                </div>
              </form>
            )}
          </div>
        </Card>

        <Card>
          <div className="p-6 h-full flex flex-col">
            <h2 className="text-lg font-semibold text-slate-800 mb-4">Recommendation Analysis</h2>
            
            {activeTab === 'crop' && (
              <>
                {!cropPrediction && !isCropLoading && (
                  <div className="flex-1 flex flex-col items-center justify-center text-slate-400 space-y-4 py-12">
                    <Sprout className="w-16 h-16 opacity-50" />
                    <p>Enter parameters to get AI crop recommendations.</p>
                  </div>
                )}

                {isCropLoading && (
                  <div className="flex-1 flex flex-col items-center justify-center py-12 space-y-4">
                    <Spinner />
                    <p className="text-slate-500 animate-pulse">Running Random Forest Model...</p>
                  </div>
                )}

                {cropPrediction && !isCropLoading && (
                  <div className="space-y-6 flex-1">
                    <div className="p-5 rounded-xl border bg-emerald-50 border-emerald-200">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="text-sm font-medium text-slate-500">Best Match</h3>
                        <span className="px-3 py-1 rounded-full text-xs font-semibold bg-white shadow-sm border border-slate-100">
                          {(cropPrediction.confidence_score * 100).toFixed(1)}% Confidence
                        </span>
                      </div>
                      <p className="text-3xl font-bold text-slate-800">{formatCropName(cropPrediction.recommended_crop)}</p>
                    </div>

                    <div>
                      <h3 className="text-sm font-semibold text-slate-700 mb-2 uppercase tracking-wider">Analysis</h3>
                      <div className="bg-slate-50 p-4 rounded-lg border border-slate-200 text-slate-700 leading-relaxed text-sm">
                        {cropPrediction.explanation}
                      </div>
                    </div>

                    {cropPrediction.alternatives && cropPrediction.alternatives.length > 0 && (
                      <div>
                        <h3 className="text-sm font-semibold text-slate-700 mb-2 uppercase tracking-wider">Alternatives</h3>
                        <div className="space-y-2">
                          {cropPrediction.alternatives.map((alt, idx) => (
                            <div key={idx} className="flex justify-between items-center bg-white border border-slate-100 p-3 rounded-lg shadow-sm">
                              <span className="font-medium text-slate-700">{formatCropName(alt.crop)}</span>
                              <span className="text-xs font-semibold text-slate-500">{(alt.confidence * 100).toFixed(1)}% match</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </>
            )}

            {activeTab === 'fertilizer' && (
              <>
                {!fertPrediction && !isFertLoading && (
                  <div className="flex-1 flex flex-col items-center justify-center text-slate-400 space-y-4 py-12">
                    <Beaker className="w-16 h-16 opacity-50" />
                    <p>Fill out the form to get a personalized fertilizer plan.</p>
                  </div>
                )}

                {isFertLoading && (
                  <div className="flex-1 flex flex-col items-center justify-center py-12 space-y-4">
                    <Loader />
                    <p className="text-slate-500 animate-pulse">Analyzing soil nutrient profiles...</p>
                  </div>
                )}

                {fertPrediction && !isFertLoading && (
                  <div className="space-y-6 flex-1">
                    <div className={`p-5 rounded-xl border ${fertPrediction.confidence_score > 0.6 ? 'bg-emerald-50 border-emerald-200' : 'bg-amber-50 border-amber-200'}`}>
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="text-sm font-medium text-slate-500">Primary Recommendation</h3>
                        <span className="px-3 py-1 rounded-full text-xs font-semibold bg-white shadow-sm border border-slate-100">
                          {(fertPrediction.confidence_score * 100).toFixed(1)}% Match
                        </span>
                      </div>
                      <p className="text-2xl font-bold text-slate-800">{fertPrediction.recommended_fertilizer}</p>
                    </div>

                    {fertPrediction.explanation && (
                      <div>
                        <h3 className="text-sm font-semibold text-slate-700 mb-2 uppercase tracking-wider">Agronomist Explanation</h3>
                        <div className="bg-slate-50 p-4 rounded-lg border border-slate-200 text-slate-700 leading-relaxed text-sm">
                          {fertPrediction.explanation}
                        </div>
                      </div>
                    )}

                    {fertPrediction.application_guidance && (
                      <div>
                        <h3 className="text-sm font-semibold text-slate-700 mb-2 uppercase tracking-wider">Application Guidance</h3>
                        <div className="bg-slate-50 p-4 rounded-lg border border-slate-200 text-slate-700 leading-relaxed text-sm">
                          {fertPrediction.application_guidance}
                        </div>
                      </div>
                    )}
                    
                    {fertPrediction.warnings && (
                      <div className="p-3 bg-red-50 border border-red-100 rounded-lg text-sm text-red-800">
                        <strong>Warning:</strong> {fertPrediction.warnings}
                      </div>
                    )}

                    {fertPrediction.metadata?.alternatives && fertPrediction.metadata.alternatives.length > 0 && (
                      <div>
                        <h3 className="text-sm font-semibold text-slate-700 mb-2 uppercase tracking-wider">Alternatives</h3>
                        <div className="space-y-2">
                          {fertPrediction.metadata.alternatives.map((alt, idx) => (
                            <div key={idx} className="flex justify-between items-center bg-slate-50 p-2 rounded text-sm border border-slate-100">
                              <span className="font-medium text-slate-700">{alt.fertilizer}</span>
                              <span className="text-slate-500">{(alt.confidence * 100).toFixed(1)}%</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </>
            )}
          </div>
        </Card>
      </div>

      <Card>
        <div className="p-6">
          <h2 className="text-lg font-semibold text-slate-800 mb-4">Recommendation History</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-slate-500 uppercase bg-slate-50 border-y border-slate-200">
                <tr>
                  <th className="px-6 py-3 font-semibold">Date</th>
                  <th className="px-6 py-3 font-semibold">Type</th>
                  <th className="px-6 py-3 font-semibold">Parameters</th>
                  <th className="px-6 py-3 font-semibold">Recommendation</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {history.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="px-6 py-8 text-center text-slate-500">
                      No recommendation history found.
                    </td>
                  </tr>
                ) : (
                  history.map((item) => (
                    <tr key={item.id} className="hover:bg-slate-50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap text-slate-600">
                        {new Date(item.created_at).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${item._type === 'Crop' ? 'bg-emerald-100 text-emerald-800' : 'bg-blue-100 text-blue-800'}`}>
                          {item._type}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-slate-600">
                        {item._type === 'Crop' ? (
                          <div>
                            <div className="font-medium text-slate-800">N-P-K: {item.nitrogen}-{item.phosphorus}-{item.potassium} | pH: {item.ph}</div>
                            <div className="text-xs text-slate-500">{item.temperature}°C / {item.humidity}% / {item.rainfall}mm</div>
                          </div>
                        ) : (
                          <div>
                            <div className="font-medium text-slate-800">{item.crop_type} - {item.soil_type} Soil</div>
                            <div className="text-xs text-slate-500">N-P-K: {item.nitrogen}-{item.phosphorus}-{item.potassium}</div>
                          </div>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {item._type === 'Crop' ? (
                          <>
                            <div className="font-medium text-slate-800">{formatCropName(item.recommended_crop)}</div>
                            <div className="text-xs text-slate-500">{(item.confidence_score * 100).toFixed(0)}% Confidence</div>
                          </>
                        ) : (
                          <>
                            <div className="font-medium text-emerald-700">{item.recommended_fertilizer}</div>
                            <div className="text-xs text-slate-500">{(item.confidence_score * 100).toFixed(0)}% Match</div>
                          </>
                        )}
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
