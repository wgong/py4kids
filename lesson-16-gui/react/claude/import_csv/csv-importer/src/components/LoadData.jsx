import React from 'react';
import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_BASE_URL;

function LoadData({ datasetName, tableConfigs, onLoadData }) {

  const handleLoadData = async () => {
    try {
      const response = await axios.post(
        `${BASE_URL}/api/load-data/${datasetName}`,
        tableConfigs
      );
      onLoadData(response.data.loaded_tables);
    } catch (err) {
      console.error('Error loading data:', err);
    }
  };
  
  const handleDownloadDB = async () => {
    try {
      const response = await axios.get(
        `${BASE_URL}/api/download-db/${datasetName}`,
        { responseType: 'blob' }
      );
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${datasetName}.sqlite3`);
      document.body.appendChild(link);
      link.click();
    } catch (err) {
      console.error('Error downloading DB:', err);
    }
  };

  return (
    <div>
      <h2>4. Load Data</h2>
      <div>
        <button className="btn btn-primary mr-2 button-spacing" onClick={handleLoadData}>Load Data</button>
        <button className="btn btn-secondary button-spacing" onClick={handleDownloadDB}>Download SQLite DB</button>

      </div>
    </div>
  );
}

export default LoadData;