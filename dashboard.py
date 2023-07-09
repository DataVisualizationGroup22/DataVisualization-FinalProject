import streamlit as st
import matplotlib.pyplot as plt
import mpld3
import pandas as pd
import geopandas as gpd
from unidecode import unidecode

# Không hiện thông báo PyplotGlobalUseWarning
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(layout='wide', initial_sidebar_state='expanded')


# Đọc các tệp chứa dữ liệu cần thiết
df = pd.read_csv('dataset/house_preprocessing_for_dashboard.csv', index_col=0)
gdf = gpd.read_file('hanoi_map/geo_hanoi_map.geojson')

st.sidebar.header('Tùy chọn')



def line_chart(attr, value, range):
    st.markdown('### Map 1')
    df_copy = df.copy()
    df_copy = df_copy[df_copy[attr].isin(value)]
    df_copy = df_copy[(df_copy['Giá/m2 (triệu)'] >= range[0]) & (df_copy['Giá/m2 (triệu)'] <= range[1])]

    df_copy['Ngày'] = pd.to_datetime(df['Ngày'])
    df_copy['Tháng'] = df_copy['Ngày'].dt.to_period('M').astype(str)
    line_df = df_copy.groupby(['Tháng', attr])['Giá/m2 (triệu)'].mean().reset_index().pivot_table(index='Tháng', columns=attr, values='Giá/m2 (triệu)').fillna(0)
    st.line_chart(line_df)

def bar_chart(attr, value, range):
    st.markdown('### Map 3')
    df_copy = df.copy()
    df_copy = df_copy[df_copy[attr].isin(value)]
    df_copy = df_copy[(df_copy['Giá/m2 (triệu)'] >= range[0]) & (df_copy['Giá/m2 (triệu)'] <= range[1])]

    bar_df = df_copy.groupby([attr])['Giá/m2 (triệu)'].mean()
    st.bar_chart(bar_df)

def hanoi_map(attr, value, range):
    st.markdown('### Map 2')
    df_copy = df.copy()
    df_copy = df_copy[df_copy[attr].isin(value)]
    df_copy = df_copy[(df_copy['Giá/m2 (triệu)'] >= range[0]) & (df_copy['Giá/m2 (triệu)'] <= range[1])]

    df_copy['Quận'] = df_copy['Quận'].fillna('').apply(lambda x: x.replace('Quận ', '').replace('Huyện ', '').replace('Thị xã ', ''))
    df_copy['Quận'] = df_copy['Quận'].replace(['Nam Từ Liêm', 'Bắc Từ Liêm'], 'Từ Liêm')
    df_copy['Quận'] = df_copy['Quận'].apply(unidecode)
    hanoi_df = df_copy.groupby('Quận')['Giá/m2 (triệu)'].mean().reset_index()
    hanoi_df = hanoi_df.merge(gdf, on='Quận', how='left')
    hanoi_df = gpd.GeoDataFrame(hanoi_df[['Giá/m2 (triệu)', 'geometry']])

    fig, ax = plt.subplots()
    hanoi_df.plot(column='Giá/m2 (triệu)', cmap='OrRd', linewidth=0.8, edgecolor='0.8', legend=True , ax=ax)
    st.pyplot()
    html = mpld3.fig_to_html(fig)
    st.components.v1.html(html, height=500)


def dashboard():
    title = '<h1 style="text-align:center; color:#47C7DA">Tên dashboard</h1>'
    st.markdown(title, unsafe_allow_html=True)
    select_attr = st.sidebar.selectbox('Chọn cột', ('Quận', 'Loại hình nhà ở', 'Giấy tờ pháp lý', 'Số tầng', 'Số phòng ngủ', 'Diện tích (m2)', 'Dáng nhà'))

    all_value = list(df[select_attr].unique())
    select_value = st.sidebar.multiselect('Chọn các mục', options=['Tất cả'] + all_value, default='Tất cả')
    if 'Tất cả' in select_value:
        select_value = all_value

    select_range = st.sidebar.slider('Chọn khoảng giá trị', float(df['Giá/m2 (triệu)'].min()), float(df['Giá/m2 (triệu)'].max()), (float(df['Giá/m2 (triệu)'].min()), float(df['Giá/m2 (triệu)'].max())))
    line_chart(select_attr, select_value, select_range)
    col1, col2 = st.columns(2)
    with col1:
        hanoi_map(select_attr, select_value, select_range)
    with col2:
        bar_chart(select_attr, select_value, select_range)


def overview():
    title = '<h1 style="text-align:center; color:#47C7DA">Overview</h1>'
    st.markdown(title, unsafe_allow_html=True)
    # Add content for page 2

def insight():
    title = '<h1 style="text-align:center; color:#47C7DA">Insight</h1>'
    st.markdown(title, unsafe_allow_html=True)

# Create a session state class to manage page selection
class SessionState:
    def __init__(self):
        self.page = None

# Create an instance of the session state
state = SessionState()

# Define the main function to handle page selection
def main():
    # Add a selection box to choose the page
    page = st.sidebar.selectbox("Chọn trang", ["Overview", "Insight", "Dashboard"])

    # Set the current page in the session state
    if page == "Overview":
        state.page = overview
    elif page == "Insight":
        state.page = insight
    elif page == "Dashboard":
        state.page = dashboard

    # Call the current page function
    state.page()

# Run the application
if __name__ == '__main__':
    main()