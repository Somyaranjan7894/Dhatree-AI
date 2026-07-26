import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Card, Button, Modal, Input } from "@/components/common";
import { farmService } from "@/api/farm.service";
import { SoilSample } from "@/types";
import { ArrowLeft, Beaker } from "lucide-react";
import { EmptyState } from "@/components/feedback/EmptyState";

export const SoilRecords: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [records, setRecords] = useState<SoilSample[]>([]);
  const [loading, setLoading] = useState(true);

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [newRecord, setNewRecord] = useState({
    sample_date: new Date().toISOString().split("T")[0],
    nitrogen: "",
    phosphorus: "",
    potassium: "",
    organic_carbon: "",
    ph_level: "",
    moisture: "",
    electrical_conductivity: "",
    texture: "",
    remarks: ""
  });

  useEffect(() => {
    if (id) {
      fetchSoilRecords(id);
    }
  }, [id]);

  const fetchSoilRecords = async (farmId: string) => {
    try {
      setLoading(true);
      const data = await farmService.getSoilSamples(farmId);
      setRecords(data);
    } catch (error) {
      console.error("Failed to fetch soil records", error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddRecord = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!id) return;
    setIsSubmitting(true);
    try {
      await farmService.addSoilSample(id, {
        sample_date: newRecord.sample_date,
        nitrogen: newRecord.nitrogen ? parseFloat(newRecord.nitrogen) : null,
        phosphorus: newRecord.phosphorus ? parseFloat(newRecord.phosphorus) : null,
        potassium: newRecord.potassium ? parseFloat(newRecord.potassium) : null,
        organic_carbon: newRecord.organic_carbon ? parseFloat(newRecord.organic_carbon) : null,
        ph_level: newRecord.ph_level ? parseFloat(newRecord.ph_level) : null,
        moisture: newRecord.moisture ? parseFloat(newRecord.moisture) : null,
        electrical_conductivity: newRecord.electrical_conductivity ? parseFloat(newRecord.electrical_conductivity) : null,
        texture: newRecord.texture || "",
        remarks: newRecord.remarks || ""
      } as SoilSample);
      setIsModalOpen(false);
      setNewRecord({
        sample_date: new Date().toISOString().split("T")[0],
        nitrogen: "",
        phosphorus: "",
        potassium: "",
        organic_carbon: "",
        ph_level: "",
        moisture: "",
        electrical_conductivity: "",
        texture: "",
        remarks: ""
      });
      await fetchSoilRecords(id);
    } catch (error: any) {
      console.error("Failed to add soil record", error);
      alert(`Failed to add record: ${JSON.stringify(error?.response?.data || "Check inputs")}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading) return <div className="p-8 text-center">Loading...</div>;

  return (
    <div className="flex flex-col gap-6 animate-fade-in">
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <Button variant="outline" onClick={() => navigate(`/farms/${id}`)} leftIcon={<ArrowLeft className="w-4 h-4" />}>
            Back to Farm
          </Button>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-slate-100 flex items-center gap-2">
            <Beaker className="h-6 w-6 text-amber-600 dark:text-amber-400" />
            Soil Records
          </h1>
        </div>
        <Button variant="primary" onClick={() => setIsModalOpen(true)}>
          Add Record
        </Button>
      </div>

      {records.length === 0 ? (
        <Card className="p-6">
          <EmptyState
            icon={<Beaker className="w-8 h-8" />}
            title="No Soil Records"
            description="No soil analysis records have been uploaded for this farm yet."
            actionLabel="Add Record"
            onAction={() => setIsModalOpen(true)}
          />
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {records.map((record) => (
            <Card key={record.id} className="p-6">
              <div className="flex justify-between items-center mb-4 border-b pb-2">
                <span className="font-semibold text-slate-700 dark:text-slate-200">
                  Sample Date: {new Date(record.sample_date).toLocaleDateString()}
                </span>
                <span className="text-xs font-medium text-slate-500">
                  pH: {record.ph_level ?? 'N/A'}
                </span>
              </div>
              <div className="grid grid-cols-2 gap-y-2 gap-x-4 text-sm text-slate-600 dark:text-slate-300">
                <p>Nitrogen: {record.nitrogen ?? 'N/A'} kg/ha</p>
                <p>Phosphorus: {record.phosphorus ?? 'N/A'} kg/ha</p>
                <p>Potassium: {record.potassium ?? 'N/A'} kg/ha</p>
                <p>Organic Carbon: {record.organic_carbon ?? 'N/A'}%</p>
                <p>Moisture: {record.moisture ?? 'N/A'}%</p>
                <p>Texture: {record.texture ?? 'N/A'}</p>
              </div>
              {record.remarks && (
                <div className="mt-4 text-sm bg-slate-50 dark:bg-slate-800 p-3 rounded italic">
                  "{record.remarks}"
                </div>
              )}
            </Card>
          ))}
        </div>
      )}

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Add Soil Record"
        description="Log new soil test results to track your farm's health over time."
      >
        <form onSubmit={handleAddRecord} className="space-y-4 mt-4">
          <Input
            label="Sample Date"
            type="date"
            value={newRecord.sample_date}
            onChange={(e) => setNewRecord({ ...newRecord, sample_date: e.target.value })}
            required
          />

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <Input
              label="Nitrogen (N)"
              type="number"
              step="0.01"
              placeholder="kg/ha"
              value={newRecord.nitrogen}
              onChange={(e) => setNewRecord({ ...newRecord, nitrogen: e.target.value })}
            />
            <Input
              label="Phosphorus (P)"
              type="number"
              step="0.01"
              placeholder="kg/ha"
              value={newRecord.phosphorus}
              onChange={(e) => setNewRecord({ ...newRecord, phosphorus: e.target.value })}
            />
            <Input
              label="Potassium (K)"
              type="number"
              step="0.01"
              placeholder="kg/ha"
              value={newRecord.potassium}
              onChange={(e) => setNewRecord({ ...newRecord, potassium: e.target.value })}
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Input
              label="pH Level"
              type="number"
              step="0.01"
              placeholder="e.g., 6.5"
              value={newRecord.ph_level}
              onChange={(e) => setNewRecord({ ...newRecord, ph_level: e.target.value })}
            />
            <Input
              label="Organic Carbon (%)"
              type="number"
              step="0.01"
              placeholder="%"
              value={newRecord.organic_carbon}
              onChange={(e) => setNewRecord({ ...newRecord, organic_carbon: e.target.value })}
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Input
              label="Moisture (%)"
              type="number"
              step="0.01"
              placeholder="%"
              value={newRecord.moisture}
              onChange={(e) => setNewRecord({ ...newRecord, moisture: e.target.value })}
            />
            <Input
              label="Electrical Cond. (mS/cm)"
              type="number"
              step="0.01"
              placeholder="mS/cm"
              value={newRecord.electrical_conductivity}
              onChange={(e) => setNewRecord({ ...newRecord, electrical_conductivity: e.target.value })}
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                Texture
              </label>
              <select
                className="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-forest-light dark:bg-forest-medium dark:text-white"
                value={newRecord.texture}
                onChange={(e) => setNewRecord({ ...newRecord, texture: e.target.value })}
              >
                <option value="">Select Texture</option>
                <option value="sandy">Sandy</option>
                <option value="silt">Silt</option>
                <option value="clay">Clay</option>
                <option value="loamy">Loamy</option>
                <option value="sandy_loam">Sandy Loam</option>
                <option value="clay_loam">Clay Loam</option>
              </select>
            </div>
            <Input
              label="Remarks / Notes"
              placeholder="Optional notes"
              value={newRecord.remarks}
              onChange={(e) => setNewRecord({ ...newRecord, remarks: e.target.value })}
            />
          </div>

          <div className="pt-4 flex justify-end gap-3 border-t border-slate-100 dark:border-forest-light">
            <Button variant="outline" type="button" onClick={() => setIsModalOpen(false)}>
              Cancel
            </Button>
            <Button variant="primary" type="submit" isLoading={isSubmitting}>
              Save Record
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default SoilRecords;
