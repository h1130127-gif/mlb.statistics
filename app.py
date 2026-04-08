import streamlit as st
import pandas as pd
from pybaseball import batting_stats

st.set_page_config(page_title="MLB 數據儀表板", page_icon="⚾")
st.title("⚾ MLB 數據儀表板")

@st.cache_data
def load_data(year):
    try:
        # 限定至少 100 個打席，確保數據具備參考價值
        df = batting_stats(year, qual=100) 
        return df
    except Exception as e:
        st.error(f"抓取資料發生錯誤: {e}")
        return pd.DataFrame()

st.subheader("⚙️ 設定條件")
selected_year = st.selectbox("選擇賽季", [2023, 2022, 2021])

st.write(f"正在載入 **{selected_year}** 年數據...")
data = load_data(selected_year)

if not data.empty:
    search_name = st.text_input("🔍 搜尋球員 (例如: Ohtani, Judge)", "")
    display_cols = ['Name', 'Team', 'G', 'HR', 'SB', 'AVG', 'OBP', 'SLG', 'OPS', 'WAR']
    
    if search_name:
        filtered_data = data[data['Name'].str.contains(search_name, case=False, na=False)]
        st.write(f"找到 {len(filtered_data)} 位符合的球員：")
        st.dataframe(filtered_data[display_cols])
    else:
        st.write("目前顯示全聯盟數據預覽：")
        st.dataframe(data[display_cols].head(10))
