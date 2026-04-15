import streamlit as st
import pandas as pd

# 1. 網頁基本設定
st.set_page_config(page_title="MLB 數據看板", page_icon="⚾", layout="wide")

# 2. 注入自訂 CSS 樣式 (極致核彈級修復)
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #1e3c72 0%, #1a237e 40%, #0d1117 100%); color: white; }
    [data-testid="stSidebar"] { background-color: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); }
    h1, h2, h3, p, span { color: white !important; font-family: 'Open Sans', sans-serif; }
    
    [data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px; padding: 20px 15px; transition: all 0.3s ease-in-out;
    }
    
    /* 🔥 終極輸入框修復：雪地寫黑字 */
    .stTextInput [data-baseweb="input"] {
        background-color: #ffffff !important;
        border: 2px solid #00ffff !important;
        border-radius: 8px !important;
    }
    .stTextInput input {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        caret-color: #000000 !important;
        font-weight: bold !important;
        font-size: 18px !important;
        background-color: transparent !important;
    }
    .stTextInput label { color: #00ffff !important; font-weight: bold !important; font-size: 1.1em !important; }
    
    /* Tabs 標籤頁樣式微調 */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { color: #ccc !important; font-weight: bold; }
    .stTabs [aria-selected="true"] { color: #00ffff !important; }
</style>
""", unsafe_allow_html=True)

# ==============================
# 🗃️ 圖片與字典設定 (豪華擴充版)
# ==============================
MLB_HTML_LOGO = "https://upload.wikimedia.org/wikipedia/commons/a/a6/Major_League_Baseball_logo.svg"

TEAM_LOGOS = {
    "ATL": "https://a.espncdn.com/i/teamlogos/mlb/500/atl.png", "MIA": "https://a.espncdn.com/i/teamlogos/mlb/500/mia.png",
    "NYM": "https://a.espncdn.com/i/teamlogos/mlb/500/nym.png", "PHI": "https://a.espncdn.com/i/teamlogos/mlb/500/phi.png",
    "WSN": "https://a.espncdn.com/i/teamlogos/mlb/500/wsh.png", "CHC": "https://a.espncdn.com/i/teamlogos/mlb/500/chc.png",
    "CIN": "https://a.espncdn.com/i/teamlogos/mlb/500/cin.png", "MIL": "https://a.espncdn.com/i/teamlogos/mlb/500/mil.png",
    "PIT": "https://a.espncdn.com/i/teamlogos/mlb/500/pit.png", "STL": "https://a.espncdn.com/i/teamlogos/mlb/500/stl.png",
    "ARI": "https://a.espncdn.com/i/teamlogos/mlb/500/ari.png", "COL": "https://a.espncdn.com/i/teamlogos/mlb/500/col.png",
    "LAD": "https://a.espncdn.com/i/teamlogos/mlb/500/lad.png", "SDP": "https://a.espncdn.com/i/teamlogos/mlb/500/sd.png",
    "SFG": "https://a.espncdn.com/i/teamlogos/mlb/500/sf.png", "BAL": "https://a.espncdn.com/i/teamlogos/mlb/500/bal.png",
    "BOS": "https://a.espncdn.com/i/teamlogos/mlb/500/bos.png", "NYY": "https://a.espncdn.com/i/teamlogos/mlb/500/nyy.png",
    "TBR": "https://a.espncdn.com/i/teamlogos/mlb/500/tb.png",  "TOR": "https://a.espncdn.com/i/teamlogos/mlb/500/tor.png",
    "CHW": "https://a.espncdn.com/i/teamlogos/mlb/500/chw.png", "CLE": "https://a.espncdn.com/i/teamlogos/mlb/500/cle.png",
    "DET": "https://a.espncdn.com/i/teamlogos/mlb/500/det.png", "KCR": "https://a.espncdn.com/i/teamlogos/mlb/500/kc.png",
    "MIN": "https://a.espncdn.com/i/teamlogos/mlb/500/min.png", "HOU": "https://a.espncdn.com/i/teamlogos/mlb/500/hou.png",
    "LAA": "https://a.espncdn.com/i/teamlogos/mlb/500/laa.png", "OAK": "https://a.espncdn.com/i/teamlogos/mlb/500/oak.png",
    "SEA": "https://a.espncdn.com/i/teamlogos/mlb/500/sea.png", "TEX": "https://a.espncdn.com/i/teamlogos/mlb/500/tex.png",
    "TOT": "https://cdn-icons-png.flaticon.com/512/3014/3014385.png" 
}

PLAYER_PHOTOS = {
    "Shohei Ohtani": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/39832.png",
    "Mookie Betts": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/33039.png",
    "Freddie Freeman": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/30193.png",
    "Aaron Judge": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/33192.png",
    "Juan Soto": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/39622.png",
    "Gerrit Cole": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/32081.png",
    "Bryce Harper": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/31696.png",
    "Ronald Acuna Jr.": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/39459.png",
    "Fernando Tatis Jr.": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/35983.png",
    "Manny Machado": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/31097.png",
    "Pete Alonso": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/37498.png",
    "Mike Trout": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/30836.png",
    "Vladimir Guerrero Jr.": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/35002.png",
    "Francisco Lindor": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/32129.png",
    "Yordan Alvarez": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/39876.png"
}
DEFAULT_PLAYER_PHOTO = "https://cdn-icons-png.flaticon.com/512/166/166344.png"

# ==============================
# 🧩 網頁內容排版與邏輯
# ==============================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3014/3014385.png", width=80)
st.sidebar.markdown("<h2 style='text-align: center; color: white;'>設定條件</h2>", unsafe_allow_html=True)
selected_year = st.sidebar.selectbox("📅 選擇賽季", [2025, 2024, 2023])

# --- MLB Logo ---
st.markdown(f"""
    <div style="display: flex; justify-content: center; margin-bottom: 20px;">
        <img src="{MLB_HTML_LOGO}" width="200" alt="MLB Logo">
    </div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(year):
    try:
        df = pd.read_csv(f"mlb_{year}.csv")
        df.columns = df.columns.str.strip()
        return df
    except Exception:
        return pd.DataFrame()

data = load_data(selected_year)

if not data.empty:
    search_name = st.text_input("🔍 搜尋球員名字 (例如: Ohtani, Judge, Soto)", "")
    
    name_col = 'Name' if 'Name' in data.columns else (data.columns[1] if len(data.columns) > 1 else data.columns[0])
    team_col = next((col for col in ['Tm', 'Team', 'team'] if col in data.columns), None)
    
    if search_name:
        filtered_data = data[data[name_col].astype(str).str.contains(search_name, case=False, na=False)]
        
        if not filtered_data.empty:
            player = filtered_data.iloc[0]
            team_code = player[team_col] if team_col else "TOT"
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_pic, col_info = st.columns([1, 5])
            
            with col_pic:
                st.image(PLAYER_PHOTOS.get(player[name_col], DEFAULT_PLAYER_PHOTO), width=120)
                
            with col_info:
                st.markdown(f"<h2 style='margin-bottom:0;'>{player[name_col]}</h2>", unsafe_allow_html=True)
                st.markdown(f"""
                    <div style='display: flex; align-items: center; gap: 10px; margin-top: 5px;'>
                        <img src='{TEAM_LOGOS.get(team_code, "https://cdn-icons-png.flaticon.com/512/3014/3014385.png")}' width='35'>
                        <span style='font-size: 1.2em; color: #ccc;'>{team_code}</span>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- 顯示當前選擇年份的數據 ---
            c1, c2, c3, c4 = st.columns(4)
            c1.metric(label="🔥 全壘打 (HR)", value=player.get('HR', 0))
            c2.metric(label="🎯 打擊率 (BA)", value=player.get('BA', 0.0))
            c3.metric(label="💥 攻擊指數 (OPS)", value=player.get('OPS', 0.0))
            c4.metric(label="💨 盜壘 (SB)", value=player.get('SB', 0))
            
            st.markdown("---")
            
            # 🔥 表格美化：使用 Pandas Style 魔術
            st.markdown("### 📋 詳細數據表")
            
            # 給搜尋結果表格加上顏色漸層和小數點格式
            styled_df = filtered_data.style.format({
                "BA": "{:.3f}",   # 打擊率強制顯示三位小數 (例如 0.300)
                "OPS": "{:.3f}"   # OPS 也顯示三位小數
            }).background_gradient(
                cmap="YlOrRd",    # 設定顏色主題為 黃(Yl) -> 橘(Or) -> 紅(Rd)
                subset=["HR"]     # 指定只有「全壘打(HR)」欄位要套用這個熱力圖效果
            )
            
            st.dataframe(styled_df, hide_index=True, use_container_width=True)
            
        else:
            st.warning("查無此人，請確認拼字。", icon="⚠️")
            
    else:
        st.info(f"💡 目前顯示 {selected_year} 年數據預覽")
        
        # 首頁的預覽表格也一起加上漸層魔法！
        preview_df = data.head(15).style.format({
            "BA": "{:.3f}",
            "OPS": "{:.3f}"
        }).background_gradient(
            cmap="YlOrRd", 
            subset=["HR"]
        )
        
        st.dataframe(preview_df, hide_index=True, use_container_width=True)
else:
    st.error(f"找不到 mlb_{selected_year}.csv 檔案，請確認檔案已上傳至 GitHub。", icon="📂")
