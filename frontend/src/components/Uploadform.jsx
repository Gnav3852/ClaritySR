import React, { useState } from "react";
import axios from "axios";

const UploadForm = ({ onProcessed }) => {
  const [file, setFile] = useState(null);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post("http://localhost:8000/process/", formData);
    onProcessed(res.data);
  };

  return (
    <div className="mb-4">
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button
        onClick={handleUpload}
        className="ml-2 px-4 py-1 bg-blue-600 text-white rounded"
      >
        Upload & Analyze
      </button>
    </div>
  );
};

export default UploadForm;
