import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)

data = pd.read_csv('VN_housing_dataset_preprocessing.csv')

st.sidebar.header('Điền vào tên dashboard')

select_attr = st.sidebar.selectbox('Attributes', ('Quận', 'Loại hình nhà ở', 'Giấy tờ pháp lý', 'Số tầng', 'Số phòng ngủ', 'Diện tích', 'Dáng nhà'))

def line_chart(attr):
    data_copy = data.copy()
    data_copy['Ngày'] = pd.to_datetime(data['Ngày'])
    data_copy['Tháng'] = data_copy['Ngày'].dt.to_period('M').astype(str)
    line_df = data_copy.groupby(['Tháng', attr])['Giá'].mean().reset_index().pivot_table(index='Tháng', columns=attr, values='Giá').fillna(0)
    st.line_chart(line_df)

def bar_chart(attr):
    data_copy = data.copy()
    bar_df = data_copy.groupby([attr])['Giá'].mean()
    st.bar_chart(bar_df)

line_chart(select_attr)
col1, col2 = st.columns(2)
with col1:
    st.write('Thêm bản đồ TP Hà Nội')    
with col2:
    bar_chart(select_attr)