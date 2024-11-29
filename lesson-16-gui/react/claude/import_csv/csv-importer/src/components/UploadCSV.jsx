import React, { useState } from 'react';
import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_BASE_URL;

function UploadCSV({ datasetName, onDatasetNameChange, onCreateDataset, onUploadCSV }) {
  const [selectedFiles, setSelectedFiles] = useState(null);
  const [error, setError] = useState('');
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (event) => {
    setError('');
    setSelectedFiles(event.target.files);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    if (!datasetName?.trim()) {
      setError('Please enter a dataset name first');
      return;
    }

    if (!selectedFiles?.length) {
      setError('Please select files to upload');
      return;
    }

    setUploading(true);
    setError('');

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

      // Log the response to debug
      console.log('Upload response:', response.data);

      // Validate and transform the response data
      const uploadedFiles = response.data.map(file => ({
        filename: file.filename,
        table_name: file.table_name || file.filename.replace('.csv', '').toLowerCase(),
        column_mapping: Object.fromEntries(
          Object.keys(file.sample_data?.[0] || {}).map(col => [
            col,
            col.toLowerCase().replace(/\s+/g, '_')
          ])
        ),
        sample_data: file.sample_data || []
      }));

      console.log('Transformed upload data:', uploadedFiles);
      onUploadCSV(uploadedFiles);
      
      // Clear the file input
      setSelectedFiles(null);
      event.target.reset();

    } catch (err) {
      console.error('Error uploading CSV:', err);
      setError(err.response?.data?.detail || 'Error uploading files. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="mb-4">
      <h2>1. Upload CSV</h2>
      
      <div className="mb-3">
        <label className="form-label">Dataset Name:</label>
        <input
          type="text"
          className="form-control"
          placeholder="Enter dataset name"
          value={datasetName}
          onChange={(e) => onDatasetNameChange(e.target.value)}
        />
      </div>

      <button 
        className="btn btn-secondary mb-3"
        onClick={onCreateDataset}
        disabled={!datasetName?.trim()}
      >
        Create Dataset
      </button>

      <form onSubmit={handleSubmit} className="mt-3">
        <div className="mb-3">
          <input 
            type="file" 
            className="form-control" 
            multiple 
            accept=".csv" 
            onChange={handleFileChange}
            disabled={!datasetName?.trim()}
          />
        </div>
        
        <button 
          type="submit" 
          className="btn btn-primary"
          disabled={!selectedFiles?.length || uploading}
        >
          {uploading ? 'Uploading...' : 'Upload'}
        </button>

        {error && (
          <div className="alert alert-danger mt-3" role="alert">
            {error}
          </div>
        )}
      </form>

      {selectedFiles && selectedFiles.length > 0 && (
        <div className="mt-3">
          <h4>Selected Files:</h4>
          <ul className="list-group">
            {Array.from(selectedFiles).map((file, index) => (
              <li key={index} className="list-group-item">
                {file.name}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default UploadCSV;