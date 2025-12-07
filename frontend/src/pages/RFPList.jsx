import React, { useEffect, useState } from "react";
import api from "../api/Api";

export default function RFPList({ onSelect }) {
  const [rfps, setRfps] = useState([]);

  useEffect(() => {
    fetch();
  }, []);

  async function fetch() {
    const res = await api.get("/rfps");

    setRfps(res.data);
  }

  return (
    <div className="max-w-md mx-auto p-6 bg-white shadow-lg rounded-xl space-y-4">
      <h2 className="text-2xl font-bold text-gray-800 mb-2">RFPs</h2>

      <ul className="space-y-2">
        {rfps.map((r) => (
          <li key={r.id}>
            <button
              className="w-full text-left px-4 py-2 bg-gray-100 rounded hover:bg-blue-100 transition font-medium text-gray-700"
              onClick={() => onSelect(r.id)}
            >
              {r.title}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
