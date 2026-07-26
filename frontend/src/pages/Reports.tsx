import React, { useEffect, useState } from "react";
import { Card, Button } from "@/components/common";
import { EmptyState } from "@/components/feedback/EmptyState";
import { FileText, Download, TrendingUp, Activity, Lightbulb } from "lucide-react";
import { reportService } from "@/api/report.service";

export const Reports: React.FC = () => {
  const [analytics, setAnalytics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const data = await reportService.getAnalytics();
      setAnalytics(data);
    } catch (error) {
      console.error("Failed to load analytics", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-slate-500">Generating analytics...</div>;
  }

  const hasData = analytics && (analytics.disease_frequency?.length > 0 || analytics.monthly_scans?.length > 0);

  return (
    <div className="flex flex-col gap-6 animate-fade-in">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-slate-100 flex items-center gap-2">
            <FileText className="h-6 w-6 text-primary-600 dark:text-primary-400" />
            Reports & Analytics
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Insights based on your farm activity, crop recommendations, and disease scans.
          </p>
        </div>
        <Button
          variant="outline"
          leftIcon={<Download className="w-4 h-4" />}
          disabled
          title="PDF export coming soon"
        >
          Export Summary
        </Button>
      </div>

      {!hasData ? (
        <Card className="p-6">
          <EmptyState
            icon={<Activity className="w-8 h-8" />}
            title="Not Enough Data"
            description="Start running disease detections and crop recommendations to generate farm analytics."
          />
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Insights Panel */}
          {analytics.insights && analytics.insights.length > 0 && (
            <Card className="p-6 md:col-span-2 bg-gradient-to-br from-primary-50 to-primary-100/50 dark:from-forest-medium dark:to-forest-medium/50 border-primary-200 dark:border-primary-900/50">
              <h2 className="text-lg font-bold text-slate-800 dark:text-slate-100 mb-4 flex items-center gap-2">
                <Lightbulb className="w-5 h-5 text-amber-500" />
                AI Generated Insights
              </h2>
              <div className="space-y-3">
                {analytics.insights.map((insight: string, idx: number) => (
                  <div key={idx} className="flex gap-3 items-start bg-white/60 dark:bg-slate-900/40 p-3 rounded-xl border border-primary-100 dark:border-forest-light">
                    <div className="mt-0.5 rounded-full bg-primary-200 dark:bg-primary-900 p-1">
                      <TrendingUp className="w-3 h-3 text-primary-700 dark:text-primary-400" />
                    </div>
                    <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">{insight}</p>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Disease Frequency */}
          <Card className="p-6 flex flex-col h-full">
            <h2 className="text-lg font-bold text-slate-800 dark:text-slate-100 mb-4 flex items-center gap-2">
              <Activity className="w-5 h-5 text-rose-500" />
              Disease Frequencies
            </h2>
            <div className="space-y-4 flex-1">
              {analytics.disease_frequency?.length > 0 ? (
                analytics.disease_frequency.map((df: any, idx: number) => (
                  <div key={idx} className="flex flex-col gap-1">
                    <div className="flex justify-between text-sm">
                      <span className="font-medium text-slate-700 dark:text-slate-300 truncate pr-2">{df.predicted_class}</span>
                      <span className="text-slate-500 dark:text-slate-400 font-bold">{df.count}</span>
                    </div>
                    <div className="w-full bg-slate-100 dark:bg-slate-800 rounded-full h-2">
                      <div 
                        className="bg-rose-500 h-2 rounded-full" 
                        style={{ width: `${Math.min((df.count / Math.max(...analytics.disease_frequency.map((d:any)=>d.count))) * 100, 100)}%` }}
                      ></div>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-sm text-slate-500">No disease scans recorded yet.</p>
              )}
            </div>
          </Card>

          {/* Monthly Scans */}
          <Card className="p-6 flex flex-col h-full">
            <h2 className="text-lg font-bold text-slate-800 dark:text-slate-100 mb-4 flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-blue-500" />
              Monthly Scan Activity
            </h2>
            <div className="flex items-end gap-2 h-48 mt-auto pt-4 border-b border-l border-slate-200 dark:border-forest-light px-2 pb-2">
              {analytics.monthly_scans?.length > 0 ? (
                analytics.monthly_scans.map((ms: any, idx: number) => {
                  const maxCount = Math.max(...analytics.monthly_scans.map((m:any) => m.count), 1);
                  const heightPercentage = Math.max((ms.count / maxCount) * 100, 10);
                  
                  return (
                    <div key={idx} className="flex-1 flex flex-col items-center justify-end group">
                      <div 
                        className="w-full max-w-[40px] bg-blue-500/80 hover:bg-blue-600 rounded-t-md transition-all relative"
                        style={{ height: `${heightPercentage}%` }}
                      >
                        <div className="absolute -top-7 left-1/2 -translate-x-1/2 bg-slate-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity">
                          {ms.count}
                        </div>
                      </div>
                      <span className="text-[10px] text-slate-500 mt-2 truncate w-full text-center block" title={ms.month}>{ms.month.split(' ')[0]}</span>
                    </div>
                  )
                })
              ) : (
                <div className="w-full h-full flex items-center justify-center text-sm text-slate-500">
                  No scan activity over the last 6 months.
                </div>
              )}
            </div>
          </Card>
        </div>
      )}
    </div>
  );
};

export default Reports;
