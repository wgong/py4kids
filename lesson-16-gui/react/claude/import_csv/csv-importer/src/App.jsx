import React, { useState } from 'react';
import axios from 'axios';
import UploadCSV from './components/UploadCSV';
import ReviewData from './components/ReviewData';
import CreateTables from './components/CreateTables';
import LoadData from './components/LoadData';

const BASE_URL = process.env.REACT_APP_API_BASE_URL;

function App() {
  const [datasetName, setDatasetName] = useState('');
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [tableConfigs, setTableConfigs] = useState([]);
  const [generatedDDL, setGeneratedDDL] = useState([]);

  const handleCreateDataset = async () => {
    try {
      await axios.post(`${BASE_URL}/api/create-dataset/${datasetName}`);
    } catch (err) {
      console.error('Error creating dataset:', err);
    }
  };
  
  const handleUploadCSV = async (uploadedFiles) => {
    setUploadedFiles(uploadedFiles);
  };
  
  const handleReviewData = (reviewedConfigs) => {
    setTableConfigs(reviewedConfigs);
  };
  
  const handleGenerateDDL = (ddl) => {
    // Save the generated DDL to the component's state
    setGeneratedDDL(ddl);
    
    // Optionally, you can perform additional actions like showing a success message
    alert('DDL generated successfully!');
  };
  
  const handleCreateTables = async () => {
    try {
      // Make an API call to create tables
      await axios.post(`${BASE_URL}/api/create-tables/${datasetName}`);
      
      // Handle the success case, e.g., show a success message
      alert('Tables created successfully!');
    } catch (err) {
      // Handle the error case, e.g., show an error message
      console.error('Error creating tables:', err);
      alert('Error creating tables. Please check the console for details.');
    }
  };
  
  const handleLoadData = async (loadedTables) => {
    try {
      // Make an API call to load data into tables
      const response = await axios.post(
        `${BASE_URL}/api/load-data/${datasetName}`,
        tableConfigs
      );
      
      // Handle the success case, e.g., show a success message with loaded table names
      const loadedTableNames = response.data.loaded_tables.join(', ');
      alert(`Data loaded successfully into tables: ${loadedTableNames}`);
    } catch (err) {
      // Handle the error case, e.g., show an error message
      console.error('Error loading data:', err);
      alert('Error loading data. Please check the console for details.');
    }
  };

  return (
    <div className="container">
      <h1>CSV Import Tool</h1>

      <UploadCSV 
        datasetName={datasetName}
        onDatasetNameChange={setDatasetName}
        onCreateDataset={handleCreateDataset}
        onUploadCSV={handleUploadCSV}
      />

      <ReviewData
        uploadedFiles={uploadedFiles}
        onReviewData={handleReviewData} 
      />
      
      <CreateTables
        datasetName={datasetName}
        tableConfigs={tableConfigs}
        onGenerateDDL={handleGenerateDDL}
        onCreateTables={handleCreateTables}
      />
      
      <LoadData 
        datasetName={datasetName}
        tableConfigs={tableConfigs}
        onLoadData={handleLoadData}
      />
      
    </div>
  );
}

export default App;