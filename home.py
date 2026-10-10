import streamlit as st
import pandas as pd
import os

# 自动适配 CSV 路径，本地和云端都不会报找不到CSV的错误
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "housing.csv")

# 页面基础配置（封面页）
st.set_page_config(page_title="Housing App — 封面", layout="centered")

st.title("🏡 California Housing Explorer")
st.subheader("数据可视化与交互式探索 — 封面")

st.write("---")

col1, col2 = st.columns([2, 3])
with col1:
    st.write("###### 作者")
    st.write("vvx")
    st.write("###### 用途")
    st.write("一个用于探索 1990 年加州房价数据的交互式 Streamlit 应用。")
    st.write("###### 快速操作")
    st.code("streamlit run app-housing.py")

with col2:
    st.write("###### 简短说明")
    st.write(
        "本应用包含一个封面页（当前页面）和一个分析页（app-housing.py）。\n"
        "在分析页中你可以通过滑块、侧边栏等交互控件筛选区域、查看地图与分布图。"
    )

st.write("---")

# 尝试载入数据并展示一些快速统计信息
@st.cache_data
def load_data(path):
    try:
        return pd.read_csv(path)
    except Exception as e:
        return None

df = load_data(csv_path)

if df is None:
    st.error("未找到 housing.csv 或读取失败。请确保 housing.csv 与本仓库在同一目录，然后运行：\n\n`streamlit run home.py` 或 `streamlit run app-housing.py`")
else:
    st.success("数据已加载：housing.csv")
    st.write(f"记录数：{len(df):,}")
    st.write(f"区域数（唯一经纬点）：{df[['latitude','longitude']].drop_duplicates().shape[0]:,}")

    with st.expander("查看数据样例（前 5 行）"):
        st.dataframe(df.head())

    with st.expander("快速统计"):
        st.metric("Median of median_house_value", f"${int(df['median_house_value'].median()):,}")
        st.metric("Average median_income", f"{df['median_income'].mean():.2f}")

st.write("---")

# 导航提示
st.info("要进入交互式分析页面，请在终端运行 `streamlit run app-housing.py`，或在 Streamlit 的多页面应用中打开 `app-housing.py` 页面。")

# 版权与许可
st.write("\n\n---\n此应用基于公开的加州住房数据示例，代码由 vvx 发布。查看 GitHub 仓库以获取更多信息。")
