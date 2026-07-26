import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Card, Button, Modal, Input } from "@/components/common";
import { farmService } from "@/api/farm.service";
import { WeatherSnapshot } from "@/types";
import { ArrowLeft, CloudRain, Wind, Thermometer } from "lucide-react";
import { EmptyState } from "@/components/feedback/EmptyState";

export const Weather: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [snapshots, setSnapshots] = useState<WeatherSnapshot[]>([]);
  const [loading, setLoading] = useState(true);
  
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [newSnapshot, setNewSnapshot] = useState({
    date: new Date().toISOString().split("T")[0],
    temperature: "",
    humidity: "",
    rainfall: "",
    wind_speed: "",
  });

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

  const handleRecordSnapshot = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!id) return;
    
    setIsSubmitting(true);
    try {
      await farmService.addWeatherSnapshot(id, {
        date: newSnapshot.date,
        temperature: newSnapshot.temperature ? parseFloat(newSnapshot.temperature) : null,
        humidity: newSnapshot.humidity ? parseFloat(newSnapshot.humidity) : null,
        rainfall: newSnapshot.rainfall ? parseFloat(newSnapshot.rainfall) : null,
        wind_speed: newSnapshot.wind_speed ? parseFloat(newSnapshot.wind_speed) : null,
      });
      setIsModalOpen(false);
      setNewSnapshot({
        date: new Date().toISOString().split("T")[0],
        temperature: "",
        humidity: "",
        rainfall: "",
        wind_speed: "",
      });
      await fetchWeatherSnapshots(id);
    } catch (error) {
      console.error("Failed to record weather snapshot", error);
      alert("Failed to record snapshot. Please check your inputs.");
    } finally {
      setIsSubmitting(false);
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
          <Button variant="primary" onClick={() => setIsModalOpen(true)}>
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
            onAction={() => setIsModalOpen(true)}
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

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Record Weather Snapshot"
        description="Log current or past weather conditions for this farm."
      >
        <form onSubmit={handleRecordSnapshot} className="space-y-4 mt-4">
          <Input
            label="Date"
            type="date"
            value={newSnapshot.date}
            onChange={(e) => setNewSnapshot({ ...newSnapshot, date: e.target.value })}
            required
          />
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Temperature (°C)"
              type="number"
              step="0.1"
              placeholder="e.g., 28.5"
              value={newSnapshot.temperature}
              onChange={(e) => setNewSnapshot({ ...newSnapshot, temperature: e.target.value })}
            />
            <Input
              label="Humidity (%)"
              type="number"
              step="1"
              placeholder="e.g., 65"
              value={newSnapshot.humidity}
              onChange={(e) => setNewSnapshot({ ...newSnapshot, humidity: e.target.value })}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Rainfall (mm)"
              type="number"
              step="0.1"
              placeholder="e.g., 12.0"
              value={newSnapshot.rainfall}
              onChange={(e) => setNewSnapshot({ ...newSnapshot, rainfall: e.target.value })}
            />
            <Input
              label="Wind Speed (km/h)"
              type="number"
              step="0.1"
              placeholder="e.g., 15.5"
              value={newSnapshot.wind_speed}
              onChange={(e) => setNewSnapshot({ ...newSnapshot, wind_speed: e.target.value })}
            />
          </div>

          <div className="pt-4 flex justify-end gap-3 border-t border-slate-100 dark:border-forest-light">
            <Button variant="outline" type="button" onClick={() => setIsModalOpen(false)}>
              Cancel
            </Button>
            <Button variant="primary" type="submit" isLoading={isSubmitting}>
              Save Snapshot
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default Weather;
