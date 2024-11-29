import React, { useState, useEffect } from 'react';

function ReviewData({ uploadedFiles, onReviewData }) {
  const [tableConfigs, setTableConfigs] = useState([]);

  useEffect(() => {
    setTableConfigs(
      uploadedFiles.map((file) => ({
        filename: file.filename,
        table_name: file.table_name,
        column_mapping: file.column_mapping,
      }))
    );
  }, [uploadedFiles]);

  const handleInputChange = (event, index, field) => {
    const newTableConfigs = [...tableConfigs];
    if (Array.isArray(field)) {
      newTableConfigs[index][field[0]][field[1]] = event.target.value;
    } else {
      newTableConfigs[index][field] = event.target.value;
    }
    setTableConfigs(newTableConfigs);
  };

  return (
    <div>
      <h2>2. Review Data</h2>
      {tableConfigs.map((config, i) => (
        <div key={config.filename}>
          <h3>File: {config.filename}</h3>
          <label>
            Table name:
            <input
              type="text"
              value={config.table_name}
              onChange={(e) => handleInputChange(e, i, 'table_name')}
            />
          </label>
          <br />
          <table>
            <thead>
              <tr>
                <th>Original Column</th>
                <th>New Name</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(config.column_mapping).map(([orig, renamed]) => (
                <tr key={orig}>
                  <td>{orig}</td>
                  <td>
                    <input
                      type="text"
                      value={renamed}
                      onChange={(e) =>
                        handleInputChange(e, i, ['column_mapping', orig])
                      }
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {uploadedFiles[i]?.sample_data && (
            <>
              <h4>Sample Data (First 5 Rows)</h4>
              <table>
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
            </>
          )}
          <hr />
        </div>
      ))}
      <button onClick={() => onReviewData(tableConfigs)}>Review</button>
    </div>
  );
}

export default ReviewData;