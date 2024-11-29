import React, { useState } from 'react';
import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_BASE_URL;

function UploadCSV({ datasetName, onDatasetNameChange, onCreateDataset, onUploadCSV }) {
  const [selectedFiles, setSelectedFiles] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFiles(event.target.files);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedFiles) return;

    const formData = new FormData();
    for (let i = 0; i < selectedFiles.length; i++) {
      formData.append('files', selectedFiles[i]);
    }

    try {
      const response = await axios.post(
        `${BASE_URL}/api/upload-csv/${datasetName}`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      onUploadCSV(response.data);
    } catch (err) {
      console.error('Error uploading CSV:', err);
    }
  };

  return (
    <div>
      <h2>1. Upload CSV</h2>
      <input
        type="text"
        placeholder="Enter dataset name"
        value={datasetName}
        onChange={(e) => onDatasetNameChange(e.target.value)}
      />
      <button onClick={onCreateDataset}>Create Dataset</button>
      <br />
      <form onSubmit={handleSubmit}>
        <input type="file" multiple accept=".csv" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
    </div>
  );
}

export default UploadCSV;