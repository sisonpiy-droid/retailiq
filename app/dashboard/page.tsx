"use client";
import { useEffect, useState } from "react";

export default function DashboardPage() {
  const [user, setUser] = useState<any>(null);
  const [activeTab, setActiveTab] = useState("overview");
  const [metrics, setMetrics] = useState({ revenue: 0, profit: 0 });
  const [question, setQuestion] = useState("");
  const [chatHistory, setChatHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const userData = localStorage.getItem("user");
    if (!userData) {
      window.location.href = "/";
      return;
    }
    const parsedUser = JSON.parse(userData);
    setUser(parsedUser);
    
    // Fetch metrics
    fetch("/api/metrics", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ stores: parsedUser.user.stores })
    })
      .then(res => res.json())
      .then(data => setMetrics(data))
      .catch(err => console.error(err));
  }, []);

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;
    
    setLoading(true);
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, stores: user.user.stores })
      });
      const data = await res.json();
      setChatHistory([{ q: question, ...data }, ...chatHistory]);
      setQuestion("");
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("user");
    window.location.href = "/";
  };

  if (!user) return <div className="p-8">Loading...</div>;

  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="w-64 bg-white border-r p-6">
        <h2 className="text-xl font-bold capitalize text-gray-800 mb-2">{user.username}</h2>
        <p className="text-sm text-gray-600 mb-1"><strong>Role:</strong> {user.user.role}</p>
        <p className="text-sm text-gray-600 mb-6"><strong>Stores:</strong> {user.user.stores.join(", ")}</p>
        
        <hr className="mb-6" />
        
        <nav className="space-y-2">
          <button 
            onClick={() => setActiveTab("overview")}
            className={`w-full text-left px-4 py-2 rounded ${activeTab === "overview" ? "bg-blue-100 text-blue-800 font-semibold" : "text-gray-600 hover:bg-gray-100"}`}
          >
            Overview
          </button>
          <button 
            onClick={() => setActiveTab("ask")}
            className={`w-full text-left px-4 py-2 rounded ${activeTab === "ask" ? "bg-blue-100 text-blue-800 font-semibold" : "text-gray-600 hover:bg-gray-100"}`}
          >
            Ask RetailIQ
          </button>
        </nav>
        
        <div className="mt-auto pt-10">
          <button 
            onClick={handleLogout}
            className="w-full text-left px-4 py-2 text-red-600 hover:bg-red-50 rounded"
          >
            Logout
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-10">
        {activeTab === "overview" && (
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-8">Executive Overview</h1>
            <div className="grid grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-lg shadow border-t-4 border-blue-600">
                <h3 className="text-gray-500 font-semibold mb-2 uppercase text-sm">Revenue</h3>
                <h2 className="text-4xl font-bold text-gray-900">₹ {metrics.revenue.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</h2>
              </div>
              <div className="bg-white p-6 rounded-lg shadow border-t-4 border-blue-600">
                <h3 className="text-gray-500 font-semibold mb-2 uppercase text-sm">Profit</h3>
                <h2 className="text-4xl font-bold text-gray-900">₹ {metrics.profit.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</h2>
              </div>
            </div>
          </div>
        )}

        {activeTab === "ask" && (
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-8">Ask RetailIQ</h1>
            <form onSubmit={handleAsk} className="mb-8">
              <div className="flex gap-2 mb-2">
                <input 
                  type="text" 
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="Ask a question about your stores (e.g., 'What is my total revenue?')"
                  className="flex-1 shadow border rounded py-3 px-4 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button 
                  type="submit"
                  disabled={loading}
                  className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded disabled:opacity-50"
                >
                  {loading ? "Analyzing..." : "Analyze"}
                </button>
              </div>
              <div className="flex flex-col gap-2">
                  <div className="flex gap-2 flex-wrap">
                    <button type="button" onClick={() => setQuestion("Show me the net sales")} className="text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 py-1 px-3 rounded-full border">Show me the net sales</button>
                    <button type="button" onClick={() => setQuestion("What is my total profit?")} className="text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 py-1 px-3 rounded-full border">What is my total profit?</button>
                    <button type="button" onClick={() => setQuestion("Top performing products by revenue")} className="text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 py-1 px-3 rounded-full border">Top performing products by revenue</button>
                    <button type="button" onClick={() => setQuestion("How many total items were sold?")} className="text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 py-1 px-3 rounded-full border">How many total items were sold?</button>
                  </div>
                </div>
            </form>

            <div className="space-y-6">
              {chatHistory.map((chat, idx) => (
                <div key={idx} className="bg-white p-6 rounded-xl shadow">
                  <div className="mb-4">
                    <p className="font-semibold text-gray-800">Q: {chat.q}</p>
                  </div>
                  
                  {chat.intent?.fallback && (
                    <div className="mb-4 p-3 bg-yellow-50 text-yellow-800 rounded border border-yellow-200 text-sm">
                      <p>⚠️ Query intent not clear or metric unsupported. Showing <strong>Revenue</strong> as a fallback.</p>
                    </div>
                  )}
                  
                  <div className="bg-gray-50 p-4 rounded-lg">
                    {chat.result.type === "empty" ? (
                      <p className="text-gray-500">No data found.</p>
                    ) : chat.result.type === "scalar" ? (
                      <h1 className="text-blue-900 text-4xl font-bold">
                        {chat.result.value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                      </h1>
                    ) : (
                      <div className="overflow-x-auto">
                        <table className="min-w-full bg-white">
                          <thead className="bg-gray-100">
                            <tr>
                              {chat.result.columns.map((c: string) => (
                                <th key={c} className="py-2 px-4 border-b text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">{c}</th>
                              ))}
                            </tr>
                          </thead>
                          <tbody>
                            {chat.result.data.map((row: any, i: number) => (
                              <tr key={i} className={i % 2 === 0 ? "bg-gray-50" : "bg-white"}>
                                {chat.result.columns.map((c: string) => (
                                  <td key={c} className="py-2 px-4 border-b text-sm text-gray-700">
                                    {typeof row[c] === 'number' ? row[c].toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : row[c]}
                                  </td>
                                ))}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    )}
                  </div>
                  
                  <div className="mt-4 text-xs text-gray-500 flex gap-4">
                    <span>Intent: {chat.intent?.metric?.toUpperCase()}</span>
                    <span>Route: {chat.intent?.route}</span>
                    <span>Time: {chat.time?.toFixed(3)}s</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
