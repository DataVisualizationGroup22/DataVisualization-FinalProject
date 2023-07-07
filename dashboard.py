import streamlit as st
import pandas as pd

data = pd.read_csv('VN_housing_dataset_preprocessing.csv')
data['Giá/m2 (triệu)'] = data['Giá']

st.sidebar.header('Điền vào tên dashboard')

select_attr = st.sidebar.selectbox('Chọn cột', ('Quận', 'Loại hình nhà ở', 'Giấy tờ pháp lý', 'Số tầng', 'Số phòng ngủ', 'Diện tích', 'Dáng nhà'))

all_value = list(data[select_attr].unique())
select_value = st.sidebar.multiselect('Chọn các mục', options=['Tất cả'] + all_value, default='Tất cả')
if 'Tất cả' in select_value:
    select_value = all_value

select_range = st.sidebar.slider('Chọn khoảng giá trị', data['Giá/m2 (triệu)'].min(), data['Giá/m2 (triệu)'].max(), (data['Giá/m2 (triệu)'].min(), data['Giá/m2 (triệu)'].max()))

def line_chart(attr, value, range):
    data_copy = data.copy()
    data_copy = data_copy[data_copy[attr].isin(value)]
    data_copy = data_copy[(data_copy['Giá/m2 (triệu)'] >= range[0]) & (data_copy['Giá'] <= range[1])]
    data_copy['Ngày'] = pd.to_datetime(data['Ngày'])
    data_copy['Tháng'] = data_copy['Ngày'].dt.to_period('M').astype(str)
    line_df = data_copy.groupby(['Tháng', attr])['Giá/m2 (triệu)'].mean().reset_index().pivot_table(index='Tháng', columns=attr, values='Giá/m2 (triệu)').fillna(0)
    st.line_chart(line_df)

def bar_chart(attr, value, range):
    data_copy = data.copy()
    data_copy = data_copy[data_copy[attr].isin(value)]
    data_copy = data_copy[(data_copy['Giá/m2 (triệu)'] >= range[0]) & (data_copy['Giá'] <= range[1])]
    bar_df = data_copy.groupby([attr])['Giá/m2 (triệu)'].mean()
    st.bar_chart(bar_df)

line_chart(select_attr, select_value, select_range)
col1, col2 = st.columns(2)
with col1:
    st.write('Thêm bản đồ TP Hà Nội')    
with col2:
    bar_chart(select_attr, select_value, select_range)