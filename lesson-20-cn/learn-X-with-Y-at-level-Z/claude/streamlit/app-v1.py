import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

def main():
    st.title("Resource Editor")

    # Load the data
    df = pd.read_csv("stem-learning-resources-per-claude-pro.csv")

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

    # Display the grid
    grid_response = AgGrid(
        df, 
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True
    )

    # Option to download the updated CSV
    if st.button('Download Updated CSV'):
        # Get the updated dataframe
        updated_df = grid_response['data']
        csv = updated_df.to_csv(index=False)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='updated_resources.csv',
            mime='text/csv',
        )

if __name__ == "__main__":
    main()