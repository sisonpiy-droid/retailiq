"use client";
import { useState } from "react";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username })
    });
    
    if (res.ok) {
      const data = await res.json();
      localStorage.setItem("user", JSON.stringify(data));
      window.location.href = "/dashboard";
    } else {
      setError("User not found.");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
      <h1 className="text-4xl font-bold mb-8 text-blue-900">RetailIQ Enterprise</h1>
      <form onSubmit={handleLogin} className="bg-white p-8 rounded-lg shadow-md w-96 border-t-4 border-blue-600">
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2">Username (e.g., ana, ravi, meera, hq)</label>
          <input 
            type="text" 
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        {error && <p className="text-red-500 text-xs italic mb-4">{error}</p>}
        <button 
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded w-full"
        >
          Login
        </button>
      </form>
    </div>
  );
}
