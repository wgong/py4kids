from utils import *

st.set_page_config(layout="wide")
st.subheader(f"{STR_MENU_IMPORT_DATA} 📥")

def snake_case(s):
    """Convert string to snake_case."""
    # Replace spaces and special chars with underscore
    s = re.sub(r'[^a-zA-Z0-9]', '_', s)
    # Convert camelCase to snake_case
    s = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s)
    # Convert to lowercase and remove multiple underscores
    return re.sub('_+', '_', s.lower()).strip('_')

def validate_dataframe(df, file_name):
    """Validate DataFrame and show basic statistics."""
    try:
        stats = {
            "rows": len(df),
            "columns": len(df.columns),
            "missing_values": df.isnull().sum().sum(),
            "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB"
        }
        
        with st.expander(f"📊 Data Quality Stats - {file_name}"):
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Rows", stats["rows"])
            col2.metric("Columns", stats["columns"])
            col3.metric("Missing Values", stats["missing_values"])
            col4.metric("Memory", stats["memory_usage"])
            
            if stats["missing_values"] > 0:
                st.warning("⚠️ Found missing values in data")
        
        return True
    except Exception as e:
        st.error(f"Error validating data for {file_name}: {str(e)}")
        return False

def add_download_buttons(dataset_name):
    """Add download buttons for DDL and SQLite database."""
    try:
        col1, col2 = st.columns(2)
        
        # Download DDL
        ddl_path = f"db/{dataset_name}/{dataset_name}_ddl.sql"
        if os.path.exists(ddl_path):
            with open(ddl_path, 'r') as f:
                ddl_content = f.read()
            col1.download_button(
                "📥 Download DDL",
                ddl_content,
                file_name=f"{dataset_name}_ddl.sql",
                mime="text/plain"
            )
        
        # Download SQLite DB
        db_path = f"db/{dataset_name}/{dataset_name}.sqlite3"
        if os.path.exists(db_path):
            with open(db_path, 'rb') as f:
                db_content = f.read()
            col2.download_button(
                "📥 Download SQLite DB",
                db_content,
                file_name=f"{dataset_name}.sqlite3",
                mime="application/x-sqlite3"
            )
    except Exception as e:
        st.error(f"Error setting up download buttons: {str(e)}")

def create_sqlite_ddl(df, table_name, file_name, column_mapping):
    """Generate SQLite DDL with comments for original filename and column names."""
    try:
        type_map = {
            'int64': 'INTEGER',
            'float64': 'REAL',
            'object': 'TEXT',
            'datetime64[ns]': 'TEXT',  # Store all timestamps as TEXT
            'bool': 'INTEGER'
        }
        
        # Add table comment with original filename
        ddl = [f"-- Original CSV file: {file_name}"]
        ddl.append(f"CREATE TABLE IF NOT EXISTS {table_name} (")
        
        # Add columns with comments showing original names
        columns = []
        for orig_col, snake_col in column_mapping.items():
            sql_type = type_map.get(str(df[orig_col].dtype), 'TEXT')
            columns.append(f"    {snake_col} {sql_type}  -- Original column: {orig_col}")
        
        ddl.append(",\n".join(columns))
        ddl.append(");")
        
        return "\n".join(ddl)
    except Exception as e:
        st.error(f"Error generating DDL for {table_name}: {str(e)}")
        return None

def csv_import_tool():
    st.header("CSV Import Tool")
    
    # Initialize session state
    if 'dataframes' not in st.session_state:
        st.session_state.dataframes = {}
    if 'table_names' not in st.session_state:
        st.session_state.table_names = {}
    if 'column_names' not in st.session_state:
        st.session_state.column_names = {}
    
    # Section 1: Upload CSV
    st.subheader("1. Upload CSV")

    c1, _, c2 = st.columns([3,1,6])
    with c1:
        dataset_name = st.text_input("Dataset Name")
    
        # Early return if no dataset name
        if not dataset_name:
            st.error("Please enter a dataset name")
            return
    
        if st.button("Create Dataset"):
            try:
                # Create directories
                Path(f"db/{dataset_name}").mkdir(eparents=True, exist_ok=True)
                st.success(f"Created dataset directory: db/{dataset_name}")
            except Exception as e:
                st.error(f"Error creating dataset directory: {str(e)}")
                return
    
    with c2:
        uploaded_files = st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)
        if uploaded_files:
            for file in uploaded_files:
                try:
                    # Save file
                    save_path = f"db/{dataset_name}/{file.name}"
                    with open(save_path, "wb") as f:
                        f.write(file.getvalue())
                    
                    # Read DataFrame
                    df = pd.read_csv(save_path)
                    
                    # Validate DataFrame
                    if not validate_dataframe(df, file.name):
                        st.warning(f"invalid data file: {file.name}")
                        continue
                    
                    table_name = snake_case(os.path.splitext(file.name)[0])
                    st.session_state.dataframes[file.name] = df
                    st.session_state.table_names[file.name] = table_name
                    st.session_state.column_names[file.name] = {col: snake_case(col) for col in df.columns}
                
                except Exception as e:
                    st.error(f"Error processing file {file.name}: {str(e)}")
                    continue
    
    # Section 2: Review Data
    if st.session_state.dataframes:
        st.subheader("2. Review Data")
        
        for file_name, df in st.session_state.dataframes.items():
            st.subheader(f"File: '{file_name}' ")
            
            # Table name input
            new_table_name = st.text_input(
                f"Table name:",
                value=st.session_state.table_names[file_name],
                key=f"table_{file_name}"
            )
            st.session_state.table_names[file_name] = new_table_name
            
            # Column name inputs
            st.write("Column names:")
            cols = st.session_state.column_names[file_name]
            for orig_col in df.columns:
                new_col = st.text_input(
                    f"Rename column: {orig_col}",
                    value=cols[orig_col],
                    key=f"col_{file_name}_{orig_col}"
                )
                cols[orig_col] = new_col
            
            # Show sample data
            st.write("Sample data (first 5 rows):")
            st.dataframe(df.head())
    
    # Section 3: Create Tables
    if st.session_state.dataframes:
        st.subheader("3. Create Tables")
        
        # Generate DDL with timestamp and subheader
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        all_ddl = [
            f"-- Generated on: {timestamp}",
            f"-- Dataset: {dataset_name}",
            ""
        ]
        
        for file_name, df in st.session_state.dataframes.items():
            table_name = st.session_state.table_names[file_name]
            ddl = create_sqlite_ddl(
                df, 
                table_name, 
                file_name, 
                st.session_state.column_names[file_name]
            )
            if ddl:
                all_ddl.append(ddl)
                all_ddl.append("")  # Empty line between tables
        
        ddl_content = "\n".join(all_ddl)
        st.code(ddl_content, language="sql")

        try:
            # Save DDL to file
            ddl_path = f"db/{dataset_name}/{dataset_name}_ddl.sql"
            with open(ddl_path, "w", encoding='utf-8') as f:
                f.write(ddl_content)
            st.success(f"DDL saved to: '{ddl_path}'")
        except Exception as e:
            st.error(f"Error saving DDL file: {str(e)}")
        
        if st.button("Create Tables"):
            db_path = f"db/{dataset_name}/{dataset_name}.sqlite3"
            conn = None
            try:
                conn = sqlite3.connect(db_path)
                for ddl in all_ddl:
                    if ddl.strip() and not ddl.strip().startswith("--"):
                        conn.executescript(ddl)
                conn.commit()
                st.success("Tables created successfully!")
            except Exception as e:
                st.error(f"Error creating tables: {str(e)}")
            finally:
                if conn:
                    conn.close()
        
        # Add download buttons after tables are created
        add_download_buttons(dataset_name)
    
    # Section 4: Load Data
    if st.session_state.dataframes:
        st.subheader("4. Load Data")
        
        if st.button("Load Data"):
            loaded_tables = []
            db_path = f"db/{dataset_name}/{dataset_name}.sqlite3"
            conn = None
            try:
                conn = sqlite3.connect(db_path)
                for file_name, df in st.session_state.dataframes.items():
                    table_name = st.session_state.table_names[file_name]
                    try:
                        # Rename columns before loading
                        df_renamed = df.rename(columns=st.session_state.column_names[file_name])
                        df_renamed.to_sql(table_name, conn, if_exists='replace', index=False)
                        loaded_tables.append(table_name)
                    except Exception as e:
                        st.error(f"Error loading table {table_name}: {str(e)}")

                if loaded_tables:
                    loaded_tables = [f"<li>{i}</li>" for i in sorted(loaded_tables)]
                    table_list = "\n".join(loaded_tables)
                    st.success(f"Data loaded successfully:")
                    st.markdown(f"""
                        {table_list}
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error connecting to database: {str(e)}")
            finally:
                if conn:
                    conn.close()

def main():
    csv_import_tool()

if __name__ == "__main__":
    main()