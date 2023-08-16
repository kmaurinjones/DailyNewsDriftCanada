import streamlit as st
from plot import *

updated_grand_plot = show_grand_plot()

st.write("This is a test")

st.plotly_chart(updated_grand_plot)