import React, { useState } from "react";
import UploadForm from "./components/UploadForm";
import MapViewer from "./components/MapViewer";
import ReportViewer from "./components/ReportViewer";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <h1 className="text-3xl font-bold mb-4">Flood Damage Analysis</h1>
      <UploadForm onProcessed={setResult} />
      {result && (
        <>
          <MapViewer result={result} />
          <ReportViewer report={result.report} />
        </>
      )}
    </div>
  );
}

export default App;
