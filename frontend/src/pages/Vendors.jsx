import React, { useState, useEffect } from "react";
import api from "../api/Api";

export default function Vendors({ onSendToVendor }) {
  const [vendors, setVendors] = useState([]);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  useEffect(() => {
    fetchList();
  }, []);

  async function fetchList() {
    const res = await api.get("/vendors/");
    setVendors(res.data);
  }

  async function createVendor() {
    try {
      await api.post("/vendors/", { name, email });
      setName("");
      setEmail("");
      fetchList(); // refresh the vendor list
    } catch (error) {
      if (error.response) {
        // Server responded with a status code outside 2xx
        if (error.response.status === 409) {
          alert("Error: This email already exists!");
        } else {
          alert(
            "Error: " + error.response.data.detail || "Something went wrong"
          );
        }
      } else if (error.request) {
        // Request was made but no response
        alert("Network error: Could not reach the server");
      } else {
        // Something else went wrong
        alert("Error: " + error.message);
      }
    }
  }
  async function send(vendorId) {
    if (onSendToVendor) onSendToVendor(vendorId);
  }

  return (
    <div className="max-w-xl mx-auto p-6 bg-white shadow-md rounded-lg space-y-4">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Vendors</h2>

      {/* Input fields */}
      <div className="flex flex-col md:flex-row gap-3">
        <input
          className="border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400 flex-1"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          className="border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400 flex-1"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
          onClick={createVendor}
        >
          Add
        </button>
      </div>

      {/* Vendor list */}
      <ul className="divide-y divide-gray-200">
        {vendors.map((v) => (
          <li
            key={v.id}
            className="flex justify-between items-center py-2 hover:bg-gray-50 px-2 rounded"
          >
            <span className="text-gray-700 font-medium">
              {v.name} - {v.email}
            </span>
            <button
              className="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600 transition"
              onClick={() => send(v.id)}
            >
              Send
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
