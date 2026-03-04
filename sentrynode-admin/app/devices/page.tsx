"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import Sidebar from "@/components/Sidebar";
import Link from "next/link";

export default function DevicesPage() {
  const [devices, setDevices] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchDevices() {
      try {
        const response = await api.getDevices();
        setDevices(response.devices);
      } catch (err: any) {
        setError(err.message || "Failed to fetch devices");
      } finally {
        setLoading(false);
      }
    }
    fetchDevices();
  }, []);

  return (
    <div className="flex min-h-screen bg-[#fbfbfc]">
      <Sidebar />
      <main className="flex-1 ml-64 p-8">
        <header className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-[#1c1c1e]">Device Management</h1>
            <p className="text-[#8e8e93]">Manage and monitor your Sentry nodes</p>
          </div>
          <Link 
            href="/devices/add"
            className="bg-primary text-white px-6 py-3 rounded-xl font-semibold shadow-lg shadow-primary/30 transition-all hover:scale-[1.02] active:scale-[0.98]"
          >
            Add Device
          </Link>
        </header>

        {error && (
          <div className="mb-8 p-4 bg-red-50 text-red-600 rounded-2xl border border-red-100">
            {error}
          </div>
        )}

        <div className="bg-white rounded-3xl premium-shadow overflow-hidden">
          <table className="w-full text-left">
            <thead>
              <tr className="bg-[#fbfbfc] border-b border-[#e5e5ea]">
                <th className="px-6 py-4 text-xs font-bold uppercase text-[#8e8e93]">Device Name</th>
                <th className="px-6 py-4 text-xs font-bold uppercase text-[#8e8e93]">Identifier</th>
                <th className="px-6 py-4 text-xs font-bold uppercase text-[#8e8e93]">Location</th>
                <th className="px-6 py-4 text-xs font-bold uppercase text-[#8e8e93]">IP Address</th>
                <th className="px-6 py-4 text-xs font-bold uppercase text-[#8e8e93]">Status</th>
                <th className="px-6 py-4 text-xs font-bold uppercase text-[#8e8e93]">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#e5e5ea]">
              {loading ? (
                <tr>
                   <td colSpan={6} className="px-6 py-12 text-center">
                     <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent mx-auto"></div>
                   </td>
                </tr>
              ) : devices.length > 0 ? (
                devices.map((device) => (
                  <tr key={device.id} className="hover:bg-[#fbfbfc] transition-colors">
                    <td className="px-6 py-4 font-semibold text-[#1c1c1e]">{device.device_name}</td>
                    <td className="px-6 py-4 text-sm text-[#636366]">{device.device_identifier}</td>
                    <td className="px-6 py-4 text-sm text-[#636366]">{device.location}</td>
                    <td className="px-6 py-4 text-sm font-mono text-[#636366]">{device.ip_address}</td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold ${device.is_active ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-600'}`}>
                        {device.is_active ? 'ACTIVE' : 'INACTIVE'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <button className="text-sm font-bold text-primary hover:underline">Manage</button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-[#8e8e93]">No devices found</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}
