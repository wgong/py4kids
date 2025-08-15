
https://chat.z.ai/c/240e081d-a855-4cdd-8631-8ce78ec885ce


Here are practical examples demonstrating `@st.fragment` for selective reruns in Streamlit. Remember to enable this experimental feature when running your app:

```bash
streamlit run your_app.py --experimentalEnableWidgets
```

---

### Example 1: Basic Fragment with Slider
```python
import streamlit as st
import time

@st.fragment
def dynamic_slider():
    value = st.slider("Adjust value", 0, 100, 25)
    st.write(f"Selected: {value}")
    st.write(f"Last updated: {time.strftime('%H:%M:%S')}")

st.title("Fragment Demo")
st.write("This static text doesn't reload when slider changes")
dynamic_slider()
```
**Behavior**: Only the fragment reruns when you move the slider (timestamp updates). The title and static text remain unchanged.

---

### Example 2: Multiple Independent Fragments
```python
import streamlit as st
import time

@st.fragment
def temperature_converter():
    celsius = st.slider("Celsius", -100, 100, 0)
    fahrenheit = (celsius * 9/5) + 32
    st.write(f"{celsius}°C = {fahrenheit:.1f}°F")
    st.caption(f"Updated at {time.strftime('%H:%M:%S')}")

@st.fragment
def color_picker():
    color = st.color_picker("Choose a color", "#00f900")
    st.markdown(f"### Selected color: {color}")
    st.markdown(f'<div style="width:100px; height:100px; background-color:{color}"></div>', unsafe_allow_html=True)

st.header("Independent Widgets")
temperature_converter()
color_picker()
```
**Behavior**: 
- Moving the temperature slider only updates the conversion (timestamp changes)
- Changing the color picker only updates the color display
- Neither widget affects the other's state

---

### Example 3: Fragment with State Preservation
```python
import streamlit as st

@st.fragment
def persistent_counter():
    if "count" not in st.session_state:
        st.session_state.count = 0
    
    def increment():
        st.session_state.count += 1
    
    st.button("Increment", on_click=increment)
    st.metric("Counter", st.session_state.count)

st.title("Stateful Fragment")
persistent_counter()
st.text_input("This input doesn't reset when counter changes")
```
**Behavior**: 
- The counter maintains its state within the fragment
- The text input value persists when you increment the counter
- Without fragment, the text input would reset on every button click

---

### Example 4: Fragment with Expensive Computation
```python
import streamlit as st
import time
import pandas as pd

@st.fragment
def data_processing():
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    
    if uploaded_file:
        # Simulate expensive processing
        with st.spinner("Processing..."):
            time.sleep(2)
            df = pd.read_csv(uploaded_file)
            st.dataframe(df.head())
            st.success(f"Processed {len(df)} rows")
    else:
        st.info("Upload a CSV file")

st.title("Data Processor")
data_processing()
st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)
```
**Behavior**: 
- Uploading a file only triggers the fragment to rerun
- The logo image doesn't reload during processing
- Without fragment, the entire page (including image) would reload on upload

---

### Example 5: Nested Fragments
```python
import streamlit as st

@st.fragment
def parent_fragment():
    st.subheader("Parent Fragment")
    parent_value = st.slider("Parent value", 0, 10, 5)
    
    @st.fragment
    def child_fragment():
        st.write("Child Fragment")
        child_value = st.slider("Child value", 0, 10, 5)
        st.write(f"Parent: {parent_value}, Child: {child_value}")
    
    child_fragment()
    st.write("Parent content")

st.title("Nested Fragments")
parent_fragment()
st.write("Main app content")
```
**Behavior**: 
- Changing parent slider only reruns parent fragment (child resets to default)
- Changing child slider only reruns child fragment (parent value persists)
- Main app content never reloads

---

### Key Benefits of Fragments:
1. **Performance**: Avoids unnecessary recomputation of unrelated components
2. **State Preservation**: Maintains widget values outside the fragment
3. **Modular Design**: Encapsulates related functionality
4. **Reduced Flickering**: Prevents UI elements from disappearing/reappearing
5. **Efficient Updates**: Minimizes data transfer between server and client

### Limitations:
1. **Experimental**: API might change in future versions
2. **State Isolation**: Session state is shared but widget states are isolated
3. **Nesting Rules**: Child fragments can't access parent fragment's widget states directly
4. **Callback Restrictions**: Callbacks inside fragments can only modify session state

Use fragments when you have:
- Independent UI sections
- Expensive computations
- Frequently changing widgets
- Complex state management needs
- Performance-critical components

Remember to test thoroughly as the behavior might differ from regular Streamlit execution!