import React from "react";
import { Link } from "react-router-dom";
import { Button, Card } from "@/components/common";
import { Sprout } from "lucide-react";

export const NotFound: React.FC = () => {
  return (
    <div className="flex min-h-[60vh] items-center justify-center animate-fade-in">
      <Card className="max-w-md text-center flex flex-col items-center gap-4 p-8">
        <div className="h-16 w-16 rounded-2xl bg-emerald-100 text-emerald-600 flex items-center justify-center shadow-inner">
          <Sprout className="h-8 w-8" />
        </div>
        <h2 className="text-2xl font-bold text-slate-800">404 - Module Not Active</h2>
        <p className="text-sm text-slate-600 leading-relaxed">
          The requested domain boundary route has not yet been activated or is scheduled for Phase 2 implementation.
        </p>
        <Link to="/" className="w-full mt-2">
          <Button variant="primary" className="w-full">
            Return to Intelligence Hub
          </Button>
        </Link>
      </Card>
    </div>
  );
};
