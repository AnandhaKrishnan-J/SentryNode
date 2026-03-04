"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import Sidebar from "@/components/Sidebar";
import Link from "next/link";

export default function AddDevicePage() {
  const [formData, setFormData] = useState({
    device_name: "",
    device_identifier: "",
    location: "",
    ip_address: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      await api.createDevice(formData);
      router.push("/devices");
    } catch (err: any) {
      setError(err.message || "Failed to create device. Check if identifier already exists.");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="flex min-h-screen bg-[#fbfbfc]">
      <Sidebar />
      <main className="flex-1 ml-64 p-8">
        <header className="mb-8">
          <div className="flex items-center gap-4 mb-2">
            <Link href="/devices" className="text-[#8e8e93] hover:text-primary transition-colors">
              <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
            </Link>
            <h1 className="text-3xl font-bold text-[#1c1c1e]">Add New Device</h1>
          </div>
          <p className="text-[#8e8e93]">Register a new Sentry node to your network</p>
        </header>

        <div className="max-w-2xl bg-white rounded-3xl premium-shadow p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="text-sm font-medium text-[#1c1c1e]">Device Name</label>
                <input
                  type="text"
                    name="device_name"
                  required
                  className="w-full rounded-xl border border-[#e5e5ea] bg-[#fbfbfc] px-4 py-3 text-[#1c1c1e] focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
                  placeholder="e.g. Living Room Pi"
                  value={formData.device_name}
                  onChange={handleChange}
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-[#1c1c1e]">Device Identifier</label>
                <input
                  type="text"
                  name="device_identifier"
                  required
                  className="w-full rounded-xl border border-[#e5e5ea] bg-[#fbfbfc] px-4 py-3 text-[#1c1c1e] focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
                  placeholder="e.g. pi-001"
                  value={formData.device_identifier}
                  onChange={handleChange}
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-[#1c1c1e]">Location</label>
                <input
                  type="text"
                  name="location"
                  className="w-full rounded-xl border border-[#e5e5ea] bg-[#fbfbfc] px-4 py-3 text-[#1c1c1e] focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
                  placeholder="e.g. Second Floor"
                  value={formData.location}
                  onChange={handleChange}
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-[#1c1c1e]">IP Address</label>
                <input
                  type="text"
                  name="ip_address"
                  className="w-full rounded-xl border border-[#e5e5ea] bg-[#fbfbfc] px-4 py-3 text-[#1c1c1e] focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
                  placeholder="e.g. 192.168.1.15"
                  value={formData.ip_address}
                  onChange={handleChange}
                />
              </div>
            </div>

            {error && (
              <div className="rounded-xl bg-red-50 p-4 text-sm text-red-600 border border-red-100">
                {error}
              </div>
            )}

            <div className="flex justify-end gap-4 pt-4">
              <Link
                href="/devices"
                className="px-6 py-3 rounded-xl font-semibold text-[#8e8e93] hover:bg-[#fbfbfc] transition-all"
              >
                Cancel
              </Link>
              <button
                type="submit"
                disabled={loading}
                className="bg-primary text-white px-8 py-3 rounded-xl font-semibold shadow-lg shadow-primary/30 transition-all hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50"
              >
                {loading ? "Registering..." : "Register Device"}
              </button>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
}
