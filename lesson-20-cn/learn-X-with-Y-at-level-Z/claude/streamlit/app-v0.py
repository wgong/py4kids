import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

def make_clickable(url):
    return f'<a href="{url}" target="_blank">{url}</a>'

def main():
    st.title("Resource Editor")

    # Load the data
    df = pd.read_csv("cs-1.csv")

    # Make URL clickable
    df['URL'] = df['URL'].apply(make_clickable)
    # st.dataframe(df)


    # Create a GridOptionsBuilder
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True, groupable=True, value=True, enableRowGroup=True, aggFunc='sum', autoHeight=True, wrapText=True)
    gb.configure_column("URL", cellRenderer='html')
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

    # Get the updated dataframe
    updated_df = grid_response['data']

    # Display the updated dataframe
    st.write("Updated Data:")
    st.dataframe(updated_df)

    # Option to download the updated CSV
    if st.button('Download Updated CSV'):
        csv = updated_df.to_csv(index=False)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='updated_resources.csv',
            mime='text/csv',
        )

if __name__ == "__main__":
    main()