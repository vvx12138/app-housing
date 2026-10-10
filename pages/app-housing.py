import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------------------- 自动适配文件路径，本地和云端都不会报找不到CSV的错误 ----------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "housing.csv")

# ---------------------- 页面基础配置 ----------------------
st.set_page_config(page_title="California Housing Data 1990", layout="wide")

# ---------------------- 加载数据 ----------------------
@st.cache_data  # 开启缓存，大幅提升重复加载速度
def load_data():
    df = pd.read_csv(csv_path)
    return df

df = load_data()

# ---------------------- 主页面标题 ----------------------
st.title("California Housing Data (1990) by vvx")

# ---------------------- 主页面滑块筛选 ----------------------
min_house_value = st.slider(
    "Minimal Median House Value",
    min_value=0,
    max_value=500001,
    value=200000
)
# 第一步筛选：只保留房价大于等于滑块值的区域
filtered_df = df[df["median_house_value"] >= min_house_value]

# ---------------------- 侧边栏筛选区域 ----------------------
st.subheader("See more filters in the sidebar:")
with st.sidebar:
    # 多选框：筛选临海类型，默认全选
    location_types = st.multiselect(
        "Choose the location type",
        options=df["ocean_proximity"].unique(),
        default=df["ocean_proximity"].unique()
    )
    
    # 单选框：筛选收入等级
    income_level = st.radio(
        "Choose income level",
        options=["Low", "Medium", "High"]
    )

# ---------------------- 应用剩余两个筛选条件 ----------------------
# 临海类型筛选
filtered_df = filtered_df[filtered_df["ocean_proximity"].isin(location_types)]

# 收入等级筛选
if income_level == "Low":
    filtered_df = filtered_df[filtered_df["median_income"] <= 2.5]
elif income_level == "Medium":
    filtered_df = filtered_df[(filtered_df["median_income"] > 2.5) & (filtered_df["median_income"] < 4.5)]
elif income_level == "High":
    filtered_df = filtered_df[filtered_df["median_income"] >= 4.5]

# ---------------------- 渲染地图 ----------------------
st.subheader("Filtered Districts Map")
st.map(filtered_df, latitude="latitude", longitude="longitude")

# ---------------------- 渲染房价直方图 ----------------------
st.subheader("Median House Value Distribution")
fig, ax = plt.subplots()
ax.hist(filtered_df["median_house_value"], bins=30, edgecolor="black")
ax.set_xlabel("Median House Value ($)")
ax.set_ylabel("Number of Districts")
st.pyplot(fig)
