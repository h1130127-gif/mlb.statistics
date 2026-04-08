import streamlit as st
import pandas as pd

st.set_page_config(page_title="MLB 數據儀表板", page_icon="⚾")
st.title("⚾ MLB 數據儀表板 (完整終極版)")

# 加入 year 參數，並保留欄位名稱修復功能
@st.cache_data
def load_data(year):
    try:
        # 動態讀取對應年份的 CSV
        df = pd.read_csv(f"mlb_{year}.csv")
        # 清除欄位名稱可能隱藏的空格
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"找不到 {year} 年的資料檔案，請確認 mlb_{year}.csv 是否已上傳！錯誤細節: {e}")
        return pd.DataFrame()

# 找回我們的年份選擇器！
st.subheader("⚙️ 設定條件")
selected_year = st.selectbox("選擇賽季", [2023, 2024, 2025])

st.write(f"正在載入 **{selected_year}** 年數據...")
data = load_data(selected_year)

if not data.empty:
    search_name = st.text_input("🔍 搜尋球員 (例如: Ohtani, Judge)", "")
    
    # 聰明地尋找姓名欄位
    if 'Name' in data.columns:
        name_col = 'Name'
    elif len(data.columns) > 1:
        name_col = data.columns[1] # 通常 B-Ref 的第二個欄位是名字
    else:
        name_col = data.columns[0]
    
    # 設定要顯示的欄位
    display_cols = [name_col, 'Age', 'Tm', 'G', 'HR', 'SB', 'BA', 'OBP', 'SLG', 'OPS']
    available_cols = [col for col in display_cols if col in data.columns]
    
    if search_name:
        # 搜尋功能
        filtered_data = data[data[name_col].astype(str).str.contains(search_name, case=False, na=False)]
        st.write(f"找到 {len(filtered_data)} 位符合的球員：")
        st.dataframe(filtered_data[available_cols])
    else:
        st.write(f"目前顯示 **{selected_year}** 年全聯盟數據預覽：")
        st.dataframe(data[available_cols].head(10))
