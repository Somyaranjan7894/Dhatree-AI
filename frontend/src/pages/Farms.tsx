import React, { useEffect, useState } from "react";
import { Card, Button, Modal, Input } from "@/components/common";
import { EmptyState } from "@/components/feedback/EmptyState";
import { Sprout, Plus, MapPin } from "lucide-react";
import { farmService } from "@/api/farm.service";
import { Farm } from "@/types";
import { useNavigate } from "react-router-dom";

export const Farms: React.FC = () => {
  const [farms, setFarms] = useState<Farm[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [newFarm, setNewFarm] = useState({
    farm_name: "",
    area: "",
    village: "",
    district: "",
    state: "",
    water_source: "rainfed"
  });
  const navigate = useNavigate();

  useEffect(() => {
    fetchFarms();
  }, []);

  const fetchFarms = async () => {
    try {
      const data = await farmService.getFarms();
      setFarms(data);
    } catch (error) {
      console.error("Failed to fetch farms", error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateFarm = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await farmService.createFarm({
        ...newFarm,
        area: parseFloat(newFarm.area) || 0,
      });
      setIsModalOpen(false);
      setNewFarm({
        farm_name: "",
        area: "",
        village: "",
        district: "",
        state: "",
        water_source: "rainfed"
      });
      await fetchFarms();
    } catch (error: any) {
      console.error("Failed to create farm", error?.response?.data || error);
      alert(`Failed to create farm: ${JSON.stringify(error?.response?.data || "Check inputs")}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-slate-500">Loading farms...</div>;
  }

  return (
    <div className="flex flex-col gap-6 animate-fade-in">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-slate-100 flex items-center gap-2">
            <Sprout className="h-6 w-6 text-primary-600 dark:text-primary-400" />
            My Registered Farms
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Manage your agricultural land parcels, soil profiles, and geo-spatial boundaries.
          </p>
        </div>
        <Button
          variant="primary"
          leftIcon={<Plus className="w-4 h-4" />}
          onClick={() => setIsModalOpen(true)}
        >
          Register New Farm Parcel
        </Button>
      </div>

      {farms.length === 0 ? (
        <Card className="p-6">
          <EmptyState
            icon={<MapPin className="w-8 h-8" />}
            title="No Active Farm Parcels Loaded"
            description="You don't have any registered farms yet."
            actionLabel="Register Farm"
            onAction={() => setIsModalOpen(true)}
          />
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {farms.map((farm) => (
            <Card key={farm.id} className="p-6 hover:shadow-lg transition-shadow cursor-pointer" onClick={() => navigate(`/farms/${farm.id}`)}>
              <div className="flex justify-between items-start mb-4">
                <h3 className="font-semibold text-lg text-slate-800 dark:text-slate-100">{farm.farm_name}</h3>
                <span className="px-2 py-1 bg-primary-100 text-primary-700 rounded text-xs font-medium dark:bg-primary-900/30 dark:text-primary-400">
                  {farm.area} Acres
                </span>
              </div>
              <div className="space-y-2 text-sm text-slate-600 dark:text-slate-300">
                <p><span className="font-medium">Location:</span> {farm.village}, {farm.district}, {farm.state}</p>
                {farm.soil_type && <p><span className="font-medium">Soil Type:</span> {farm.soil_type}</p>}
                <p><span className="font-medium">Water Source:</span> {farm.water_source}</p>
              </div>
            </Card>
          ))}
        </div>
      )}

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Register New Farm Parcel"
        description="Add a new farm to manage crops, track soil health, and receive recommendations."
      >
        <form onSubmit={handleCreateFarm} className="space-y-4 mt-4">
          <Input
            label="Farm Name"
            placeholder="e.g., North Field"
            value={newFarm.farm_name}
            onChange={(e) => setNewFarm({ ...newFarm, farm_name: e.target.value })}
            required
          />
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Area (Acres)"
              type="number"
              step="0.01"
              placeholder="e.g., 10.5"
              value={newFarm.area}
              onChange={(e) => setNewFarm({ ...newFarm, area: e.target.value })}
              required
            />
            <Input
              label="Village / Town"
              placeholder="e.g., Kothapalli"
              value={newFarm.village}
              onChange={(e) => setNewFarm({ ...newFarm, village: e.target.value })}
              required
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="District"
              placeholder="e.g., Karimnagar"
              value={newFarm.district}
              onChange={(e) => setNewFarm({ ...newFarm, district: e.target.value })}
              required
            />
            <Input
              label="State"
              placeholder="e.g., Telangana"
              value={newFarm.state}
              onChange={(e) => setNewFarm({ ...newFarm, state: e.target.value })}
              required
            />
          </div>

          <div className="space-y-1">
            <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
              Water Source
            </label>
            <select
              className="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-forest-light dark:bg-forest-medium dark:text-white"
              value={newFarm.water_source}
              onChange={(e) => setNewFarm({ ...newFarm, water_source: e.target.value })}
            >
              <option value="rainfed">Rainfed / Monsoon</option>
              <option value="canal">Canal Irrigation</option>
              <option value="tube_well">Tube Well / Borewell</option>
              <option value="open_well">Open Well</option>
              <option value="drip_irrigation">Drip Irrigation System</option>
              <option value="sprinkler">Sprinkler Irrigation System</option>
              <option value="other">Other / Mixed</option>
            </select>
          </div>

          <div className="pt-4 flex justify-end gap-3 border-t border-slate-100 dark:border-forest-light">
            <Button variant="outline" type="button" onClick={() => setIsModalOpen(false)}>
              Cancel
            </Button>
            <Button variant="primary" type="submit" isLoading={isSubmitting}>
              Register Farm
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default Farms;
