import streamlit as st
import pandas as pd
import numpy as np
import os
import time

## Menu
st.sidebar.write("[Streamlit concepts](https://docs.streamlit.io/library/get-started/main-concepts)")
menu_options = ("Dataframe", "Widget", "Layout", "Theme", "Cache", "Misc")
default_ix = menu_options.index("Cache")
menu_item = st.sidebar.selectbox("Pick a Concept:", menu_options, index=default_ix)
st.sidebar.write("""
Since Streamlit runs script from top to bottom, we use menu-item to split
the whole script into sub-sections, so only a selected sub-section is rerun
""")

st.sidebar.write("""
Streamlit links
- [Cheatsheet](https://docs.streamlit.io/library/cheatsheet)
- [API Reference](https://docs.streamlit.io/library/api-reference)
- [Components](https://docs.streamlit.io/library/components)
- [Gallery](https://streamlit.io/gallery)
""")



if menu_item == "Dataframe":

    ## Display Data
    st.header('Dataframe')
    st.subheader('st.write anything')
    st.write(pd.DataFrame({
        'first column': list(range(5)),
        'second column': [100*i for i in range(5)]
    }))

    df = pd.DataFrame({
        'first column': [1, 2, 3, 4],
        'second column': [10, 20, 30, 40]
    })
    df # same as : st.write(df)

    st.subheader('st.dataframe makes interactive table')
    df = np.random.randn(10, 20)
    st.dataframe(df)

    dataframe = pd.DataFrame(
        np.random.randn(10, 20),
        columns=('col %d' % i for i in range(20)))
    st.dataframe(dataframe.style.highlight_max(axis=0))

    st.subheader('st.table makes static table')
    st.table(dataframe)

    st.header('Charts and Maps')
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])
    st.line_chart(chart_data)

    map_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        columns=['lat', 'lon'])
    st.map(map_data)

if menu_item == "Widget":
    ## UI control
    st.header('Widgets ')



    st.subheader('st.slider')  
    # Add a slider to the sidebar:
    slider_range = st.slider(
        'Select a range of values',
        0.0, 100.0, (25.0, 75.0)
    )
    st.write(f"Range: {slider_range}")

    slider_value = st.slider(
        'Select a values',
        0.0, 100.0, 50.0
    )
    st.write(f"Value: {slider_value}")

    x = st.slider('x') # 👈 this is a widget
    st.write(x, 'squared is', x * x)

    st.subheader('st.text_input ')
    st.text_input("Your name", key="name")
    # You can access the value at any point with:
    st.write(f"You entered: {st.session_state.name}")

    st.subheader('st.selectbox ')
    df = pd.DataFrame({
        'first column': [1, 2, 3, 4],
        'second column': [10, 20, 30, 40]
    })
    option = st.selectbox(
        'Which number do you like best?',
        df['first column'])
    'You selected: ', option

    # Add a selectbox to the sidebar:
    selectbox_contact = st.selectbox(
        'How would you like to be contacted?',   # label
        ('Email', 'Home phone', 'Mobile phone')
    )
    st.write(f"You prefer to be contacted by : {selectbox_contact}")

    st.subheader('st.checkbox ')
    if st.checkbox('Show dataframe'):
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['a', 'b', 'c'])
        chart_data

    st.subheader('st.progress')
    'Starting a long computation...'
    # Add a placeholder
    latest_iteration = st.empty()
    bar = st.progress(0)
    for i in range(100):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {i+1}')
        bar.progress(i + 1)
        time.sleep(0.1)
    '...and now we\'re done!'

if menu_item == "Layout":
    ## UI Layout
    st.header('Layout')

    st.subheader('st.columns')  
    left_column, right_column = st.columns(2)

    # You can use a column just like st.sidebar:
    with left_column:
        st.subheader('st.button')    
        st.button('Press me!')
    # Or even better, call Streamlit functions inside a "with" block:
    with right_column:
        st.subheader('st.radio')    
        chosen = st.radio(
            'Sorting hat',
            ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
        st.write(f"You are in {chosen} house!")

if menu_item == "Theme":
    ## Theme
    st.header('Theme')

@st.cache # 👈 below function will be cached
def Fibonacci(n):
    # Function for nth Fibonacci number

    # Check if input is 0 then it will
    # print incorrect input
    if n < 0:
        print(f"Incorrect input: {n}, must be an int >=0")
        return None

    # Check if n is 0
    # then it will return 0
    elif n == 0:
        return 0

    # Check if n is 1,2
    # it will return 1
    elif n == 1 or n == 2:
        return 1
    else:
        return Fibonacci(n-1) + Fibonacci(n-2)

if menu_item == "Cache":

    ## Caching
    st.header('Caching')
    num = st.slider("num", 1, 100, 5)
    ts_start = time.time()
    fib_num = Fibonacci(num)
    ts_duration = time.time() - ts_start
    st.write(f"Fib({num}) = {fib_num} \n calculated in {ts_duration:.3f} sec")
    st.button("Rerun")

    st.write("""Notice that:\n
    (1) calculating Fib of the same number takes much smaller constant time;\n
    (2) sub-function within recursive calls are also cached;
    """)

if menu_item == "Misc":
    st.header('Misc')
    st.write(f"os.getcwd() = {os.getcwd()}" )

st.write("""
[streamlitapp-demo-concept](https://share.streamlit.io/wgong/streamlitapp/main/demos/demo_concept.py)
"""
)
