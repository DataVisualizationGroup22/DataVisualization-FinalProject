import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)

data = pd.read_csv('VN_housing_dataset_preprocessing.csv')

st.title('Dashboard')

a1, a2 = st.columns(2)

with a1:
    data_district = data.groupby('Quận')['Giá'].mean().reset_index()
    data_district = data_district.sort_values('Giá', ascending=False)
    plt.bar(data_district.index, data_district['Giá'])
    plt.xticks(rotation=90)
    st.pyplot()
with a2:
    data['Ngày'] = pd.to_datetime(data['Ngày'])
    data_monthly = data.groupby(data['Ngày'].dt.to_period('M'))['Giá'].mean().reset_index()
    data_monthly.plot(x='Ngày', y='Giá', kind='line', rot=90)
    st.pyplot()