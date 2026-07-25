import React, { useState, useEffect, useRef } from 'react';
import { Search, MapPin, Activity, Sprout, Book, X, Leaf } from 'lucide-react';
import { apiClient } from '../../api/client';


interface SearchResult {
  id: string;
  title: string;
  description: string;
  type: 'farm' | 'knowledge' | 'prediction' | 'crop_rec' | 'fert_rec';
}

interface SearchResponse {
  farms: SearchResult[];
  diseases: SearchResult[];
  predictions: SearchResult[];
  recommendations: SearchResult[];
}

export const GlobalSearch: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const searchRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setIsOpen(true);
      }
      if (e.key === 'Escape') {
        setIsOpen(false);
      }
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    const debounceSearch = setTimeout(async () => {
      if (query.length < 2) {
        setResults(null);
        return;
      }
      setIsLoading(true);
      try {
        const res: any = await apiClient.get(`/dashboard/search/?q=${encodeURIComponent(query)}`);
        setResults(res.data);
      } catch (err) {
        console.error('Search error', err);
      } finally {
        setIsLoading(false);
      }
    }, 300);

    return () => clearTimeout(debounceSearch);
  }, [query]);

  const getIcon = (type: string) => {
    switch (type) {
      case 'farm': return <MapPin className="w-4 h-4 text-orange-500" />;
      case 'knowledge': return <Book className="w-4 h-4 text-blue-500" />;
      case 'prediction': return <Activity className="w-4 h-4 text-rose-500" />;
      case 'crop_rec': return <Leaf className="w-4 h-4 text-emerald-500" />;
      case 'fert_rec': return <Sprout className="w-4 h-4 text-emerald-600" />;
      default: return <Search className="w-4 h-4 text-slate-400" />;
    }
  };

  const hasResults = results && (results.farms.length > 0 || results.diseases.length > 0 || results.predictions.length > 0 || results.recommendations.length > 0);

  return (
    <>
      {/* Trigger Button */}
      <button 
        onClick={() => setIsOpen(true)}
        className="flex items-center gap-2 px-3 py-1.5 md:w-64 bg-slate-100 hover:bg-slate-200 text-slate-500 rounded-full transition-colors text-sm border border-transparent focus:outline-none focus:ring-2 focus:ring-emerald-500"
      >
        <Search className="w-4 h-4" />
        <span className="flex-1 text-left hidden sm:inline-block">Search farms, diseases...</span>
        <span className="hidden md:inline-block text-[10px] bg-slate-200 px-1.5 py-0.5 rounded font-medium text-slate-400 border border-slate-300">Ctrl+K</span>
      </button>

      {/* Modal Overlay */}
      {isOpen && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-[100] flex justify-center items-start pt-[10vh] animate-fade-in">
          <div ref={searchRef} className="w-full max-w-2xl bg-white rounded-xl shadow-2xl overflow-hidden mx-4 transform transition-all">
            
            {/* Search Input Header */}
            <div className="flex items-center px-4 py-3 border-b border-slate-100">
              <Search className="w-5 h-5 text-emerald-600 mr-3" />
              <input 
                autoFocus
                type="text" 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search across your entire platform..."
                className="flex-1 bg-transparent focus:outline-none text-slate-800 text-lg placeholder-slate-400"
              />
              <button onClick={() => setIsOpen(false)} className="text-slate-400 hover:text-slate-600 p-1 rounded-md hover:bg-slate-100">
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Results Area */}
            <div className="max-h-[60vh] overflow-y-auto p-2 bg-slate-50">
              
              {isLoading && (
                <div className="p-8 text-center text-slate-400 animate-pulse text-sm">Searching...</div>
              )}

              {!isLoading && query.length >= 2 && !hasResults && (
                <div className="p-8 text-center text-slate-500 text-sm">
                  No results found for "{query}". Try checking your spelling.
                </div>
              )}

              {!isLoading && query.length < 2 && (
                <div className="p-8 text-center text-slate-400 text-sm">
                  Type at least 2 characters to search.
                </div>
              )}

              {!isLoading && hasResults && (
                <div className="space-y-4 p-2">
                  
                  {results?.farms && results.farms.length > 0 && (
                    <div>
                      <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 px-2">Farms</h4>
                      {results.farms.map(item => (
                        <div key={item.id} className="flex items-start gap-3 p-2 hover:bg-white rounded-lg transition-colors cursor-pointer group">
                          <div className="mt-1 bg-orange-100 p-1.5 rounded-md">{getIcon(item.type)}</div>
                          <div>
                            <p className="font-semibold text-slate-800 text-sm group-hover:text-emerald-700">{item.title}</p>
                            <p className="text-xs text-slate-500 truncate max-w-md">{item.description}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {results?.diseases && results.diseases.length > 0 && (
                    <div>
                      <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 px-2 mt-4">Knowledge Base</h4>
                      {results.diseases.map(item => (
                        <div key={item.id} className="flex items-start gap-3 p-2 hover:bg-white rounded-lg transition-colors cursor-pointer group">
                          <div className="mt-1 bg-blue-100 p-1.5 rounded-md">{getIcon(item.type)}</div>
                          <div>
                            <p className="font-semibold text-slate-800 text-sm group-hover:text-emerald-700 capitalize">{item.title}</p>
                            <p className="text-xs text-slate-500 line-clamp-1 max-w-md">{item.description}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {results?.predictions && results.predictions.length > 0 && (
                    <div>
                      <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 px-2 mt-4">Disease Scans</h4>
                      {results.predictions.map(item => (
                        <div key={item.id} className="flex items-start gap-3 p-2 hover:bg-white rounded-lg transition-colors cursor-pointer group">
                          <div className="mt-1 bg-rose-100 p-1.5 rounded-md">{getIcon(item.type)}</div>
                          <div>
                            <p className="font-semibold text-slate-800 text-sm group-hover:text-emerald-700 capitalize">{item.title}</p>
                            <p className="text-xs text-slate-500">{item.description}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {results?.recommendations && results.recommendations.length > 0 && (
                    <div>
                      <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 px-2 mt-4">Recommendations</h4>
                      {results.recommendations.map(item => (
                        <div key={item.id} className="flex items-start gap-3 p-2 hover:bg-white rounded-lg transition-colors cursor-pointer group">
                          <div className="mt-1 bg-emerald-100 p-1.5 rounded-md">{getIcon(item.type)}</div>
                          <div>
                            <p className="font-semibold text-slate-800 text-sm group-hover:text-emerald-700">{item.title}</p>
                            <p className="text-xs text-slate-500">{item.description}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                  
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
};
