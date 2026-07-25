import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Card, Button } from "@/components/common";
import { farmService } from "@/api/farm.service";
import { WeatherSnapshot } from "@/types";
import { ArrowLeft, CloudRain, Wind, Thermometer } from "lucide-react";
import { EmptyState } from "@/components/feedback/EmptyState";

export const Weather: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [snapshots, setSnapshots] = useState<WeatherSnapshot[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      fetchWeatherSnapshots(id);
    } else {
      setLoading(false);
    }
  }, [id]);

  const fetchWeatherSnapshots = async (farmId: string) => {
    try {
      setLoading(true);
      const data = await farmService.getWeatherSnapshots(farmId);
      setSnapshots(data);
    } catch (error) {
      console.error("Failed to fetch weather snapshots", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-8 text-center">Loading...</div>;

  if (!id) {
    return (
      <div className="flex flex-col gap-6 animate-fade-in">
        <h1 className="text-2xl font-bold text-slate-800 dark:text-slate-100 flex items-center gap-2">
          <CloudRain className="h-6 w-6 text-blue-600 dark:text-blue-400" />
          Weather Intelligence
        </h1>
        <Card className="p-6">
          <EmptyState
            icon={<CloudRain className="w-8 h-8" />}
            title="Select a Farm"
            description="Weather data is tied to specific farm locations. Please select a farm from the 'My Farms' menu to view its weather intelligence."
            actionLabel="Go to My Farms"
            onAction={() => navigate("/farms")}
          />
        </Card>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6 animate-fade-in">
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <Button variant="outline" onClick={() => navigate(id ? `/farms/${id}` : "/farms")} leftIcon={<ArrowLeft className="w-4 h-4" />}>
            Back
          </Button>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-slate-100 flex items-center gap-2">
            <CloudRain className="h-6 w-6 text-blue-600 dark:text-blue-400" />
            Weather Snapshots
          </h1>
        </div>
        {id && (
          <Button variant="primary" onClick={() => alert("Add snapshot feature coming soon")}>
            Record Snapshot
          </Button>
        )}
      </div>

      {snapshots.length === 0 ? (
        <Card className="p-6">
          <EmptyState
            icon={<CloudRain className="w-8 h-8" />}
            title="No Weather Snapshots"
            description="No weather snapshots have been recorded for this farm yet."
            actionLabel="Record Snapshot"
            onAction={() => alert("Add snapshot feature coming soon")}
          />
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {snapshots.map((snapshot) => (
            <Card key={snapshot.id} className="p-5 flex flex-col gap-4">
              <div className="text-sm font-semibold text-slate-500 border-b pb-2">
                {new Date(snapshot.date).toLocaleDateString()}
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-slate-700 dark:text-slate-200">
                  <Thermometer className="w-5 h-5 text-red-500" />
                  <span className="font-medium">{snapshot.temperature ?? '--'} °C</span>
                </div>
                <div className="flex items-center gap-2 text-slate-700 dark:text-slate-200">
                  <CloudRain className="w-5 h-5 text-blue-500" />
                  <span className="font-medium">{snapshot.rainfall ?? '--'} mm</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-slate-700 dark:text-slate-200">
                  <Wind className="w-5 h-5 text-gray-500" />
                  <span className="font-medium">{snapshot.wind_speed ?? '--'} km/h</span>
                </div>
                <div className="text-sm text-slate-500">
                  Hum: {snapshot.humidity ?? '--'}%
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default Weather;
