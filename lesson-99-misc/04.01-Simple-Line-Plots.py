import streamlit as st


st.write(list(range(5)))

if False:
	# %matplotlib inline
	import matplotlib.pyplot as plt
	plt.style.use('seaborn-whitegrid')
	import numpy as np
	fig = plt.figure()
	ax = plt.axes()
	fig = plt.figure()
	ax = plt.axes()

	x = np.linspace(0, 10, 1000)
	ax.plot(x, np.sin(x))
