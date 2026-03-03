"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";

import Link from "next/link";

export default function RegisterPage() {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const router = useRouter();

    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        if (password !== confirmPassword) {
            setError("Passwords do not match");
            return;
        }

        setLoading(true);

        try {
            await api.register({
                username,
                email,
                password,
            });

            router.push("/login");
        } catch (err: any) {
            setError(err.message || "Registration failed");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex min-h-screen items-center justify-center bg-[#fbfbfc] p-4">
            <div className="w-full max-w-md space-y-8 rounded-3xl bg-white p-10 premium-shadow">
                <div className="text-center">
                    <div className="inline-block rounded-2xl bg-primary/10 p-3 mb-4">
                        <svg
                            className="h-8 w-8 text-primary"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M5 13l4 4L19 7"
                            />
                        </svg>
                    </div>
                    <h2 className="text-3xl font-bold tracking-tight text-[#1c1c1e]">
                        Create Account
                    </h2>
                    <p className="mt-2 text-sm text-[#8e8e93]">
                        Register a new SentryNode admin account
                    </p>
                </div>

                <form className="mt-8 space-y-6" onSubmit={handleRegister}>
                    <div className="space-y-4">
                        <div>
                            <label className="text-sm font-medium text-[#1c1c1e]">
                                Username
                            </label>
                            <input
                                type="text"
                                required
                                className="mt-1 block w-full rounded-xl border border-[#e5e5ea] bg-[#fbfbfc] px-4 py-3 text-[#1c1c1e] focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
                                placeholder="Choose a username"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                            />
                        </div>

                        <div>
                            <label className="text-sm font-medium text-[#1c1c1e]">
                                Email
                            </label>
                            <input
                                type="email"
                                required
                                className="mt-1 block w-full rounded-xl border border-[#e5e5ea] bg-[#fbfbfc] px-4 py-3 text-[#1c1c1e] focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
                                placeholder="Enter your email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                        </div>

                        <div>
                            <label className="text-sm font-medium text-[#1c1c1e]">
                                Password
                            </label>
                            <input
                                type="password"
                                required
                                className="mt-1 block w-full rounded-xl border border-[#e5e5ea] bg-[#fbfbfc] px-4 py-3 text-[#1c1c1e] focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
                                placeholder="••••••••"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </div>

                        <div>
                            <label className="text-sm font-medium text-[#1c1c1e]">
                                Confirm Password
                            </label>
                            <input
                                type="password"
                                required
                                className="mt-1 block w-full rounded-xl border border-[#e5e5ea] bg-[#fbfbfc] px-4 py-3 text-[#1c1c1e] focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
                                placeholder="Re-enter password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                            />
                        </div>
                    </div>

                    {error && (
                        <div className="rounded-xl bg-red-50 p-4 text-sm text-red-600">
                            {error}
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full rounded-xl bg-primary px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-primary/30 transition-all hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50"
                    >
                        {loading ? "Creating account..." : "Register"}
                    </button>
                </form>

                <p className="text-center text-sm text-[#8e8e93]">
                    Already have an account?{" "}
                    <Link
                        href="/login"
                        className="font-medium text-primary hover:underline"
                    >
                        Sign in
                    </Link>
                </p>
            </div>
        </div>
    );
}