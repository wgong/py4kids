from utils import *

st.set_page_config(layout="wide")


def get_all_tables(db_path):
    """Get list of all tables in SQLite database."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]
        
        conn.close()
        return tables
    except Exception as e:
        st.error(f"Error reading database tables: {str(e)}")
        return []

def preview_table(db_path, table_name):
    """Show preview of table data."""
    try:
        # Read first 5 rows from table
        conn = sqlite3.connect(db_path)
        query = f"SELECT * FROM {table_name} LIMIT 5"
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    except Exception as e:
        st.error(f"Error previewing table {table_name}: {str(e)}")
        return None

def sqlite_import_tool():
    st.header("SQlite Import Tool 📥")
    DB_LOADED = False

    # Section 1: Upload SQLite
    st.subheader("1. Upload SQLite Database")

    c1, _, c2 = st.columns([3,1,6])
    with c1:
        dataset_name = st.text_input("Dataset Name")
    
        # Early return if no dataset name
        if not dataset_name:
            st.error("Please enter a dataset name")
            return
    
        if st.button("Create Dataset"):
            try:
                # Create directory
                Path(f"db/{dataset_name}").mkdir(eparents=True, exist_ok=True)
                st.success(f"Created dataset directory: db/{dataset_name}")
            except Exception as e:
                st.error(f"Error creating dataset directory: {str(e)}")
                return
    
    with c2:
        uploaded_file = st.file_uploader(
            "Upload SQLite database", 
            type=["db", "sqlite", "sqlite3"], 
            help="Upload your SQLite database file"
        )
        
        if uploaded_file and dataset_name:
            try:
                # Save the uploaded file with the new name
                save_path = f"db/{dataset_name}/{dataset_name}.sqlite3"
                
                # Write the uploaded file
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                st.success(f"""
                Database imported successfully:
                - Original file: {uploaded_file.name}
                - Saved as: {save_path}
                """)

                DB_LOADED = True
                
                
            except Exception as e:
                st.error(f"Error processing database file: {str(e)}")

    if DB_LOADED:
        # Preview Section - Now in full width below upload section
        st.subheader("2. Preview Data")
        
        # Get all tables
        tables = get_all_tables(save_path)
        
        if tables:
            st.success(f"Imported {len(tables)} tables:")
            tab_list = ',\t '.join(tables)
            st.info(f"{tab_list}")
            
            # Preview each table
            for table in tables:
                with st.expander(f"Table: {table}"):
                    st.caption("First 5 rows:")
                    df = preview_table(save_path, table)
                    if df is not None:
                        st.dataframe(df)
                        st.caption(f"Columns: {', '.join(df.columns)}")
        else:
            st.warning("No tables found in database")


def main():
    sqlite_import_tool()

if __name__ == "__main__":
    main()