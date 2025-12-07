import React, { useState } from "react";
import CreateRFP from "./pages/CreateRFP";
import RFPList from "./pages/RFPList";
import RFPDetail from "./pages/RFPDetail";
import Vendors from "./pages/Vendors";
import "./app.css";
import api from "./api/Api";

export default function App() {
  const [selected, setSelected] = useState(null);
  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">
        AI-Powered RFP (FastAPI + React)
      </h1>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* Left Column: Create RFP + Vendors */}
        <div className="flex-1 space-y-6">
          <div className="bg-white p-6 rounded-xl shadow-md">
            <CreateRFP />
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md">
            <Vendors
              onSendToVendor={async (vid) => {
                if (!selected) return;

                try {
                  await api.post(`/vendors/send/${vid}/${selected}`);
                  alert("Sent to vendor!");
                } catch (err) {
                  console.error(err);
                  alert("Failed to send");
                }
              }}
            />
          </div>
        </div>

        {/* Right Column: RFP List + Details */}
        <div className="flex-1 space-y-6">
          <div className="bg-white p-6 rounded-xl shadow-md">
            <RFPList onSelect={setSelected} />
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md">
            <RFPDetail rfpId={selected} />
          </div>
        </div>
      </div>
    </div>
  );
}

//npm start
