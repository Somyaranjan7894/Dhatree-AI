import React, { useState, useEffect } from 'react';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Loader } from '../components/common/Loader';
import { diseaseDiagnosisService } from '../api/disease_diagnosis.service';
import { DiseaseKnowledge } from '../types/disease_diagnosis.types';
import { BookOpen, Search, Leaf, ShieldAlert, HeartPulse, ExternalLink } from "lucide-react";

export const DiseaseDiagnosis: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [cropFilter, setCropFilter] = useState('');
  const [severityFilter, setSeverityFilter] = useState('');
  
  const [isLoading, setIsLoading] = useState(false);
  const [diseases, setDiseases] = useState<DiseaseKnowledge[]>([]);
  const [selectedDisease, setSelectedDisease] = useState<DiseaseKnowledge | null>(null);

  useEffect(() => {
    handleSearch();
  }, [cropFilter, severityFilter]);

  const handleSearch = async () => {
    setIsLoading(true);
    try {
      const results = await diseaseDiagnosisService.searchDiseases(searchQuery, cropFilter, severityFilter);
      setDiseases(results);
      if (results.length === 1) {
        setSelectedDisease(results[0]);
      } else {
        setSelectedDisease(null);
      }
    } catch (err) {
      console.error('Failed to search diseases', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const severityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'low': return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'high': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'critical': return 'bg-red-100 text-red-800 border-red-200';
      default: return 'bg-slate-100 text-slate-800 border-slate-200';
    }
  };

  const formatDiseaseName = (name: string) => {
    return name.replace(/___/g, ' - ').replace(/_/g, ' ');
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-slate-800 flex items-center gap-2">
          <BookOpen className="h-6 w-6 text-emerald-600" />
          Disease Knowledge Base
        </h1>
      </div>

      <Card>
        <div className="p-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="h-5 w-5 text-slate-400" />
              </div>
              <input
                type="text"
                className="pl-10 w-full rounded-md border-slate-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500"
                placeholder="Search diseases, symptoms, or descriptions..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={handleKeyPress}
              />
            </div>
            
            <div className="w-full md:w-48">
              <select
                className="w-full rounded-md border-slate-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500"
                value={cropFilter}
                onChange={(e) => setCropFilter(e.target.value)}
              >
                <option value="">All Crops</option>
                <option value="Apple">Apple</option>
                <option value="Corn">Corn</option>
                <option value="Potato">Potato</option>
                <option value="Rice">Rice</option>
                <option value="Tomato">Tomato</option>
              </select>
            </div>

            <div className="w-full md:w-48">
              <select
                className="w-full rounded-md border-slate-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500"
                value={severityFilter}
                onChange={(e) => setSeverityFilter(e.target.value)}
              >
                <option value="">All Severities</option>
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
                <option value="Critical">Critical</option>
              </select>
            </div>

            <Button onClick={handleSearch} disabled={isLoading}>
              Search
            </Button>
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-4">
          <Card className="h-full max-h-[800px] flex flex-col">
            <div className="p-4 border-b border-slate-100 bg-slate-50">
              <h2 className="font-semibold text-slate-700">Search Results ({diseases.length})</h2>
            </div>
            <div className="overflow-y-auto flex-1 p-2">
              {isLoading ? (
                <div className="flex justify-center p-8"><Loader /></div>
              ) : diseases.length === 0 ? (
                <div className="text-center p-8 text-slate-500 text-sm">
                  No diseases found matching your criteria.
                </div>
              ) : (
                <div className="space-y-2">
                  {diseases.map(disease => (
                    <div 
                      key={disease.id}
                      onClick={() => setSelectedDisease(disease)}
                      className={`p-3 rounded-lg cursor-pointer border transition-colors ${selectedDisease?.id === disease.id ? 'bg-emerald-50 border-emerald-200' : 'bg-white border-slate-200 hover:border-emerald-300 hover:bg-slate-50'}`}
                    >
                      <div className="flex justify-between items-start mb-1">
                        <h3 className="font-medium text-slate-800 text-sm">{formatDiseaseName(disease.name)}</h3>
                        <span className={`text-xs px-2 py-0.5 rounded-full border ${severityColor(disease.severity)}`}>
                          {disease.severity}
                        </span>
                      </div>
                      <div className="text-xs text-slate-500 flex items-center gap-1">
                        <Leaf className="w-3 h-3" /> {disease.crop}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </Card>
        </div>

        <div className="lg:col-span-2">
          {selectedDisease ? (
            <Card className="h-full">
              <div className="p-6 space-y-6">
                <div>
                  <div className="flex justify-between items-start">
                    <div>
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-xs font-semibold uppercase tracking-wider text-emerald-600 bg-emerald-50 px-2 py-1 rounded-full">
                          {selectedDisease.crop}
                        </span>
                        <span className={`text-xs font-semibold uppercase tracking-wider px-2 py-1 rounded-full border ${severityColor(selectedDisease.severity)}`}>
                          {selectedDisease.severity} SEVERITY
                        </span>
                      </div>
                      <h2 className="text-2xl font-bold text-slate-800">{formatDiseaseName(selectedDisease.name)}</h2>
                    </div>
                  </div>
                  <p className="mt-4 text-slate-600 leading-relaxed">{selectedDisease.description}</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div>
                      <h3 className="text-sm font-semibold text-slate-700 flex items-center gap-2 mb-2">
                        <ShieldAlert className="w-4 h-4 text-amber-500" /> Symptoms
                      </h3>
                      <div className="bg-amber-50 p-4 rounded-lg border border-amber-100 text-sm text-amber-900 leading-relaxed">
                        {selectedDisease.symptoms}
                      </div>
                    </div>

                    {selectedDisease.preventions.length > 0 && (
                      <div>
                        <h3 className="text-sm font-semibold text-slate-700 mb-2">Preventive Measures</h3>
                        <ul className="space-y-2">
                          {selectedDisease.preventions.map(prev => (
                            <li key={prev.id} className="text-sm bg-slate-50 p-3 rounded-lg border border-slate-100">
                              <span className="block text-slate-700">{prev.measure}</span>
                              {prev.timing && <span className="block text-xs text-slate-400 mt-1">Timing: {prev.timing}</span>}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>

                  <div className="space-y-4">
                    <div>
                      <h3 className="text-sm font-semibold text-slate-700 flex items-center gap-2 mb-2">
                        <HeartPulse className="w-4 h-4 text-rose-500" /> Treatments
                      </h3>
                      {selectedDisease.treatments.length === 0 ? (
                        <p className="text-sm text-slate-500 italic">No specific treatments recorded.</p>
                      ) : (
                        <div className="space-y-3">
                          {selectedDisease.treatments.map(treat => (
                            <div key={treat.id} className="bg-white border border-slate-200 rounded-lg p-3">
                              <div className="flex justify-between items-center mb-2">
                                <span className={`text-xs font-semibold px-2 py-0.5 rounded ${treat.type === 'Organic' ? 'bg-emerald-100 text-emerald-800' : 'bg-purple-100 text-purple-800'}`}>
                                  {treat.type}
                                </span>
                              </div>
                              <p className="text-sm text-slate-700 mb-2">{treat.method}</p>
                              {treat.application_frequency && (
                                <p className="text-xs text-slate-500"><strong className="text-slate-600">Frequency:</strong> {treat.application_frequency}</p>
                              )}
                              {treat.safety_precautions && (
                                <p className="text-xs text-rose-600 mt-1"><strong className="text-rose-700">Safety:</strong> {treat.safety_precautions}</p>
                              )}
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                    
                    {selectedDisease.references.length > 0 && (
                      <div>
                         <h3 className="text-sm font-semibold text-slate-700 mb-2">References</h3>
                         <ul className="space-y-2">
                           {selectedDisease.references.map(ref => (
                             <li key={ref.id} className="text-sm flex items-center gap-2">
                               <ExternalLink className="w-3 h-3 text-slate-400" />
                               {ref.url ? (
                                 <a href={ref.url} target="_blank" rel="noreferrer" className="text-blue-600 hover:underline">{ref.source_name}</a>
                               ) : (
                                 <span className="text-slate-600">{ref.source_name}</span>
                               )}
                             </li>
                           ))}
                         </ul>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </Card>
          ) : (
            <Card className="h-full flex flex-col items-center justify-center p-12 text-slate-400">
              <BookOpen className="w-16 h-16 opacity-30 mb-4" />
              <p>Select a disease from the list to view its complete diagnosis and treatment details.</p>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
