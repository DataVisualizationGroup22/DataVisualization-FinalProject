import streamlit as st
import pandas as pd
import numpy as np

row = st.container()

with row:
    st.write('row1')
with row:
    st.write('row2')