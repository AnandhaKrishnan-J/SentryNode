"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import Sidebar from "@/components/Sidebar";

export default function DashboardPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchData() {
      try {
        const summary = await api.getDashboardSummary();
        setData(summary);
      } catch (err: any) {
        setError(err.message || "Failed to fetch dashboard data");
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex min-h-screen bg-[#fbfbfc]">
        <Sidebar />
        <div className="flex-1 ml-64 flex items-center justify-center">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
        </div>
      </div>
    );
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "SAFE": return "text-green-600 bg-green-50";
      case "UNDER_ATTACK": return "text-red-600 bg-red-50";
      case "DEGRADED": return "text-yellow-600 bg-yellow-50";
      default: return "text-gray-600 bg-gray-50";
    }
  };

  return (
    <div className="flex min-h-screen bg-[#fbfbfc]">
      <Sidebar />
      <main className="flex-1 ml-64 p-8">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-[#1c1c1e]">Security Overview</h1>
          <p className="text-[#8e8e93]">Real-time network status and threat monitoring</p>
        </header>

        {error && (
          <div className="mb-8 p-4 bg-red-50 text-red-600 rounded-2xl border border-red-100">
            {error}
          </div>
        )}

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="p-6 bg-white rounded-3xl premium-shadow">
            <p className="text-sm font-medium text-[#8e8e93] mb-1">Security Status</p>
            <div className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold ${getStatusColor(data?.security_status)}`}>
              {data?.security_status || "UNKNOWN"}
            </div>
            <p className="text-2xl font-bold mt-2 text-[#1c1c1e]">System Protected</p>
          </div>
          <div className="p-6 bg-white rounded-3xl premium-shadow">
            <p className="text-sm font-medium text-[#8e8e93] mb-1">Active Alerts</p>
            <p className="text-3xl font-bold text-[#1c1c1e]">{data?.active_alerts || 0}</p>
            <p className="text-xs text-[#8e8e93] mt-1">Requiring immediate attention</p>
          </div>
          <div className="p-6 bg-white rounded-3xl premium-shadow">
            <p className="text-sm font-medium text-[#8e8e93] mb-1">Highest Severity</p>
            <p className="text-2xl font-bold text-[#1c1c1e]">{data?.highest_severity || "NONE"}</p>
            <p className="text-xs text-[#8e8e93] mt-1">Current threat level</p>
          </div>
        </div>

        {/* Content Tabs/Sections */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Devices List */}
          <div className="bg-white rounded-3xl premium-shadow overflow-hidden">
            <div className="px-6 py-5 border-b border-[#e5e5ea] flex justify-between items-center">
              <h3 className="font-bold text-[#1c1c1e]">Monitored Devices</h3>
              <button className="text-primary text-sm font-medium hover:underline">View All</button>
            </div>
            <div className="divide-y divide-[#e5e5ea]">
              {data?.devices?.map((device: any) => (
                <div key={device.device_id} className="px-6 py-4 flex items-center justify-between hover:bg-[#fbfbfc] transition-colors">
                  <div>
                    <p className="font-semibold text-[#1c1c1e]">{device.device_name}</p>
                    <p className="text-xs text-[#8e8e93]">Last seen: {new Date(device.last_seen).toLocaleString()}</p>
                  </div>
                  <div className="text-right">
                    <span className={`inline-block w-2 h-2 rounded-full mr-2 ${device.status === 'online' ? 'bg-green-500' : 'bg-gray-300'}`}></span>
                    <span className="text-xs font-medium uppercase text-[#636366]">{device.status}</span>
                  </div>
                </div>
              ))}
              {(!data?.devices || data.devices.length === 0) && (
                <div className="px-6 py-8 text-center text-[#8e8e93]">No devices found</div>
              )}
            </div>
          </div>

          {/* Recent Alerts */}
          <div className="bg-white rounded-3xl premium-shadow overflow-hidden">
            <div className="px-6 py-5 border-b border-[#e5e5ea] flex justify-between items-center">
              <h3 className="font-bold text-[#1c1c1e]">Recent Alerts</h3>
              <button className="text-primary text-sm font-medium hover:underline">Clear All</button>
            </div>
            <div className="divide-y divide-[#e5e5ea]">
              {data?.recent_alerts?.map((alert: any) => (
                <div key={alert.id} className="px-6 py-4 flex items-center gap-4 hover:bg-[#fbfbfc] transition-colors">
                  <div className={`p-2 rounded-xl ${alert.severity === 'CRITICAL' ? 'bg-red-100 text-red-600' : 'bg-yellow-100 text-yellow-600'}`}>
                    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                  </div>
                  <div className="flex-1">
                    <p className="font-semibold text-[#1c1c1e] text-sm">{alert.alert_type}</p>
                    <p className="text-xs text-[#8e8e93]">{new Date(alert.timestamp).toLocaleString()}</p>
                  </div>
                  <div className="text-xs font-bold text-[#636366]">
                    {alert.severity}
                  </div>
                </div>
              ))}
              {(!data?.recent_alerts || data.recent_alerts.length === 0) && (
                <div className="px-6 py-8 text-center text-[#8e8e93]">No recent alerts</div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
