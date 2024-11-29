import React, { useState } from 'react';
import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_BASE_URL;

function CreateTables({ datasetName, tableConfigs, onGenerateDDL, onCreateTables }) {
  const [ddl, setDDL] = useState('');
  
  console.log('tableConfigs:', tableConfigs);

  const handleGenerateDDL = async () => {
    try {
      const response = await axios.post(
        `${BASE_URL}/api/generate-ddl/${datasetName}`, 
        tableConfigs
      );
      setDDL(response.data.ddl);
      onGenerateDDL(response.data.ddl);
    } catch (err) {
      console.error('Error generating DDL:', err);
    }
  };


  const handleDownloadDDL = () => {
    const element = document.createElement('a');
    const file = new Blob([ddl], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = `${datasetName}_ddl.sql`;
    document.body.appendChild(element); 
    element.click();
  };
  
  const handleCreateTables = async () => {
    try {
      await axios.post(`${BASE_URL}/api/create-tables/${datasetName}`);
      onCreateTables();
    } catch (err) {
      console.error('Error creating tables:', err);
    } 
  };

  return (
    <div>
      <h2>3. Create Tables</h2>
      <pre>{ddl}</pre>
      <div className="mb-3">
        <button className="btn btn-info mr-2 button-spacing" onClick={handleGenerateDDL}>Generate DDL</button>
        <button className="btn btn-secondary button-spacing" onClick={handleDownloadDDL}>Download DDL</button>
      </div>

      <div className="mb-3">
        <button className="btn btn-primary button-spacing" onClick={handleCreateTables}>Create Tables</button>
      </div>
    </div>
  );
}

export default CreateTables;