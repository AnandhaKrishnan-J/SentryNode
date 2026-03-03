"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import Sidebar from "@/components/Sidebar";

export default function LogsPage() {
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchLogs() {
      try {
        const response = await api.getTrafficLogs();
        setLogs(response.items || []);
      } catch (err: any) {
        setError(err.message || "Failed to fetch logs");
      } finally {
        setLoading(false);
      }
    }
    fetchLogs();
  }, []);

  return (
    <div className="flex min-h-screen bg-[#fbfbfc]">
      <Sidebar />
      <main className="flex-1 ml-64 p-8">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-[#1c1c1e]">Traffic Logs</h1>
          <p className="text-[#8e8e93]">Real-time network traffic and deep packet inspection</p>
        </header>

        {error && (
          <div className="mb-8 p-4 bg-red-50 text-red-600 rounded-2xl border border-red-100">
            {error}
          </div>
        )}

        <div className="bg-white rounded-3xl premium-shadow overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="bg-[#fbfbfc] border-b border-[#e5e5ea]">
                  <th className="px-6 py-4 text-xs font-bold uppercase text-[#8e8e93] tracking-wider">Timestamp</th>
                  <th className="px-6 py-4 text-xs font-bold uppercase text-[#8e8e93] tracking-wider">Source IP</th>
                  <th className="px-6 py-4 text-xs font-bold uppercase text-[#8e8e93] tracking-wider">Dest IP</th>
                  <th className="px-6 py-4 text-xs font-bold uppercase text-[#8e8e93] tracking-wider">Protocol</th>
                  <th className="px-6 py-4 text-xs font-bold uppercase text-[#8e8e93] tracking-wider text-right">Packets</th>
                  <th className="px-6 py-4 text-xs font-bold uppercase text-[#8e8e93] tracking-wider text-right">Bytes</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#e5e5ea]">
                {loading ? (
                  <tr>
                    <td colSpan={6} className="px-6 py-12 text-center text-[#8e8e93]">
                      <div className="h-6 w-6 animate-spin rounded-full border-2 border-primary border-t-transparent mx-auto mb-2"></div>
                      Loading logs...
                    </td>
                  </tr>
                ) : logs.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="px-6 py-12 text-center text-[#8e8e93]">
                      No traffic logs found.
                    </td>
                  </tr>
                ) : (
                  logs.map((log) => (
                    <tr key={log.id} className="hover:bg-[#fbfbfc] transition-colors">
                      <td className="px-6 py-4 text-sm text-[#1c1c1e] font-medium whitespace-nowrap">
                        {new Date(log.timestamp).toLocaleString()}
                      </td>
                      <td className="px-6 py-4 text-sm">
                        <span className="font-mono bg-[#f2f2f7] px-2 py-1 rounded text-[#1c1c1e]">
                          {log.source_ip}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm">
                        <span className="font-mono bg-[#f2f2f7] px-2 py-1 rounded text-[#1c1c1e]">
                          {log.destination_ip}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-primary/10 text-primary">
                          {log.protocol}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-[#1c1c1e] text-right">
                        {log.packet_count.toLocaleString()}
                      </td>
                      <td className="px-6 py-4 text-sm text-[#1c1c1e] text-right font-semibold">
                        {log.byte_count.toLocaleString()}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}
