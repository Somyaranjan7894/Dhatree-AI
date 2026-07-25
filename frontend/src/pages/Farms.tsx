import React, { useEffect, useState } from "react";
import { Card, Button } from "@/components/common";
import { EmptyState } from "@/components/feedback/EmptyState";
import { Sprout, Plus, MapPin } from "lucide-react";
import { farmService } from "@/api/farm.service";
import { Farm } from "@/types";
import { useNavigate } from "react-router-dom";

export const Farms: React.FC = () => {
  const [farms, setFarms] = useState<Farm[]>([]);
  const [loading, setLoading] = useState(true);
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
          onClick={() => {
            // Future feature: create new farm
            alert("Create new farm feature coming soon");
          }}
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
            onAction={() => alert("Create new farm feature coming soon")}
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
                <p><span className="font-medium">Soil Type:</span> {farm.soil_type}</p>
                <p><span className="font-medium">Water Source:</span> {farm.water_source}</p>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default Farms;
