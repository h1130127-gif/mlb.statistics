import streamlit as st
import pandas as pd

# 【美化技巧】：加入 layout="wide" 並設定網頁標題
st.set_page_config(page_title="MLB statistics", page_icon="⚾", layout="wide")

# ==============================
# 🧰 【核心魔法】：注入自訂 CSS 樣式
# ==============================
st.markdown("""
<style>
    /* 1. 設定整體網頁漸層背景 (運動藍) */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #1a237e 40%, #0d1117 100%);
        color: white;
    }
    
    /* 2. 美化側邊欄 */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px); /* 磨砂玻璃效果 */
    }
    
    /* 3. 美化主標題與副標題顏色 */
    h1, h2, h3, p {
        color: white !important;
        font-family: 'Open Sans', sans-serif;
    }
    .stMarkdown p {
        color: rgba(255,255,255,0.8) !important;
    }

    /* 4. 【核心美化】：Metric 卡片 (戰力看板) */
    [data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        
        /* 【動態效果】：加入平滑過渡動畫 */
        transition: all 0.3s ease-in-out;
    }
    
    /* 【動態效果】：滑鼠懸停時卡片浮起、變亮、加陰影 */
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px); /* 向上浮動 */
        background-color: rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 20px rgba(0, 255, 255, 0.3); /* 霓虹藍陰影 */
        border-color: rgba(0, 255, 255, 0.5);
    }
    
    /* 美化 Metric 標籤與數值文字 */
    [data-testid="stMetricLabel"] {
        color: rgba(255,255,255,0.7) !important;
        font-size: 16px !important;
    }
    [data-testid="stMetricValue"] {
        color: #00ffff !important; /* 霓虹青色 */
        font-weight: bold !important;
        background: -webkit-linear-gradient(#00ffff, #0099ff); /* 文字漸層 */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* 5. 美化輸入框 */
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: #00ffff !important;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.5) !important;
    }

    /* 6. 【動態效果】：自訂 Fade-in (淡入) 動畫 */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* 將動畫應用在搜尋後的結果區域 */
    .stDataFrame, [data-testid="stHeader"] + div {
        animation: fadeIn 0.8s ease-out;
    }

</style>
""", unsafe_allow_html=True)

# ==============================
# 🧩 網頁內容與邏輯
# ==============================

# 側邊欄設定
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3014/3014385.png", width=80)
st.sidebar.markdown("<h2 style='text-align: center; color: white;'>設定條件</h2>", unsafe_allow_html=True)
selected_year = st.sidebar.selectbox("📅 選擇賽季", [2023, 2024, 2025])

# 主畫面 Banner
st.image("https://images.unsplash.com/photo-1508344928928-7165b67de128?w=1200&q=80", use_container_width=True)
st.title("⚾ MLB 砲火展示台 (霓虹動態版)")
st.markdown(f"這是一個自動修復、永遠穩定的打者數據庫，目前搜尋 **{selected_year}** 年數據。")

@st.cache_data
def load_data(year):
    try:
        df = pd.read_csv(f"mlb_{year}.csv")
        df.columns = df.columns.str.strip() # 自動修復欄位空格
        return df
    except Exception as e:
        st.error(f"找不到 {year} 年的資料檔案！請檢查 GitHub。", icon="🚨")
        return pd.DataFrame()

# 載入資料
data = load_data(selected_year)

if not data.empty:
    search_name = st.text_input("🔍 搜尋球員 (例如: Ohtani, Judge)", "")
    
    # 自動尋找姓名與球隊欄位
    name_col = 'Name' if 'Name' in data.columns else (data.columns[1] if len(data.columns) > 1 else data.columns[0])
    team_col = next((col for col in ['Tm', 'Team', 'team'] if col in data.columns), None)
    
    # 組合顯示欄位
    display_cols = [name_col, 'Age'] + ([team_col] if team_col else []) + ['G', 'HR', 'SB', 'BA', 'OBP', 'SLG', 'OPS']
    available_cols = [col for col in display_cols if col in data.columns]
    
    if search_name:
        # 搜尋功能 (astype確保不崩潰)
        filtered_data = data[data[name_col].astype(str).str.contains(search_name, case=False, na=False)]
        
        if not filtered_data.empty:
            st.success(f"找到了！共 {len(filtered_data)} 位球員", icon="✅")
            
            player = filtered_data.iloc[0]
            team_display = player[team_col] if team_col else "未知球隊"
            
            # 加上 Emoji 裝飾
            st.subheader(f"🏟️ {player[name_col]} ｜ 🛡️ {team_display}")
            
            # 【美化核心】：使用 Columns 進行 Metric 排版，CSS 會自動套用樣式
            col1, col2, col3, col4 = st.columns(4)
            col1.metric(label="🔥 全壘打 (HR)", value=player.get('HR', 0))
            col2.metric(label="🎯 打擊率 (BA)", value=player.get('BA', 0.0))
            col3.metric(label="💥 攻擊指數 (OPS)", value=player.get('OPS', 0.0))
            col4.metric(label="💨 盜壘 (SB)", value=player.get('SB', 0))
            
            st.markdown("---")
            st.write("📊 詳細數據表格：")
            # 表格會觸發 Fade-in 動畫
            st.dataframe(filtered_data[available_cols], use_container_width=True)
        else:
            st.warning("查無此人，請確認拼字。", icon="⚠️")
            
    else:
        st.info(f"💡 目前顯示 **{selected_year}** 年全聯盟數據預覽：", icon="💡")
        st.dataframe(data[available_cols].head(15), use_container_width=True)
