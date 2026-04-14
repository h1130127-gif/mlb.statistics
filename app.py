import streamlit as st
import pandas as pd

# 1. 網頁基本設定 (縮略圖與標題)
st.set_page_config(page_title="MLB 砲火展示台", page_icon="⚾", layout="wide")

# 2. 注入自訂 CSS 樣式 (保留霓虹動態版)
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
# 🗃️ 圖片資料庫 (保留完整的 30 隊 Logo)
# ==============================
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
    "TOT": "https://www.mlbstatic.com/team-logos/league-on-dark/mlb.svg" # 交易球員預設 Logo
}

# 球星照片字典 (保留現有設定)
PLAYER_PHOTOS = {
    "Shohei Ohtani": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/39832.png",
    "Aaron Judge": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/33192.png",
    "Mike Trout": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/30836.png",
    "Mookie Betts": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/33039.png",
    "Freddie Freeman": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/30193.png",
    "Juan Soto": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/39622.png"
}
# 預設圖片設定
DEFAULT_PLAYER_PHOTO = "https://cdn-icons-png.flaticon.com/512/166/166344.png"
DEFAULT_TEAM_LOGO = "https://www.mlbstatic.com/team-logos/league-on-dark/mlb.svg"

# ==============================
# 🧩 網頁內容排版與邏輯
# ==============================
# 側邊欄設定
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3014/3014385.png", width=80)
st.sidebar.markdown("<h2 style='text-align: center; color: white;'>設定條件</h2>", unsafe_allow_html=True)
selected_year = st.sidebar.selectbox("📅 選擇賽季", [2023, 2024, 2025])

# --- 【這裡就是修改的地方】 ---
# 主畫面 Banner (將原本的 Unsplash 網址換成 MLB 的 SVG Logo)
st.image("https://www.mlbstatic.com/team-logos/league-on-dark/mlb.svg", use_container_width=True)
# -----------------------------

st.title("⚾ MLB")

# 數據載入函數
@st.cache_data
def load_data(year):
    try:
        df = pd.read_csv(f"mlb_{year}.csv")
        # 清除欄位空格
        df.columns = df.columns.str.strip()
        return df
    except Exception:
        # 找不到檔案時回傳空表格，不讓程式崩潰
        return pd.DataFrame()

# 執行載入
data = load_data(selected_year)

# 網頁主體邏輯
if not data.empty:
    search_name = st.text_input("🔍 搜尋球員 (例如: Ohtani, Judge, Soto)", "")
    
    # 自動抓取姓名與球隊欄位名稱
    name_col = 'Name' if 'Name' in data.columns else (data.columns[1] if len(data.columns) > 1 else data.columns[0])
    team_col = next((col for col in ['Tm', 'Team', 'team'] if col in data.columns), None)
    
    if search_name:
        # 進行搜尋
        filtered_data = data[data[name_col].astype(str).str.contains(search_name, case=False, na=False)]
        
        if not filtered_data.empty:
            st.success(f"找到了！共 {len(filtered_data)} 位球員", icon="✅")
            
            # 取第一筆結果做詳細顯示
            player = filtered_data.iloc[0]
            # 取得球隊縮寫，沒有時預設為 TOT
            team_code = player[team_col] if team_col else "TOT"
            
            # 【視覺排版】：大頭照與球隊資訊
            st.markdown("<br>", unsafe_allow_html=True) # 加一點空白
            col_pic, col_info = st.columns([1, 5])
            
            with col_pic:
                # 顯示球員照片
                st.image(PLAYER_PHOTOS.get(player[name_col], DEFAULT_PLAYER_PHOTO), width=120)
                
            with col_info:
                # 顯示名字
                st.markdown(f"<h2 style='margin-bottom:0;'>{player[name_col]}</h2>", unsafe_allow_html=True)
                # 顯示球隊 Logo 與縮寫
                st.markdown(f"""
                    <div style='display: flex; align-items: center; gap: 10px; margin-top: 5px;'>
                        <img src='{TEAM_LOGOS.get(team_code, DEFAULT_TEAM_LOGO)}' width='35'>
                        <span style='font-size: 1.2em; color: #ccc;'>{team_code}</span>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 【視覺排版】：數據看板
            c1, c2, c3, c4 = st.columns(4)
            # 使用 CSS 霓虹特效
            c1.metric(label="🔥 全壘打 (HR)", value=player.get('HR', 0))
            c2.metric(label="🎯 打擊率 (BA)", value=player.get('BA', 0.0))
            c3.metric(label="💥 攻擊指數 (OPS)", value=player.get('OPS', 0.0))
            c4.metric(label="💨 盜壘 (SB)", value=player.get('SB', 0))
            
            st.markdown("---")
            st.write("📊 詳細數據表格：")
            # 顯示表格
            st.dataframe(filtered_data, use_container_width=True)
        else:
            st.warning("查無此人，請確認拼字。", icon="⚠️")
            
    else:
        # 未搜尋時顯示預覽
        st.info(f"💡 目前顯示 {selected_year} 年數據預覽")
        st.dataframe(data.head(15), use_container_width=True)
