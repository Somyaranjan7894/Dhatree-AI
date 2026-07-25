import React, { useEffect, useState } from 'react';
import { Leaf, Activity, Sprout, AlertTriangle, Info, ShieldAlert, Cpu } from 'lucide-react';
import { dashboardService, DashboardOverviewResponse } from '../api/dashboard.service';
import { Loader } from '../components/common/Loader';
import { Link } from 'react-router-dom';

export const Dashboard: React.FC = () => {
  const [data, setData] = useState<DashboardOverviewResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await dashboardService.getOverview();
        setData(response);
      } catch (error) {
        console.error('Failed to load dashboard', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div className="p-8 flex justify-center"><Loader /></div>;
  if (!data) return <div className="p-8 text-center text-slate-500">Failed to load dashboard</div>;

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
        <p className="text-slate-500">Your daily farming insights and actionable tasks.</p>
      </div>

      {/* Actionable Insights */}
      {data.insights.length > 0 && (
        <div className="space-y-3">
          <h2 className="text-lg font-semibold text-slate-800">Actionable Insights</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {data.insights.map((insight, idx) => (
              <div key={idx} className={`p-4 rounded-xl border flex items-start gap-3 ${
                insight.type === 'warning' ? 'bg-orange-50 border-orange-200 text-orange-800' :
                insight.type === 'critical' ? 'bg-red-50 border-red-200 text-red-800' :
                'bg-blue-50 border-blue-200 text-blue-800'
              }`}>
                <div className="mt-0.5">
                  {insight.type === 'warning' ? <AlertTriangle className="w-5 h-5 text-orange-500" /> :
                   insight.type === 'critical' ? <ShieldAlert className="w-5 h-5 text-red-500" /> :
                   <Info className="w-5 h-5 text-blue-500" />}
                </div>
                <p className="text-sm font-medium leading-relaxed">{insight.message}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* High Level Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-5 flex items-center justify-between hover:shadow-md transition-shadow">
          <div>
            <p className="text-sm text-slate-500 font-medium mb-1">Active Farms</p>
            <p className="text-3xl font-bold text-slate-900">{data.metrics.active_farms}</p>
          </div>
          <div className="bg-emerald-100 p-3 rounded-full text-emerald-600">
            <Leaf className="w-6 h-6" />
          </div>
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-5 flex items-center justify-between hover:shadow-md transition-shadow">
          <div>
            <p className="text-sm text-slate-500 font-medium mb-1">Total Scans</p>
            <p className="text-3xl font-bold text-slate-900">{data.metrics.total_disease_predictions}</p>
          </div>
          <div className="bg-blue-100 p-3 rounded-full text-blue-600">
            <Activity className="w-6 h-6" />
          </div>
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-5 flex items-center justify-between hover:shadow-md transition-shadow">
          <div>
            <p className="text-sm text-slate-500 font-medium mb-1">Unread Alerts</p>
            <p className="text-3xl font-bold text-slate-900">{data.metrics.unread_alerts}</p>
          </div>
          <div className="bg-orange-100 p-3 rounded-full text-orange-600">
            <ShieldAlert className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Recent Disease Diagnoses */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
          <div className="p-4 border-b border-slate-100 flex justify-between items-center bg-slate-50">
            <h3 className="font-semibold text-slate-800 flex items-center gap-2">
              <Activity className="w-4 h-4 text-rose-500" /> Recent Disease Diagnoses
            </h3>
            <Link to="/disease-detection" className="text-sm text-emerald-600 hover:text-emerald-700 font-medium bg-white px-3 py-1 rounded-md border border-slate-200 shadow-sm">Scan New</Link>
          </div>
          <div className="p-4">
            {data.recent_activity.diseases.length === 0 ? (
              <p className="text-sm text-slate-500 text-center py-4">No recent disease predictions.</p>
            ) : (
              <ul className="space-y-3">
                {data.recent_activity.diseases.map(d => (
                  <li key={d.id} className="flex justify-between items-center p-3 hover:bg-slate-50 rounded-lg transition-colors border border-transparent hover:border-slate-100 group">
                    <div>
                      <p className="font-medium text-slate-800 text-sm group-hover:text-emerald-700 transition-colors">{d.disease.replace(/___/g, ' - ').replace(/_/g, ' ')}</p>
                      <p className="text-xs text-slate-500">{new Date(d.date).toLocaleDateString()}</p>
                    </div>
                    <span className="bg-rose-50 text-rose-700 text-xs font-semibold px-2.5 py-1 rounded-full border border-rose-100 shadow-sm">
                      {(d.confidence * 100).toFixed(1)}% Conf
                    </span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

        {/* AI Recommendations */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
          <div className="p-4 border-b border-slate-100 flex justify-between items-center bg-slate-50">
            <h3 className="font-semibold text-slate-800 flex items-center gap-2">
              <Cpu className="w-4 h-4 text-blue-500" /> Latest Recommendations
            </h3>
          </div>
          <div className="p-4">
            <div className="space-y-4">
              <div>
                <div className="flex justify-between items-center mb-2">
                  <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Fertilizer Plans</h4>
                  <Link to="/fertilizer-recommendation" className="text-xs text-emerald-600 hover:underline">Get new plan &rarr;</Link>
                </div>
                {data.recent_activity.fertilizer_recommendations.length === 0 ? (
                  <p className="text-xs text-slate-500 italic bg-slate-50 p-3 rounded-md">No plans yet.</p>
                ) : (
                  <ul className="space-y-2">
                    {data.recent_activity.fertilizer_recommendations.slice(0,2).map(f => (
                      <li key={f.id} className="flex items-start gap-3 p-2 hover:bg-slate-50 rounded-md transition-colors border border-transparent hover:border-slate-100">
                        <div className="mt-0.5 bg-blue-100 p-1.5 rounded-md text-blue-600 shadow-sm"><Sprout className="w-3.5 h-3.5" /></div>
                        <div>
                          <p className="text-sm font-medium text-slate-800">{f.fertilizer}</p>
                          <p className="text-xs text-slate-500">For {f.crop}</p>
                        </div>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
              
              <div className="pt-2 border-t border-slate-50">
                <div className="flex justify-between items-center mb-2">
                  <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Crop Suggestions</h4>
                  <Link to="/crop-recommendation" className="text-xs text-emerald-600 hover:underline">Get new suggestion &rarr;</Link>
                </div>
                {data.recent_activity.crop_recommendations.length === 0 ? (
                  <p className="text-xs text-slate-500 italic bg-slate-50 p-3 rounded-md">No suggestions yet.</p>
                ) : (
                  <ul className="space-y-2">
                    {data.recent_activity.crop_recommendations.slice(0,2).map(c => (
                      <li key={c.id} className="flex items-start gap-3 p-2 hover:bg-slate-50 rounded-md transition-colors border border-transparent hover:border-slate-100">
                        <div className="mt-0.5 bg-emerald-100 p-1.5 rounded-md text-emerald-600 shadow-sm"><Leaf className="w-3.5 h-3.5" /></div>
                        <div>
                          <p className="text-sm font-medium text-slate-800 capitalize">{c.crop}</p>
                          <p className="text-xs text-slate-500">{(c.confidence*100).toFixed(1)}% match</p>
                        </div>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};
