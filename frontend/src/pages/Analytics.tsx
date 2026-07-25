import React, { useEffect, useState } from 'react';
import { analyticsService, AnalyticsResponse } from '../api/analytics.service';
import { Loader } from '../components/common/Loader';
import { TrendingUp, BarChart2, Lightbulb } from 'lucide-react';

export const Analytics: React.FC = () => {
  const [data, setData] = useState<AnalyticsResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await analyticsService.getAnalytics();
        setData(response);
      } catch (error) {
        console.error('Failed to load analytics', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div className="p-8 flex justify-center"><Loader /></div>;
  if (!data) return <div className="p-8 text-center text-slate-500">Failed to load analytics</div>;

  const maxFreq = data.disease_frequency.length > 0 ? Math.max(...data.disease_frequency.map(d => d.count)) : 1;
  const maxScan = data.monthly_scans.length > 0 ? Math.max(...data.monthly_scans.map(m => m.count)) : 1;

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Farm Analytics</h1>
        <p className="text-slate-500">Trends and insights based on your farming activity.</p>
      </div>

      {/* Auto-generated Insights */}
      {data.insights.length > 0 && (
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-5 border border-blue-100 shadow-sm">
          <h2 className="text-sm font-bold text-blue-900 flex items-center gap-2 mb-3">
            <Lightbulb className="w-5 h-5 text-blue-600" /> Auto-Generated Insights
          </h2>
          <ul className="space-y-2">
            {data.insights.map((insight, idx) => (
              <li key={idx} className="flex items-start gap-2 text-sm text-blue-800">
                <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-blue-500 flex-shrink-0" />
                <span className="leading-relaxed">{insight}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Disease Frequency Bar Chart */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
          <h3 className="font-semibold text-slate-800 mb-4 flex items-center gap-2">
            <BarChart2 className="w-5 h-5 text-emerald-600" /> Disease Frequency
          </h3>
          {data.disease_frequency.length === 0 ? (
            <p className="text-slate-500 text-sm text-center py-8">No diseases detected yet.</p>
          ) : (
            <div className="space-y-4">
              {data.disease_frequency.map((item, idx) => (
                <div key={idx}>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="font-medium text-slate-700 capitalize">{item.predicted_class}</span>
                    <span className="text-slate-500">{item.count} scans</span>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                    <div 
                      className="bg-emerald-500 h-2.5 rounded-full transition-all duration-1000 ease-out" 
                      style={{ width: `${(item.count / maxFreq) * 100}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Monthly Scans Trend */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
          <h3 className="font-semibold text-slate-800 mb-6 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-blue-600" /> Scan Activity Trend
          </h3>
          {data.monthly_scans.length === 0 ? (
            <p className="text-slate-500 text-sm text-center py-8">No activity data available.</p>
          ) : (
            <div className="flex items-end gap-2 h-48 pt-4">
              {data.monthly_scans.map((item, idx) => (
                <div key={idx} className="flex-1 flex flex-col justify-end items-center group">
                  <div className="opacity-0 group-hover:opacity-100 transition-opacity text-xs font-semibold text-slate-700 mb-2">
                    {item.count}
                  </div>
                  <div 
                    className="w-full max-w-[40px] bg-blue-100 group-hover:bg-blue-500 rounded-t-md transition-all duration-500 relative overflow-hidden"
                    style={{ height: `${(item.count / maxScan) * 100}%`, minHeight: '4px' }}
                  >
                    <div className="absolute inset-0 bg-blue-500/20 group-hover:bg-blue-600/20" />
                  </div>
                  <div className="text-[10px] text-slate-400 mt-2 rotate-45 origin-left w-full text-center">
                    {item.month.split(' ')[0]}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

      </div>
    </div>
  );
};
