import streamlit as st
import pandas as pd

# 【美化技巧】：加入 layout="wide" 讓網站自動填滿整個螢幕寬度
st.set_page_config(page_title="MLB 數據儀表板", page_icon="⚾", layout="wide")
st.title("⚾ MLB 數據儀表板")

@st.cache_data
def load_data(year):
    try:
        df = pd.read_csv(f"mlb_{year}.csv")
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"找不到 {year} 年的資料檔案！錯誤細節: {e}")
        return pd.DataFrame()

# 【美化技巧】：把設定條件收納到側邊欄，讓主畫面乾淨
st.sidebar.header("⚙️ 設定條件")
selected_year = st.sidebar.selectbox("選擇賽季", [2023, 2024, 2025])

data = load_data(selected_year)

if not data.empty:
    search_name = st.text_input("🔍 搜尋球員 (例如: Ohtani, Judge)", "")
    
    if 'Name' in data.columns:
        name_col = 'Name'
    elif len(data.columns) > 1:
        name_col = data.columns[1]
    else:
        name_col = data.columns[0]
    
    display_cols = [name_col, 'Age', 'Tm', 'G', 'HR', 'SB', 'BA', 'OBP', 'SLG', 'OPS']
    available_cols = [col for col in display_cols if col in data.columns]
    
    if search_name:
        filtered_data = data[data[name_col].astype(str).str.contains(search_name, case=False, na=False)]
        
        if not filtered_data.empty:
            st.success(f"找到了！ {len(filtered_data)} 位符合條件的球員")
            
            # 【美化核心】：抓出搜尋到的第一位球員，做成戰力看板
            player = filtered_data.iloc[0]
            st.subheader(f"⭐ {player[name_col]} ({player.get('Tm', '未知球隊')})")
            
            # 使用 st.columns 把畫面切成 4 等份
            col1, col2, col3, col4 = st.columns(4)
            
            # 使用 st.metric 顯示大字體數據
            col1.metric(label="全壘打 (HR)", value=player.get('HR', 0))
            col2.metric(label="打擊率 (BA)", value=player.get('BA', 0.0))
            col3.metric(label="攻擊指數 (OPS)", value=player.get('OPS', 0.0))
            col4.metric(label="盜壘 (SB)", value=player.get('SB', 0))
            
            st.markdown("---") # 畫一條分隔線
            st.write("詳細數據表格：")
            st.dataframe(filtered_data[available_cols])
        else:
            st.warning("查無此人，請確認拼字是否正確喔！")
            
    else:
        st.write(f"目前顯示 **{selected_year}** 年全聯盟數據預覽：")
        st.dataframe(data[available_cols].head(15))
