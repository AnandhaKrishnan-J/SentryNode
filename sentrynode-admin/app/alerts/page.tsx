"use client";

import Sidebar from "@/components/Sidebar";

export default function AlertsPage() {
  return (
    <div className="flex min-h-screen bg-[#fbfbfc]">
      <Sidebar />
      <main className="flex-1 ml-64 p-8">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-[#1c1c1e]">Security Alerts</h1>
          <p className="text-[#8e8e93]">Detailed logs of network incidents and threats</p>
        </header>

        <div className="bg-white rounded-3xl premium-shadow p-12 text-center">
          <div className="inline-block p-4 bg-primary/10 rounded-2xl mb-4">
            <svg className="h-12 w-12 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
          </div>
          <h3 className="text-xl font-bold text-[#1c1c1e] mb-2">Detailed Alert View</h3>
          <p className="text-[#8e8e93] max-w-sm mx-auto">This page will provide deep insights into individual security events and historical data.</p>
          <button className="mt-6 text-primary font-bold hover:underline">Go to Dashboard for recent alerts</button>
        </div>
      </main>
    </div>
  );
}
