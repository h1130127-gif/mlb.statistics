import streamlit as st
import pandas as pd

# 1. 網頁基本設定
st.set_page_config(page_title="MLB 砲火展示台", page_icon="⚾", layout="wide")

# 2. 注入自訂 CSS 樣式 (霓虹動態版)
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #1e3c72 0%, #1a237e 40%, #0d1117 100%); color: white; }
    [data-testid="stSidebar"] { background-color: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); }
    h1, h2, h3, p, span { color: white !important; font-family: 'Open Sans', sans-serif; }
    [data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px; padding: 20px 15px; transition: all 0.3s ease-in-out;
    }
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px); background-color: rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 20px rgba(0, 255, 255, 0.3); border-color: rgba(0, 255, 255, 0.5);
    }
    [data-testid="stMetricValue"] {
        color: #00ffff !important; font-weight: bold !important;
        background: -webkit-linear-gradient(#00ffff, #0099ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .stTextInput>div>div>input { background-color: rgba(255, 255, 255, 0.1) !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# ==============================
# 🗃️ 圖片資料庫 (這裡就是你剛剛問要替換的部分)
# ==============================
TEAM_LOGOS = {
    # 國家聯盟
    "ATL": "https://a.espncdn.com/i/teamlogos/mlb/500/atl.png", "MIA": "https://a.espncdn.com/i/teamlogos/mlb/500/mia.png",
    "NYM": "https://a.espncdn.com/i/teamlogos/mlb/500/nym.png", "PHI": "https://a.espncdn.com/i/teamlogos/mlb/500/phi.png",
    "WSN": "https://a.espncdn.com/i/teamlogos/mlb/500/wsh.png", "CHC": "https://a.espncdn.com/i/teamlogos/mlb/500/chc.png",
    "CIN": "https://a.espncdn.com/i/teamlogos/mlb/500/cin.png", "MIL": "https://a.espncdn.com/i/teamlogos/mlb/500/mil.png",
    "PIT": "https://a.espncdn.com/i/teamlogos/mlb/500/pit.png", "STL": "https://a.espncdn.com/i/teamlogos/mlb/500/stl.png",
    "ARI": "https://a.espncdn.com/i/teamlogos/mlb/500/ari.png", "COL": "https://a.espncdn.com/i/teamlogos/mlb/500/col.png",
    "LAD": "https://a.espncdn.com/i/teamlogos/mlb/500/lad.png", "SDP": "https://a.espncdn.com/i/teamlogos/mlb/500/sd.png",
    "SFG": "https://a.espncdn.com/i/teamlogos/mlb/500/sf.png",
    # 美國聯盟
    "BAL": "https://a.espncdn.com/i/teamlogos/mlb/500/bal.png", "BOS": "https://a.espncdn.com/i/teamlogos/mlb/500/bos.png",
    "NYY": "https://a.espncdn.com/i/teamlogos/mlb/500/nyy.png", "TBR": "https://a.espncdn.com/i/teamlogos/mlb/500/tb.png",
    "TOR": "https://a.espncdn.com/i/teamlogos/mlb/500/tor.png", "CHW": "https://a.espncdn.com/i/teamlogos/mlb/500/chw.png",
    "CLE": "https://a.espncdn.com/i/teamlogos/mlb/500/cle.png", "DET": "https://a.espncdn.com/i/teamlogos/mlb/500/det.png",
    "KCR": "https://a.espncdn.com/i/teamlogos/mlb/500/kc.png",  "MIN": "https://a.espncdn.com/i/teamlogos/mlb/500/min.png",
    "HOU": "https://a.espncdn.com/i/teamlogos/mlb/500/hou.png", "LAA": "https://a.espncdn.com/i/teamlogos/mlb/500/laa.png",
    "OAK": "https://a.espncdn.com/i/teamlogos/mlb/500/oak.png", "SEA": "https://a.espncdn.com/i/teamlogos/mlb/500/sea.png",
    "TEX": "https://a.espncdn.com/i/teamlogos/mlb/500/tex.png", "TOT": "https://www.mlbstatic.com/team-logos/league-on-dark/mlb.svg"
}

PLAYER_PHOTOS = {
    "Shohei Ohtani": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/39832.png",
    "Aaron Judge": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/33192.png",
    "Mike Trout": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/30836.png",
    "Mookie Betts": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/33039.png",
    "Freddie Freeman": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/30193.png",
    "Juan Soto": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/39622.png"
}
DEFAULT_PLAYER_PHOTO = "https://cdn-icons-png.flaticon.com/512/166/166344.png"
DEFAULT_TEAM_LOGO = "https://www.mlbstatic.com/team-logos/league-on-dark/mlb.svg"

# ==============================
# 🧩 網頁邏輯
# ==============================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3014/3014385.png", width=80)
st.sidebar.markdown("<h2 style='text-align: center; color: white;'>設定條件</h2>", unsafe_allow_html=True)
selected_year = st.sidebar.selectbox("📅 選擇賽季", [2023, 2022, 2021])

st.image("https://images.unsplash.com/photo-1508344928928-7165b67de128?w=1200&q=80", use_container_width=True)
st.title("⚾ MLB 砲火展示台")

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
    search_name = st.text_input("🔍 搜尋球員 (例如: Ohtani, Judge, Soto)", "")
    
    # 自動抓欄位名稱
    name_col = 'Name' if 'Name' in data.columns else (data.columns[1] if len(data.columns) > 1 else data.columns[0])
    team_col = next((col for col in ['Tm', 'Team', 'team'] if col in data.columns), None)
    
    if search_name:
        filtered_data = data[data[name_col].astype(str).str.contains(search_name, case=False, na=False)]
        
        if not filtered_data.empty:
            player = filtered_data.iloc[0]
            team_code = player[team_col] if team_col else "TOT"
            
            # 顯示球員照片與球隊 Logo
            st.markdown("<br>", unsafe_allow_html=True)
            col_pic, col_info = st.columns([1, 5])
            with col_pic:
                st.image(PLAYER_PHOTOS.get(player[name_col], DEFAULT_PLAYER_PHOTO), width=120)
            with col_info:
                st.markdown(f"<h2 style='margin-bottom:0;'>{player[name_col]}</h2>", unsafe_allow_html=True)
                st.markdown(f"""
                    <div style='display: flex; align-items: center; gap: 10px; margin-top: 5px;'>
                        <img src='{TEAM_LOGOS.get(team_code, DEFAULT_TEAM_LOGO)}' width='35'>
                        <span style='font-size: 1.2em; color: #ccc;'>{team_code}</span>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            # 數據看板
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("🔥 HR", player.get('HR', 0))
            c2.metric("🎯 BA", player.get('BA', 0.0))
            c3.metric("💥 OPS", player.get('OPS', 0.0))
            c4.metric("💨 SB", player.get('SB', 0))
            
            st.markdown("---")
            st.dataframe(filtered_data, use_container_width=True)
    else:
        st.info(f"💡 目前顯示 {selected_year} 年數據預覽")
        st.dataframe(data.head(15), use_container_width=True)
