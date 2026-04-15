import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 網頁基本設定
st.set_page_config(page_title="MLB 數據看板", page_icon="⚾", layout="wide")

# 2. 注入自訂 CSS 樣式
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #1e3c72 0%, #1a237e 40%, #0d1117 100%); color: white; }
    [data-testid="stSidebar"] { background-color: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); }
    h1, h2, h3, p, span { color: white !important; font-family: 'Open Sans', sans-serif; }
    
    [data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px; padding: 20px 15px; transition: all 0.3s ease-in-out;
    }
    
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
    
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { color: #ccc !important; font-weight: bold; }
    .stTabs [aria-selected="true"] { color: #00ffff !important; }
</style>
""", unsafe_allow_html=True)

# ==============================
# 🗃️ 圖片與字典設定
# ==============================
MLB_HTML_LOGO = "https://upload.wikimedia.org/wikipedia/commons/a/a6/Major_League_Baseball_logo.svg"

TEAM_LOGOS = {
    "ATL": "https://a.espncdn.com/i/teamlogos/mlb/500/atl.png", "MIA": "https://a.espncdn.com/i/teamlogos/mlb/500/mia.png",
    "NYM": "https://a.espncdn.com/i/teamlogos/mlb/500/nym.png", "PHI": "https://a.espncdn.com/i/teamlogos/mlb/500/phi.png",
    "LAD": "https://a.espncdn.com/i/teamlogos/mlb/500/lad.png", "SDP": "https://a.espncdn.com/i/teamlogos/mlb/500/sd.png",
    "SFG": "https://a.espncdn.com/i/teamlogos/mlb/500/sf.png", "BAL": "https://a.espncdn.com/i/teamlogos/mlb/500/bal.png",
    "BOS": "https://a.espncdn.com/i/teamlogos/mlb/500/bos.png", "NYY": "https://a.espncdn.com/i/teamlogos/mlb/500/nyy.png",
    "HOU": "https://a.espncdn.com/i/teamlogos/mlb/500/hou.png", "TEX": "https://a.espncdn.com/i/teamlogos/mlb/500/tex.png",
    "TOT": "https://cdn-icons-png.flaticon.com/512/3014/3014385.png" 
}

PLAYER_PHOTOS = {
    "Shohei Ohtani": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/39832.png",
    "Mookie Betts": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/33039.png",
    "Freddie Freeman": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/30193.png",
    "Aaron Judge": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/33192.png",
    "Juan Soto": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/39622.png",
    "Bryce Harper": "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/31696.png",
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

# 🔥 這個就是剛剛弄丟的「圖表美化工具」
def create_beautiful_chart(df, y_col, line_color, y_label):
    fig = px.line(df, x="Year", y=y_col, text=y_col, markers=True)
    fig.update_traces(
        line_color=line_color, 
        marker=dict(size=12, color="white", line=dict(width=2, color=line_color)),
        textposition="top center", 
        textfont=dict(size=14, color="white")
    )
    fig.update_layout(
        xaxis_title="📅 賽季年份 (Year)",
        yaxis_title=y_label,
        plot_bgcolor="rgba(255,255,255,0.05)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(showgrid=False, type='category'),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    return fig

data = load_data(selected_year)

if not data.empty:
    search_name = st.text_input("🔍 搜尋球員名字 (例如: Ohtani, Judge, Soto)", "")
    
    # 根據你的截圖，動態抓取 Player 和 Team 欄位
    name_col = 'Player' if 'Player' in data.columns else ('Name' if 'Name' in data.columns else data.columns[1])
    team_col = next((col for col in ['Team', 'Tm', 'team'] if col in data.columns), None)
    
    if search_name:
        filtered_data = data[data[name_col].astype(str).str.contains(search_name, case=False, na=False)]
        
        if not filtered_data.empty:
            player = filtered_data.iloc[0]
            team_code = player[team_col] if team_col else "TOT"
            
            # 清除名字後面的 * 或 # 以便抓取照片
            clean_name = player[name_col].replace('*', '').replace('#', '').strip()
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_pic, col_info = st.columns([1, 5])
            
            with col_pic:
                st.image(PLAYER_PHOTOS.get(clean_name, DEFAULT_PLAYER_PHOTO), width=120)
                
            with col_info:
                st.markdown(f"<h2 style='margin-bottom:0;'>{player[name_col]}</h2>", unsafe_allow_html=True)
                st.markdown(f"""
                    <div style='display: flex; align-items: center; gap: 10px; margin-top: 5px;'>
                        <img src='{TEAM_LOGOS.get(team_code, "https://cdn-icons-png.flaticon.com/512/3014/3014385.png")}' width='35'>
                        <span style='font-size: 1.2em; color: #ccc;'>{team_code}</span>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- 四大數據看板 (加上防呆格式) ---
            c1, c2, c3, c4 = st.columns(4)
            c1.metric(label="🔥 全壘打 (HR)", value=int(player.get('HR', 0)))
            c2.metric(label="🎯 打擊率 (BA)", value=f"{float(player.get('BA', 0.0)):.3f}")
            c3.metric(label="💥 攻擊指數 (OPS)", value=f"{float(player.get('OPS', 0.0)):.3f}")
            c4.metric(label="💨 盜壘 (SB)", value=int(player.get('SB', 0)))
            
            st.markdown("---")
            
            # ==========================================
            # 📈 Plotly 升級版：跨賽季數據軌跡
            # ==========================================
            st.markdown("### 📈 跨賽季數據軌跡 (2023 - 2025)")
            
            trend_records = []
            for y in [2023, 2024, 2025]:
                df_year = load_data(y)
                if not df_year.empty and name_col in df_year.columns:
                    p_match = df_year[df_year[name_col].astype(str).str.contains(search_name, case=False, na=False)]
                    if not p_match.empty:
                        trend_records.append({
                            "Year": str(y),
                            "HR": float(p_match.iloc[0].get('HR', 0)),
                            "OPS": float(p_match.iloc[0].get('OPS', 0.0)),
                            "BA": float(p_match.iloc[0].get('BA', 0.0))
                        })
            
            if len(trend_records) > 0:
                trend_df = pd.DataFrame(trend_records).sort_values(by="Year")
                
                tab1, tab2, tab3 = st.tabs(["🔥 全壘打趨勢", "💥 OPS 趨勢", "🎯 打擊率趨勢"])
                
                with tab1:
                    fig_hr = create_beautiful_chart(trend_df, "HR", "#ff4b4b", "⚾ 全壘打總數 (支)")
                    st.plotly_chart(fig_hr, use_container_width=True)
                with tab2:
                    fig_ops = create_beautiful_chart(trend_df, "OPS", "#00ffff", "💥 攻擊指數 (OPS)")
                    st.plotly_chart(fig_ops, use_container_width=True)
                with tab3:
                    fig_ba = create_beautiful_chart(trend_df, "BA", "#00ff00", "🎯 打擊率 (AVG)")
                    st.plotly_chart(fig_ba, use_container_width=True)
            else:
                st.info("📊 尚未累積足夠的歷史賽季數據。")
            
            st.markdown("---")
            
            # ==========================================
            # 📋 表格美化：Pandas Style 魔術 (小數點嚴格控制)
            # ==========================================
            st.markdown("### 📋 詳細數據表")
            
            format_dict = {}
            if 'BA' in filtered_data.columns: format_dict['BA'] = "{:.3f}"
            if 'OBP' in filtered_data.columns: format_dict['OBP'] = "{:.3f}"
            if 'SLG' in filtered_data.columns: format_dict['SLG'] = "{:.3f}"
            if 'OPS' in filtered_data.columns: format_dict['OPS'] = "{:.3f}"
            if 'HR' in filtered_data.columns: format_dict['HR'] = "{:.0f}"
            if 'SB' in filtered_data.columns: format_dict['SB'] = "{:.0f}"
            if 'RBI' in filtered_data.columns: format_dict['RBI'] = "{:.0f}"

            styled_df = filtered_data.style.format(format_dict)
            
            if 'HR' in filtered_data.columns:
                styled_df = styled_df.background_gradient(cmap="YlOrRd", subset=["HR"])
                
            st.dataframe(styled_df, hide_index=True, use_container_width=True)
            
        else:
            st.warning("查無此人，請確認拼字。", icon="⚠️")
            
    else:
        st.info(f"💡 目前顯示 {selected_year} 年數據預覽")
        
        format_dict_preview = {}
        if 'BA' in data.columns: format_dict_preview['BA'] = "{:.3f}"
        if 'OBP' in data.columns: format_dict_preview['OBP'] = "{:.3f}"
        if 'SLG' in data.columns: format_dict_preview['SLG'] = "{:.3f}"
        if 'OPS' in data.columns: format_dict_preview['OPS'] = "{:.3f}"
        if 'HR' in data.columns: format_dict_preview['HR'] = "{:.0f}"
        
        preview_df = data.head(15).style.format(format_dict_preview)
        
        if 'HR' in data.columns:
            preview_df = preview_df.background_gradient(cmap="YlOrRd", subset=["HR"])
            
        st.dataframe(preview_df, hide_index=True, use_container_width=True)
        
else:
    st.error(f"找不到 mlb_{selected_year}.csv 檔案，請確認檔案已上傳至 GitHub。", icon="📂")
