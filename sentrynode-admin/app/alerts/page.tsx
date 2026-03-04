"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import Sidebar from "@/components/Sidebar";

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState({ severity: "", resolved: false });

  useEffect(() => {
    fetchAlerts();
  }, [filter]);

  async function fetchAlerts() {
    setLoading(true);
    try {
      const response = await api.getAlerts({
        severity: filter.severity || undefined,
        resolved: filter.resolved,
        limit: 100
      });
      setAlerts(response.alerts || []);
    } catch (err: any) {
      setError(err.message || "Failed to fetch alerts");
    } finally {
      setLoading(false);
    }
  }

  const handleAcknowledge = async (id: number) => {
    try {
      await api.acknowledgeAlert(id);
      setAlerts(alerts.map(a => a.id === id ? { ...a, resolved: true } : a));
    } catch (err: any) {
      alert(err.message || "Failed to acknowledge alert");
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity.toUpperCase()) {
      case "CRITICAL": return "text-red-700 bg-red-100 border-red-200";
      case "HIGH": return "text-orange-700 bg-orange-100 border-orange-200";
      case "MEDIUM": return "text-yellow-700 bg-yellow-100 border-yellow-200";
      case "LOW": return "text-blue-700 bg-blue-100 border-blue-200";
      default: return "text-gray-700 bg-gray-100 border-gray-200";
    }
  };

  return (
    <div className="flex min-h-screen bg-[#fbfbfc]">
      <Sidebar />
      <main className="flex-1 ml-64 p-8">
        <header className="mb-8 flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-bold text-[#1c1c1e]">Security Alerts</h1>
            <p className="text-[#8e8e93]">Detailed logs of network incidents and threats</p>
          </div>
          <div className="flex gap-4">
            <select 
              className="rounded-xl border border-[#e5e5ea] bg-white px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
              value={filter.severity}
              onChange={(e) => setFilter({ ...filter, severity: e.target.value })}
            >
              <option value="">All Severities</option>
              <option value="CRITICAL">Critical</option>
              <option value="HIGH">High</option>
              <option value="MEDIUM">Medium</option>
              <option value="LOW">Low</option>
            </select>
            <label className="flex items-center gap-2 text-sm text-[#636366] cursor-pointer">
              <input 
                type="checkbox"
                className="rounded border-[#e5e5ea] text-primary focus:ring-primary/20"
                checked={filter.resolved}
                onChange={(e) => setFilter({ ...filter, resolved: e.target.checked })}
              />
              Show Resolved
            </label>
          </div>
        </header>

        {error && (
          <div className="mb-8 p-4 bg-red-50 text-red-600 rounded-2xl border border-red-100 italic">
            {error}
          </div>
        )}

        <div className="bg-white rounded-3xl premium-shadow overflow-hidden">
          <table className="w-full text-left">
            <thead>
              <tr className="bg-[#fbfbfc] border-b border-[#e5e5ea]">
                <th className="px-6 py-4 text-xs font-bold uppercase text-[#8e8e93] tracking-wider">Time</th>
                <th className="px-6 py-4 text-xs font-bold uppercase text-[#8e8e93] tracking-wider">Type</th>
                <th className="px-6 py-4 text-xs font-bold uppercase text-[#8e8e93] tracking-wider">Device ID</th>
                <th className="px-6 py-4 text-xs font-bold uppercase text-[#8e8e93] tracking-wider">Severity</th>
                <th className="px-6 py-4 text-xs font-bold uppercase text-[#8e8e93] tracking-wider">Details</th>
                <th className="px-6 py-4 text-xs font-bold uppercase text-[#8e8e93] tracking-wider text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#e5e5ea]">
              {loading ? (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-[#8e8e93]">
                    <div className="h-6 w-6 animate-spin rounded-full border-2 border-primary border-t-transparent mx-auto mb-2"></div>
                    Updating signals...
                  </td>
                </tr>
              ) : alerts.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-[#8e8e93]">
                    No security alerts found matching your filters.
                  </td>
                </tr>
              ) : (
                alerts.map((alert) => (
                  <tr key={alert.id} className={`hover:bg-[#fbfbfc] transition-colors ${alert.resolved ? 'opacity-60' : ''}`}>
                    <td className="px-6 py-4 text-sm text-[#636366] whitespace-nowrap">
                      {new Date(alert.timestamp).toLocaleString()}
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm font-bold text-[#1c1c1e]">{alert.alert_type}</span>
                    </td>
                    <td className="px-6 py-4 text-sm font-mono text-[#8e8e93]">
                      {alert.device_id}
                    </td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex px-2.5 py-0.5 rounded-full text-xs font-bold border ${getSeverityColor(alert.severity)}`}>
                        {alert.severity}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-[#1c1c1e]">
                      {alert.description || "No description provided"}
                    </td>
                    <td className="px-6 py-4 text-right">
                      {!alert.resolved ? (
                        <button 
                          onClick={() => handleAcknowledge(alert.id)}
                          className="text-xs font-bold text-primary hover:underline bg-primary/5 px-3 py-1.5 rounded-lg transition-colors hover:bg-primary/10"
                        >
                          Acknowledge
                        </button>
                      ) : (
                        <span className="text-xs font-bold text-green-600 bg-green-50 px-3 py-1.5 rounded-lg border border-green-100">
                          Resolved
                        </span>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}
