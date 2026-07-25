import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Card, Button } from "@/components/common";
import { farmService } from "@/api/farm.service";
import { Farm, FarmCrop } from "@/types";
import { ArrowLeft, Leaf, Droplets, CloudRain } from "lucide-react";

export const FarmDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [farm, setFarm] = useState<Farm | null>(null);
  const [crops, setCrops] = useState<FarmCrop[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      fetchFarmDetails(id);
    }
  }, [id]);

  const fetchFarmDetails = async (farmId: string) => {
    try {
      setLoading(true);
      const [farmData, cropsData] = await Promise.all([
        farmService.getFarm(farmId),
        farmService.getFarmCrops(farmId)
      ]);
      setFarm(farmData);
      setCrops(cropsData);
    } catch (error) {
      console.error("Failed to fetch farm details", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-8 text-center">Loading...</div>;
  if (!farm) return <div className="p-8 text-center text-red-500">Farm not found</div>;

  return (
    <div className="flex flex-col gap-6 animate-fade-in">
      <div className="flex items-center gap-4">
        <Button variant="outline" onClick={() => navigate("/farms")} leftIcon={<ArrowLeft className="w-4 h-4" />}>
          Back
        </Button>
        <h1 className="text-2xl font-bold text-slate-800 dark:text-slate-100">
          {farm.farm_name}
        </h1>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="p-6 md:col-span-1">
          <h2 className="text-lg font-semibold mb-4 border-b pb-2">Overview</h2>
          <div className="space-y-3 text-sm">
            <p><span className="font-medium text-slate-500">Area:</span> {farm.area} Acres</p>
            <p><span className="font-medium text-slate-500">Location:</span> {farm.village}, {farm.district}, {farm.state}</p>
            <p><span className="font-medium text-slate-500">Coordinates:</span> {farm.latitude ?? 'N/A'}, {farm.longitude ?? 'N/A'}</p>
            <p><span className="font-medium text-slate-500">Soil Type:</span> {farm.soil_type}</p>
            <p><span className="font-medium text-slate-500">Water Source:</span> {farm.water_source}</p>
          </div>
          <div className="mt-6 flex flex-col gap-3">
            <Button variant="secondary" onClick={() => navigate(`/farms/${farm.id}/soil-records`)} leftIcon={<Droplets className="w-4 h-4" />} className="w-full justify-start">
              Soil Records
            </Button>
            <Button variant="secondary" onClick={() => navigate(`/farms/${farm.id}/weather`)} leftIcon={<CloudRain className="w-4 h-4" />} className="w-full justify-start">
              Weather Snapshots
            </Button>
          </div>
        </Card>

        <div className="md:col-span-2 flex flex-col gap-6">
          <Card className="p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold">Active Crops</h2>
              <Button variant="primary" size="sm" onClick={() => alert("Add crop feature coming soon")}>
                Add Crop
              </Button>
            </div>
            {crops.length === 0 ? (
              <p className="text-sm text-slate-500 italic">No crops actively grown on this farm.</p>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {crops.map((fc) => (
                  <div key={fc.id} className="p-4 border rounded-lg bg-slate-50 dark:bg-slate-800 dark:border-slate-700">
                    <div className="flex items-center gap-2 mb-2">
                      <Leaf className="w-5 h-5 text-green-600" />
                      <span className="font-medium">{fc.crop}</span>
                    </div>
                    <div className="text-xs text-slate-500 dark:text-slate-400 space-y-1">
                      <p>Sown: {new Date(fc.sowing_date).toLocaleDateString()}</p>
                      <p>Expected Harvest: {fc.expected_harvest_date ? new Date(fc.expected_harvest_date).toLocaleDateString() : 'N/A'}</p>
                      <p>Status: <span className="uppercase font-semibold text-primary-600">{fc.status}</span></p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
};

export default FarmDetails;
