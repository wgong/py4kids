# FastAPI application# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import List, Dict
import pandas as pd
import sqlite3
import os
import re
from pathlib import Path
from datetime import datetime
import json
from pydantic import BaseModel

class ColumnMapping(BaseModel):
    source: str
    target: str
    data_type: str

class TableConfig(BaseModel):
    filename: str
    table_name: str
    column_mapping: List[ColumnMapping]

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import re

def snake_case(s: str) -> str:
    """
    Convert string to snake_case.
    
    Examples:
        >>> snake_case('price_(GBP)')
        'price_gbp'
        >>> snake_case('HelloWorld')
        'hello_world'
        >>> snake_case('First Name!')
        'first_name'
        >>> snake_case('API_URL')
        'api_url'
    """
    # First convert camelCase to snake_case
    s = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s)
    # Convert UPPERCASE to lowercase with underscore
    s = re.sub('([A-Z])([A-Z][a-z])', r'\1_\2', s)
    # Replace all non-alphanumeric characters with underscore
    s = re.sub(r'[^a-zA-Z0-9]', '_', s)
    # Convert to lowercase
    s = s.lower()
    # Replace multiple underscores with single underscore
    s = re.sub('_+', '_', s)
    # Remove leading and trailing underscores
    s = s.strip('_')
    return s


def create_sqlite_ddl(df: pd.DataFrame, table_name: str, file_name: str, column_mapping: list) -> str:
    """Generate SQLite DDL with comments."""
    type_map = {
        'int64': 'INTEGER',
        'float64': 'REAL',
        'object': 'TEXT',
        'datetime64[ns]': 'TEXT',
        'bool': 'INTEGER'
    }
    
    ddl = [f"-- Original CSV file: {file_name}"]
    ddl.append(f"CREATE TABLE IF NOT EXISTS {table_name} (")
    
    columns = []
    for orig_col, snake_col, sql_type in column_mapping:
        columns.append(f"    {snake_col[1]} {sql_type[1]}  -- Original column: {orig_col[1]}")
    
    ddl.append("\n\t,".join(columns))
    ddl.append(");")
    
    return "\n".join(ddl)

@app.post("/api/create-dataset/{dataset_name}")
async def create_dataset(dataset_name: str):
    try:
        Path(f"db/{dataset_name}").mkdir(parents=True, exist_ok=True)
        return {"message": f"Created dataset directory: db/{dataset_name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload-csv/{dataset_name}")
async def upload_csv(dataset_name: str, files: List[UploadFile] = File(...)):
    try:
        uploaded_files = []
        for file in files:
            # Save uploaded file
            save_path = f"db/{dataset_name}/{file.filename}"
            content = await file.read()
            with open(save_path, "wb") as f:
                f.write(content)
            
            # Read and analyze DataFrame
            df = pd.read_csv(save_path)
            table_name = snake_case(os.path.splitext(file.filename)[0])
            column_mapping = {col: snake_case(col) for col in df.columns}
            
            stats = {
                "filename": file.filename,
                "rows": len(df),
                "columns": len(df.columns),
                "missing_values": int(df.isnull().sum().sum()),
                "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB",
                "table_name": table_name,
                "column_mapping": column_mapping,
                "sample_data": df.head().to_dict(orient='records')
            }
            print(f"stats = \n{stats}")
            uploaded_files.append(stats)
        
        return uploaded_files
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-ddl/{dataset_name}")
async def generate_ddl(dataset_name: str, table_configs: List[TableConfig]):
    try:
        print(f"table_configs:\n{table_configs}")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        all_ddl = [
            f"-- Generated on: {timestamp}",
            f"-- Dataset: {dataset_name}",
            ""
        ]
        
        for config in table_configs:
            df = pd.read_csv(f"db/{dataset_name}/{config.filename}")
            ddl = create_sqlite_ddl(
                df,
                config.table_name,
                config.filename,
                config.column_mapping
            )
            all_ddl.append(ddl)
            all_ddl.append("")
        
        ddl_content = "\n".join(all_ddl)
        ddl_path = f"db/{dataset_name}/{dataset_name}_ddl.sql"
        
        with open(ddl_path, "w", encoding='utf-8') as f:
            f.write(ddl_content)
        
        return {"ddl": ddl_content}
    except Exception as e:
        print(f"generate_ddl error:\n{str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/create-tables/{dataset_name}")
async def create_tables(dataset_name: str):
    try:
        ddl_path = f"db/{dataset_name}/{dataset_name}_ddl.sql"
        db_path = f"db/{dataset_name}/{dataset_name}.sqlite3"
        
        with open(ddl_path, 'r') as f:
            ddl_content = f.read()
        
        conn = sqlite3.connect(db_path)
        try:
            for ddl in ddl_content.split(';'):
                if ddl.strip() and not ddl.strip().startswith('--'):
                    conn.execute(ddl)
            conn.commit()
            return {"message": "Tables created successfully"}
        finally:
            conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/load-data/{dataset_name}")
async def load_data(dataset_name: str, table_configs: List[Dict]):
    try:
        db_path = f"db/{dataset_name}/{dataset_name}.sqlite3"
        loaded_tables = []
        
        conn = sqlite3.connect(db_path)
        try:
            for config in table_configs:
                df = pd.read_csv(f"db/{dataset_name}/{config['filename']}")
                df_renamed = df.rename(columns=config['column_mapping'])
                df_renamed.to_sql(config['table_name'], conn, if_exists='replace', index=False)
                loaded_tables.append(config['table_name'])
            
            return {"loaded_tables": loaded_tables}
        finally:
            conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download-ddl/{dataset_name}")
async def download_ddl(dataset_name: str):
    ddl_path = f"db/{dataset_name}/{dataset_name}_ddl.sql"
    if os.path.exists(ddl_path):
        return FileResponse(ddl_path, filename=f"{dataset_name}_ddl.sql", media_type="application/sql")
    raise HTTPException(status_code=404, detail="DDL file not found")

@app.get("/api/download-db/{dataset_name}")
async def download_db(dataset_name: str):
    db_path = f"db/{dataset_name}/{dataset_name}.sqlite3"
    if os.path.exists(db_path):
        return FileResponse(db_path, filename=f"{dataset_name}.sqlite3", media_type="application/x-sqlite3")
    raise HTTPException(status_code=404, detail="Database file not found")


# Requirements (requirements.txt):
# fastapi==0.68.1
# uvicorn==0.15.0
# python-multipart==0.0.5
# pandas==1.3.3
# SQLAlchemy==1.4.23