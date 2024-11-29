import React, { useState, useEffect } from 'react';

function ReviewData({ uploadedFiles, onReviewData }) {
  const [tableConfigs, setTableConfigs] = useState([]);

  useEffect(() => {
    // Log the incoming data to debug
    console.log('uploadedFiles received:', uploadedFiles);

    if (!uploadedFiles?.length) {
      console.warn('No uploaded files received');
      return;
    }

    // Transform the data into the correct structure
    const configs = uploadedFiles.map((file) => {
      // Convert the column_mapping object into an array of mappings
      const columnMappings = Object.entries(file.column_mapping || {}).map(([source, target]) => ({
        source: source,
        target: target,
        data_type: 'TEXT'  // Default to TEXT, adjust as needed
      }));

      return {
        filename: file.filename,
        table_name: file.table_name || file.filename.replace('.csv', '').toLowerCase(),
        column_mapping: columnMappings
      };
    });

    console.log('Transformed tableConfigs:', configs);
    setTableConfigs(configs);
  }, [uploadedFiles]);

  const handleInputChange = (event, index, field) => {
    const newTableConfigs = [...tableConfigs];
    
    if (Array.isArray(field)) {
      // Handle column mapping changes
      const [fieldType, columnIndex] = field;
      if (fieldType === 'column_mapping') {
        const mapping = {...newTableConfigs[index].column_mapping[columnIndex]};
        mapping.target = event.target.value;
        newTableConfigs[index].column_mapping[columnIndex] = mapping;
      }
    } else {
      // Handle table name changes
      newTableConfigs[index][field] = event.target.value;
    }
    
    setTableConfigs(newTableConfigs);
  };

  const handleReview = () => {
    // Validate the data before sending
    if (!tableConfigs?.length) {
      alert('No table configurations available');
      return;
    }

    // Log the final data being sent
    console.log('Sending tableConfigs:', tableConfigs);
    onReviewData(tableConfigs);
  };

  if (!uploadedFiles?.length) {
    return <div>No files uploaded yet.</div>;
  }

  return (
    <div>
      <h2>2. Review Data</h2>
      {tableConfigs.map((config, i) => (
        <div key={config.filename} className="mb-4">
          <h3>File: {config.filename}</h3>
          <div className="mb-3">
            <label className="form-label">
              Table name:
              <input
                type="text"
                className="form-control"
                value={config.table_name}
                onChange={(e) => handleInputChange(e, i, 'table_name')}
              />
            </label>
          </div>
          
          <table className="table table-bordered">
            <thead>
              <tr>
                <th>Original Column</th>
                <th>New Name</th>
                <th>Data Type</th>
              </tr>
            </thead>
            <tbody>
              {config.column_mapping.map((mapping, colIndex) => (
                <tr key={mapping.source}>
                  <td>{mapping.source}</td>
                  <td>
                    <input
                      type="text"
                      className="form-control"
                      value={mapping.target}
                      onChange={(e) => handleInputChange(e, i, ['column_mapping', colIndex])}
                    />
                  </td>
                  <td>
                    <select
                      className="form-select"
                      value={mapping.data_type}
                      onChange={(e) => {
                        const newConfigs = [...tableConfigs];
                        newConfigs[i].column_mapping[colIndex].data_type = e.target.value;
                        setTableConfigs(newConfigs);
                      }}
                    >
                      <option value="TEXT">TEXT</option>
                      <option value="INTEGER">INTEGER</option>
                      <option value="REAL">REAL</option>
                      <option value="DATE">DATE</option>
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {uploadedFiles[i]?.sample_data && (
            <div className="mt-3">
              <h4>Sample Data (First 5 Rows)</h4>
              <div className="table-responsive">
                <table className="table table-sm table-bordered">
                  <thead>
                    <tr>
                      {Object.keys(uploadedFiles[i].sample_data[0] || {}).map((col) => (
                        <th key={col}>{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {uploadedFiles[i].sample_data.slice(0, 5).map((row, rowIndex) => (
                      <tr key={rowIndex}>
                        {Object.values(row).map((cell, cellIndex) => (
                          <td key={cellIndex}>{cell}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
          <hr />
        </div>
      ))}
      <button 
        className="btn btn-primary"
        onClick={handleReview}
        disabled={!tableConfigs.length}
      >
        Review
      </button>
    </div>
  );
}

export default ReviewData;