from utils import *

st.set_page_config(layout="wide")
st.subheader(f"Import Excel 📊")

def snake_case(s):
    """Convert string to snake_case."""
    s = re.sub(r'[^a-zA-Z0-9]', '_', s)
    s = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s)
    return re.sub('_+', '_', s.lower()).strip('_')

def validate_dataframe(df, sheet_name):
    """Validate DataFrame and show basic statistics."""
    try:
        stats = {
            "rows": len(df),
            "columns": len(df.columns),
            "missing_values": df.isnull().sum().sum(),
            "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB"
        }
        
        with st.expander(f"📊 Data Quality Stats - {sheet_name}"):
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Rows", stats["rows"])
            col2.metric("Columns", stats["columns"])
            col3.metric("Missing Values", stats["missing_values"])
            col4.metric("Memory", stats["memory_usage"])
            
            if stats["missing_values"] > 0:
                st.warning(f"⚠️ Found missing values in sheet '{sheet_name}'")
        
        return True
    except Exception as e:
        st.error(f"Error validating data for sheet '{sheet_name}': {str(e)}")
        return False

def add_download_buttons(dataset_name):
    """Add download buttons for DDL and SQLite database."""
    try:
        col1, col2 = st.columns(2)
        sub_folder = f"db/{dataset_name}"
        ddl_path = f"{sub_folder}/{dataset_name}_ddl.sql"
        if os.path.exists(ddl_path):
            with open(ddl_path, 'r') as f:
                ddl_content = f.read()
            col1.download_button(
                "📥 Download DDL",
                ddl_content,
                file_name=f"{dataset_name}_ddl.sql",
                mime="text/plain"
            )
        
        db_path = f"{sub_folder}/{dataset_name}.sqlite3"
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

def create_sqlite_ddl(df, table_name, sheet_name, column_mapping, ignored_columns):
    """Generate SQLite DDL with comments for original sheet name and column names."""
    try:
        type_map = {
            'int64': 'INTEGER',
            'float64': 'REAL',
            'object': 'TEXT',
            'datetime64[ns]': 'TEXT',
            'bool': 'INTEGER'
        }
        
        ddl = [f"-- Original Excel sheet: {sheet_name}"]
        ddl.append(f"CREATE TABLE IF NOT EXISTS {table_name} (")
        
        columns = []
        for orig_col, snake_col in column_mapping.items():
            if orig_col not in ignored_columns:
                sql_type = type_map.get(str(df[orig_col].dtype), 'TEXT')
                columns.append(f"    {snake_col} {sql_type}  -- Original column: {orig_col}")
        
        ddl.append(",\n".join(columns))
        ddl.append(");")
        
        return "\n".join(ddl)
    except Exception as e:
        st.error(f"Error generating DDL for {table_name}: {str(e)}")
        return None

def xlsx_import_tool():
    st.title("Excel Sheet Import Tool")
    
    # Initialize session state
    if 'sheets_data' not in st.session_state:
        st.session_state.sheets_data = {}
    if 'table_names' not in st.session_state:
        st.session_state.table_names = {}
    if 'column_names' not in st.session_state:
        st.session_state.column_names = {}
    if 'ignored_sheets' not in st.session_state:
        st.session_state.ignored_sheets = set()
    if 'ignored_columns' not in st.session_state:
        st.session_state.ignored_columns = {}
    
    # Section 1: Upload Excel File
    st.header("1. Upload Excel File")

    c1, _, c2 = st.columns([3,1,6])
    with c1:
        dataset_name = st.text_input("Dataset Name")
    
        if not dataset_name:
            st.error("Please enter a dataset name")
            return
    
        if st.button("Create Dataset"):
            try:
                Path(f"db/{dataset_name}").mkdir(eparents=True, exist_ok=True)
                st.success(f"Created dataset directory: db/{dataset_name}")
            except Exception as e:
                st.error(f"Error creating dataset directory: {str(e)}")
                return
    
    with c2:
        uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])
        if uploaded_file:
            try:
                # Save file
                save_path = f"db/{dataset_name}/{uploaded_file.name}"
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                # Read all sheets
                excel_file = pd.ExcelFile(save_path)
                sheet_names = excel_file.sheet_names
                
                st.success(f"Found {len(sheet_names)} sheets in the Excel file")
                
                # Process each sheet
                for sheet_name in sheet_names:
                    df = pd.read_excel(save_path, sheet_name=sheet_name)
                    
                    if validate_dataframe(df, sheet_name):
                        table_name = snake_case(sheet_name)
                        st.session_state.sheets_data[sheet_name] = df
                        st.session_state.table_names[sheet_name] = table_name
                        st.session_state.column_names[sheet_name] = {col: snake_case(col) for col in df.columns}
                        # Initialize ignored columns for this sheet
                        if sheet_name not in st.session_state.ignored_columns:
                            st.session_state.ignored_columns[sheet_name] = set()
                    else:
                        st.warning(f"invalid data sheet: {sheet_name}")
            except Exception as e:
                st.error(f"Error processing Excel file: {str(e)}")
    
    # Section 2: Review Sheets
    if st.session_state.sheets_data:
        st.header("2. Review Sheets")
        
        for sheet_name, df in st.session_state.sheets_data.items():
            st.subheader(f"Sheet: '{sheet_name}'")
            
            # Sheet ignore checkbox
            col1, col2 = st.columns([6, 1])
            with col1:
                # Table name input
                new_table_name = st.text_input(
                    f"Table name for sheet '{sheet_name}':",
                    value=st.session_state.table_names[sheet_name],
                    key=f"table_{sheet_name}"
                )
                st.session_state.table_names[sheet_name] = new_table_name
            
            with col2:
                ignore_sheet = st.checkbox("Ignore Sheet", 
                                        key=f"ignore_sheet_{sheet_name}",
                                        value=sheet_name in st.session_state.ignored_sheets)
                if ignore_sheet:
                    st.session_state.ignored_sheets.add(sheet_name)
                else:
                    st.session_state.ignored_sheets.discard(sheet_name)
            
            if not ignore_sheet:
                # Column name inputs with ignore checkboxes
                st.write(f"Column names for sheet '{sheet_name}':")
                cols = st.session_state.column_names[sheet_name]
                for orig_col in df.columns:
                    col1, col2, col3 = st.columns([3, 3, 1])
                    with col1:
                        st.text(f"Original: {orig_col}")
                    with col2:
                        new_col = st.text_input(
                            f"New name",
                            value=cols[orig_col],
                            key=f"col_{sheet_name}_{orig_col}"
                        )
                        cols[orig_col] = new_col
                    with col3:
                        ignore_col = st.checkbox("Ignore", 
                                              key=f"ignore_col_{sheet_name}_{orig_col}",
                                              value=orig_col in st.session_state.ignored_columns[sheet_name])
                        if ignore_col:
                            st.session_state.ignored_columns[sheet_name].add(orig_col)
                        else:
                            st.session_state.ignored_columns[sheet_name].discard(orig_col)
                
                # Show sample data
                st.write("Sample data (first 5 rows):")
                display_cols = [col for col in df.columns if col not in st.session_state.ignored_columns[sheet_name]]
                st.dataframe(df[display_cols].head())
    
    # Section 3: Create Tables
    if st.session_state.sheets_data:
        st.header("3. Create Tables")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        all_ddl = [
            f"-- Generated on: {timestamp}",
            f"-- Dataset: {dataset_name}",
            ""
        ]
        
        for sheet_name, df in st.session_state.sheets_data.items():
            if sheet_name not in st.session_state.ignored_sheets:
                table_name = st.session_state.table_names[sheet_name]
                ddl = create_sqlite_ddl(
                    df, 
                    table_name, 
                    sheet_name, 
                    st.session_state.column_names[sheet_name],
                    st.session_state.ignored_columns[sheet_name]
                )
                if ddl:
                    all_ddl.append(ddl)
                    all_ddl.append("")
        
        ddl_content = "\n".join(all_ddl)
        st.code(ddl_content, language="sql")

        try:
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
        
        add_download_buttons(dataset_name)
    
    # Section 4: Load Data
    if st.session_state.sheets_data:
        st.header("4. Load Data")
        
        if st.button("Load Data"):
            loaded_tables = []
            db_path = f"db/{dataset_name}/{dataset_name}.sqlite3"
            conn = None
            try:
                conn = sqlite3.connect(db_path)
                for sheet_name, df in st.session_state.sheets_data.items():
                    if sheet_name not in st.session_state.ignored_sheets:
                        table_name = st.session_state.table_names[sheet_name]
                        try:
                            # Filter out ignored columns and rename remaining ones
                            df_filtered = df[[col for col in df.columns if col not in st.session_state.ignored_columns[sheet_name]]]
                            column_mapping = {col: st.session_state.column_names[sheet_name][col] 
                                           for col in df_filtered.columns}
                            df_renamed = df_filtered.rename(columns=column_mapping)
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
    xlsx_import_tool()

if __name__ == "__main__":
    main()