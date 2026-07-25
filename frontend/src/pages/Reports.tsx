import React from "react";
import { Card, Button } from "@/components/common";
import { EmptyState } from "@/components/feedback/EmptyState";
import { FileText, Download } from "lucide-react";

export const Reports: React.FC = () => {
  return (
    <div className="flex flex-col gap-6 animate-fade-in">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-slate-100 flex items-center gap-2">
            <FileText className="h-6 w-6 text-primary-600 dark:text-primary-400" />
            Reports & Analytics
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Export comprehensive PDF/CSV summaries of crop cycles, fertilizer history, and pathology logs.
          </p>
        </div>
        <Button
          variant="outline"
          leftIcon={<Download className="w-4 h-4" />}
          disabled
          title="Scheduled for Phase 6 Implementation"
        >
          Export Analytics Bundle
        </Button>
      </div>

      <Card className="p-6">
        <div className="mb-4 pb-4 border-b border-slate-100 dark:border-forest-light flex items-center justify-between">
          <span className="text-sm font-semibold text-slate-700 dark:text-slate-200">
            Reports Module Boundary (`backend/modules/reports`)
          </span>
          <span className="text-xs text-primary-600 dark:text-primary-400 font-medium">
            REST API: `/api/v1/reports/`
          </span>
        </div>

        <EmptyState
          icon={<FileText className="w-8 h-8" />}
          title="Analytics Reporting Engine Standby"
          description="The reporting module orchestrates data aggregation across farms, soil analyses, and diagnostic records to generate regulatory and farm management reports. Scheduled for Phase 6 rollout."
          actionLabel="View API Specs"
          onAction={() => window.open("/api/v1/docs/", "_blank")}
        />
      </Card>
    </div>
  );
};

export default Reports;
