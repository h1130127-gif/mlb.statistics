import streamlit as st
import pandas as pd

st.set_page_config(page_title="MLB 數據儀表板", page_icon="⚾")
st.title("⚾ MLB 數據儀表板 ")

# 加上參數 year，讓程式知道要讀哪個檔案
@st.cache_data
def load_data(year):
    try:
        df = pd.read_csv(f"mlb_{year}.csv")
        return df
    except Exception as e:
        st.error(f"找不到 {year} 年的資料檔案，請確認是否已上傳到 GitHub！")
        return pd.DataFrame()

# 加入年份選擇器
st.subheader("⚙️ 設定條件")
selected_year = st.selectbox("選擇賽季", [2023, 2024, 2025])

st.write(f"正在載入 **{selected_year}** 年數據...")
data = load_data(selected_year)

if not data.empty:
    search_name = st.text_input("🔍 搜尋球員 (例如: Ohtani, Judge)", "")
    
    display_cols = ['Name', 'Tm', 'G', 'HR', 'SB', 'BA', 'OBP', 'SLG', 'OPS']
    available_cols = [col for col in display_cols if col in data.columns]
    
    if search_name:
        filtered_data = data[data['Name'].str.contains(search_name, case=False, na=False)]
        st.write(f"找到 {len(filtered_data)} 位符合的球員：")
        st.dataframe(filtered_data[available_cols])
    else:
        st.write(f"目前顯示 {selected_year} 年全聯盟數據預覽：")
        st.dataframe(data[available_cols].head(10))
