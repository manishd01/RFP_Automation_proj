import React, { useState } from "react";
import api from "../api/Api";

export default function CreateRFP() {
  const [title, setTitle] = useState("");
  const [desc, setDesc] = useState("");
  const [created, setCreated] = useState(null);

  async function submit() {
    console.log("Submitting", title, desc);
    try {
      const res = await api.post("/rfps/", { title, description: desc });

      setCreated(res.data);
      setTitle("");
      setDesc("");
    } catch (e) {
      alert("Error: " + e);
    }
  }

  return (
    <div className="max-w-lg mx-auto p-6 bg-white shadow-lg rounded-xl space-y-4">
      <h2 className="text-2xl font-bold text-gray-800">Create RFP</h2>

      {/* Title Input */}
      <input
        className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      {/* Description Textarea */}
      <textarea
        className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400 resize-none h-32"
        placeholder="Description"
        value={desc}
        onChange={(e) => setDesc(e.target.value)}
      />

      {/* Submit Button */}
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
        onClick={submit}
      >
        Create
      </button>

      {/* Created RFP Display */}
      {created && (
        <div className="mt-4 p-4 bg-gray-50 rounded shadow-inner">
          <h4 className="font-semibold text-gray-700 mb-2">RFP Created</h4>
          <pre className="text-sm font-mono text-gray-800 whitespace-pre-wrap break-words">
            {JSON.stringify(created, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
