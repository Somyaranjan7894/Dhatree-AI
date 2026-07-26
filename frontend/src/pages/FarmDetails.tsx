import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Card, Button, Modal, Input } from "@/components/common";
import { farmService } from "@/api/farm.service";
import { cropService } from "@/api/crop.service";
import { Farm, FarmCrop } from "@/types";
import { ArrowLeft, Leaf, Droplets, CloudRain } from "lucide-react";

export const FarmDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [farm, setFarm] = useState<Farm | null>(null);
  const [crops, setCrops] = useState<FarmCrop[]>([]);
  const [availableCrops, setAvailableCrops] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [newCrop, setNewCrop] = useState({
    crop: "",
    sowing_date: new Date().toISOString().split("T")[0],
    expected_harvest_date: "",
    area_allocated: "",
    status: "sown"
  });

  useEffect(() => {
    if (id) {
      fetchFarmDetails(id);
      fetchAvailableCrops();
    }
  }, [id]);

  const fetchAvailableCrops = async () => {
    try {
      const data = await cropService.getCrops();
      const cropsArray = Array.isArray(data) ? data : (data?.results || data?.data || []);
      setAvailableCrops(cropsArray);
      if (cropsArray.length > 0) {
        setNewCrop(prev => ({ ...prev, crop: cropsArray[0].id }));
      }
    } catch (error) {
      console.error("Failed to fetch available crops", error);
      setAvailableCrops([]);
    }
  };

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

  const handleAddCrop = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!id) return;
    setIsSubmitting(true);
    try {
      await farmService.addFarmCrop(id, {
        crop: newCrop.crop,
        sowing_date: newCrop.sowing_date,
        expected_harvest_date: newCrop.expected_harvest_date || null,
        area_allocated: newCrop.area_allocated ? parseFloat(newCrop.area_allocated) : null,
        status: newCrop.status
      });
      setIsModalOpen(false);
      setNewCrop(prev => ({
        ...prev,
        sowing_date: new Date().toISOString().split("T")[0],
        expected_harvest_date: "",
        area_allocated: "",
        status: "sown"
      }));
      await fetchFarmDetails(id);
    } catch (error: any) {
      console.error("Failed to add crop", error);
      alert(`Failed to add crop: ${JSON.stringify(error?.response?.data || "Check inputs")}`);
    } finally {
      setIsSubmitting(false);
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
              <Button variant="primary" size="sm" onClick={() => setIsModalOpen(true)}>
                Add Crop
              </Button>
            </div>
            {crops.length === 0 ? (
              <p className="text-sm text-slate-500 italic">No crops actively grown on this farm.</p>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {crops.map((fc: any) => (
                  <div key={fc.id} className="p-4 border rounded-lg bg-slate-50 dark:bg-slate-800 dark:border-slate-700">
                    <div className="flex items-center gap-2 mb-2">
                      <Leaf className="w-5 h-5 text-green-600" />
                      <span className="font-medium">{fc.crop_name || fc.crop}</span>
                    </div>
                    <div className="text-xs text-slate-500 dark:text-slate-400 space-y-1">
                      <p>Sown: {new Date(fc.sowing_date).toLocaleDateString()}</p>
                      <p>Expected Harvest: {fc.expected_harvest_date ? new Date(fc.expected_harvest_date).toLocaleDateString() : 'N/A'}</p>
                      <p>Status: <span className="uppercase font-semibold text-primary-600">{fc.status_display || fc.status}</span></p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>
        </div>
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Add Crop to Farm"
        description="Register a new crop cycle on this farm."
      >
        <form onSubmit={handleAddCrop} className="space-y-4 mt-4">
          <div className="space-y-1">
            <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
              Crop Type
            </label>
            <select
              className="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-forest-light dark:bg-forest-medium dark:text-white"
              value={newCrop.crop}
              onChange={(e) => setNewCrop({ ...newCrop, crop: e.target.value })}
              required
            >
              <option value="" disabled>Select a crop</option>
              {availableCrops.map((c: any) => (
                <option key={c.id} value={c.id}>{c.crop_name}</option>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Sowing Date"
              type="date"
              value={newCrop.sowing_date}
              onChange={(e) => setNewCrop({ ...newCrop, sowing_date: e.target.value })}
              required
            />
            <Input
              label="Expected Harvest Date"
              type="date"
              value={newCrop.expected_harvest_date}
              onChange={(e) => setNewCrop({ ...newCrop, expected_harvest_date: e.target.value })}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Area Allocated (Acres)"
              type="number"
              step="0.01"
              placeholder="e.g., 2.5"
              value={newCrop.area_allocated}
              onChange={(e) => setNewCrop({ ...newCrop, area_allocated: e.target.value })}
              required
            />
            <div className="space-y-1">
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                Status
              </label>
              <select
                className="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-forest-light dark:bg-forest-medium dark:text-white"
                value={newCrop.status}
                onChange={(e) => setNewCrop({ ...newCrop, status: e.target.value })}
              >
                <option value="sown">Sown / Planted</option>
                <option value="vegetative">Vegetative Stage</option>
                <option value="harvested">Harvested</option>
                <option value="failed">Failed / Damaged</option>
              </select>
            </div>
          </div>

          <div className="pt-4 flex justify-end gap-3 border-t border-slate-100 dark:border-forest-light">
            <Button variant="outline" type="button" onClick={() => setIsModalOpen(false)}>
              Cancel
            </Button>
            <Button variant="primary" type="submit" isLoading={isSubmitting}>
              Add Crop
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default FarmDetails;
