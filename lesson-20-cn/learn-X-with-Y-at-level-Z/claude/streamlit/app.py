import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

file_csv = "stem-learning-resources-per-claude-pro.csv"
st.set_page_config(layout="wide")  # Set the page layout to wide mode

def main():
    
    st.title("Learning Resources")

    # Load the data
    df = pd.read_csv(file_csv)

    # Create a GridOptionsBuilder
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True, groupable=True, value=True, enableRowGroup=True, aggFunc='sum', autoHeight=True, wrapText=True)
    
    # Configure URL column to render HTML and be non-editable
    url_renderer = JsCode("""
    class URLRenderer {
        init(params) {
            this.eGui = document.createElement('a');
            this.eGui.innerText = params.value;
            this.eGui.setAttribute('href', params.value);
            this.eGui.setAttribute('target', '_blank');
            this.eGui.style.color = 'blue';
            this.eGui.style.textDecoration = 'underline';
        }
        getGui() {
            return this.eGui;
        }
    }
    """)

    gb.configure_column("URL", 
                        cellRenderer=url_renderer,
                        editable=False)
    
    gb.configure_selection('single')
    gridOptions = gb.build()

    # Use st.container() to create a full-width container
    with st.container():
        # Display the grid
        grid_response = AgGrid(
            df, 
            gridOptions=gridOptions,
            update_mode=GridUpdateMode.MODEL_CHANGED,
            fit_columns_on_grid_load=True,
            allow_unsafe_jscode=True,
            theme='streamlit',  # Use the streamlit theme for better integration
            height=600,  # Set a fixed height for the grid
        )

    # Option to download the updated CSV
    updated_df = grid_response['data']
    if updated_df is not None and not updated_df.empty:
        st.download_button(
            label="Download CSV",
            data=updated_df.to_csv(index=False),
            file_name='updated_resources.csv',
            mime='text/csv',
        )

if __name__ == "__main__":
    main()