import React, { useEffect, useState } from "react";
import api from "../api/Api";

export default function RFPDetail({ rfpId }) {
  const [rfp, setRfp] = useState(null);
  const [proposals, setProposals] = useState([]);

  useEffect(() => {
    if (rfpId) load();
  }, [rfpId]);

  async function load() {
    console.log("Loading RFP", rfpId);
    const res = await api.get("/rfps/" + rfpId);
    setRfp(res.data);
    // const p = await api.get("/proposals/for_rfp/" + rfpId);
    // setProposals(p.data);
  }

  async function sendToVendor(vendorId) {
    await api.post(`/vendors/send/${vendorId}/${rfpId}`);
    alert("Sent (may be simulated if SMTP not configured).");
  }

  if (!rfp) return <div>Select an RFP</div>;
  return (
    <div className="max-w-5xl mx-auto p-6 bg-white shadow-lg rounded-xl space-y-6">
      {/* RFP Header */}
      <div>
        <h2 className="text-3xl font-bold mb-2 text-gray-800">{rfp.title}</h2>
        <p className="text-gray-700 whitespace-pre-line">{rfp.description}</p>
      </div>

      {/* Structured Data */}
      <div>
        <h3 className="text-xl font-semibold mb-2 text-gray-800">
          Structured Data
        </h3>
        <pre className="bg-gray-50 p-4 rounded-lg overflow-x-auto text-sm font-mono whitespace-pre-wrap shadow-inner">
          {JSON.stringify(rfp.structured, null, 2)}
        </pre>
      </div>

      {/* Proposals Table */}
      <div>
        <h3 className="text-xl font-semibold mb-3 text-gray-800">Proposals</h3>

        <div className="overflow-x-auto rounded-lg shadow-sm border border-gray-200">
          <table className="min-w-full divide-y divide-gray-200 text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-2 text-left font-medium text-gray-700">
                  Vendor
                </th>
                <th className="px-4 py-2 text-center font-medium text-gray-700">
                  Score
                </th>
                <th className="px-4 py-2 text-left font-medium text-gray-700">
                  Proposal Data
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {proposals.map((p) => (
                <tr key={p.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-4 py-2">{p.vendor_id}</td>
                  <td className="px-4 py-2 text-center font-semibold">
                    {p.score}
                  </td>
                  <td className="px-4 py-2">
                    <pre className="bg-gray-50 p-2 rounded-lg font-mono whitespace-pre-wrap break-words shadow-inner text-xs md:text-sm">
                      {JSON.stringify(p.proposal, null, 2)}
                    </pre>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <p className="text-gray-500 text-sm mt-2">
        To send RFP to a vendor: open Vendors and click{" "}
        <span className="font-semibold">Send</span>.
      </p>
    </div>
  );
}
