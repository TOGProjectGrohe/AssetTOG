import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บพื้นฐานให้กระชับเข้ามุมมองสไตล์สมาร์ทโฟน
st.set_page_config(page_title="TOG App", layout="centered", initial_sidebar_state="collapsed")

# 2. 🛠️ ชุดคำสั่งดักทำลายป้ายแอดมิน และบังคับแถบปุ่มนำทางชิดขอบบนสุด 100%
st.markdown("""
    <style>
    /* 🚫 ซ่อนปุ่มแอดมิน, ปุ่มเครื่องมือ และป้าย Deploy ดั้งเดิมของ Streamlit ทั้งหมด */
    .stDeployButton, 
    [data-testid="stHeader"], 
    [data-testid="stToolbar"], 
    [data-testid="stDecoration"],
    header, 
    footer,
    #MainMenu {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }
    
    /* 🚫 ดักฝังบล็อกเลเยอร์ซ่อนปุ่มป้ายวงกลมเขียว (Manage App) บนหน้าจอมือถือไม่ให้โผล่ที่มุมขวาล่าง */
    [data-testid="stStatusWidget"], 
    #stConnectionStatus,
    .st-emotion-cache-zq59db,
    .st-emotion-cache-1wb763a,
    .st-emotion-cache-6q9sum,
    .st-emotion-cache-15z78k,
    .st-emotion-cache-b9st7z,
    .st-emotion-cache-h5g6vv,
    div[class*="viewerBadge"],
    div[class*="st-emotion-cache-"] button[title="Manage app"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0 !important;
    }

    /* 📱 ดีไซน์คุมธีมหน้าจอมือถือ ส้มพาสเทลสวยงาม */
    .stApp {
        max-width: 420px !important;
        margin: 0px auto !important;
        background: linear-gradient(180deg, #ffb07c 0%, #ffe3d1 30%, #fff7f2 100%) !important;
        border: 12px solid #1e293b !important;
        border-radius: 40px !important;
        padding: 65px 24px 24px 24px !important; /* เว้นระยะด้านบนให้พอดีกับปุ่มนำทางชิดขอบ */
        box-shadow: 0 20px 50px rgba(0,0,0,0.3) !important;
        min-height: 90vh !important;
        height: auto !important;
    }
    
    /* เคลียร์ระยะห่างของ Vertical Block เพื่อความกระชับ */
    div[data-testid="stVerticalBlock"] > div,
    div[data-testid="element-container"],
    [data-testid="stVerticalBlock"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0px !important;
        margin: 0px !important;
    }

    /* กล่องพื้นหลังขาวสำหรับ Content */
    .login-card {
        background-color: white !important;
        border-radius: 20px !important;
        padding: 15px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 15px !important;
    }

    /* 🎯 จัดการแถบนำทางให้อยู่ "ขอบบนสุดของโทรศัพท์" ไม่ให้ทับซ้อนกับโลโก้ */
    .custom-top-navbar {
        position: absolute !important;
        top: 0px !important; /* ดันกระชากขึ้นไปแตะขอบบนสุดของกรอบมือถือ */
        left: 0px !important;
        right: 0px !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        padding: 20px 24px 0px 24px !important; /* ใช้พื้นที่ภายในคุมระยะห่าง */
        z-index: 999999 !important;
    }
    
    /* ดีไซน์ปุ่มลิงก์นำทางแบบโค้งมน */
    .nav-btn-link {
        background-color: #007bc3 !important;
        color: white !important;
        border-radius: 20px !important;
        padding: 8px 16px !important;
        font-size: 13px !important;
        font-weight: bold !important;
        text-decoration: none !important;
        display: inline-block !important;
        box-shadow: 0 4px 10px rgba(0, 123, 195, 0.25) !important;
        white-space: nowrap !important;
    }
    .nav-btn-link:hover {
        background-color: #0c2340 !important;
    }

    /* ปรับแต่งปุ่มสไตล์ Streamlit ด้านล่าง */
    div.stButton > button {
        background-color: #007bc3 !important;
        color: white !important;
        border-radius: 30px !important;
        padding: 12px 0px !important;
        font-weight: bold !important;
        font-size: 15px !important;
        border: none !important;
        width: 100% !important;
    }
    
    /* ระบบสไลด์กราฟซ้าย-ขวาบนมือถือ */
    .scrollable-graph-container {
        width: 100% !important;
        overflow-x: auto !important;
        display: block !important;
        margin-bottom: 20px !important;
    }
    .inner-graph-box {
        width: 600px !important;
        display: block !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 📊 ฟังก์ชันดึงข้อมูลจาก Google Sheets
@st.cache_data(ttl=15)
def get_graph_data(target_error):
    sheet_id = "1qKY4ZBWYXM81Y8BZSMjOf7z1hJXeJFCjB5KeRPQBe4c"
    gid = "0"
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    try:
        raw_df = pd.read_csv(csv_url)
        raw_df.columns = raw_df.columns.str.strip()
        raw_df['errortype'] = pd.to_numeric(raw_df['errortype'], errors='coerce')
        raw_df['rework quantity'] = pd.to_numeric(raw_df['rework quantity'], errors='coerce').fillna(0)
        filtered_df = raw_df[raw_df['errortype'] == target_error]
        grouped_df = filtered_df.groupby('Material', as_index=False)['rework quantity'].sum()
        top_10 = grouped_df.sort_values(by='rework quantity', ascending=False).head(10)
        top_10['Material'] = top_10['Material'].astype(str)
        return top_10
    except:
        return pd.DataFrame(columns=['Material', 'rework quantity'])

# 4. ตรวจสอบสถานะหน้าเพจผ่าน Query Parameters
if "nav" not in st.query_params:
    st.query_params["nav"] = "login"

current_page = st.query_params["nav"]

# --- 🎯 แถบปุ่มนำทาง (เกาะติดมุมบนสุดอย่างแท้จริง ไม่แตกแถว และไม่ทับซ้อน) ---
st.markdown("""
<div class="custom-top-navbar">
    <a href="?nav=login" target="_self" class="nav-btn-link">🏠 Home</a>
    <a href="?nav=login" target="_self" class="nav-btn-link">🚪 Logout</a>
</div>
""", unsafe_allow_html=True)

# --- ส่วนหัวโลโก้ (ขยับระยะลงมาเพื่อเปิดพื้นที่ให้ปุ่มนำทางด้านบนอย่างสวยงาม) ---
st.markdown("""
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 25px; margin-top: 25px;">
    <div style="width: 45px; height: 45px; background-color: #000; border-radius: 50%; display: flex; justify-content: center; align-items: center; color: #fff; font-weight: bold; font-size: 14px;">TOG</div>
    <div>
        <small style="color:#fff; opacity:0.8; display:block; font-size:11px;">ยินดีต้อนรับ</small>
        <span style="font-size:16px; font-weight:600; color:white;">TOG App</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- หน้าแรก: Login ----------------
if current_page == "login":
    st.markdown('<div style="background:rgba(255,255,255,0.4); border:1px solid rgba(255,255,255,0.5); border-radius:20px; padding:15px; text-align:center; color:#2c3e50; font-weight:bold; margin-bottom:20px;">✨ ปรับปรุงประสิทธิภาพการทำงานอย่างต่อเนื่อง</div>', unsafe_allow_html=True)

    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:18px; margin-top:0; color:#2c3e50;'>🪪 ส่วนพนักงานเข้าใช้งาน</h3>", unsafe_allow_html=True)

    enable_camera = st.checkbox("เปิดสิทธิ์ใช้งานกล้องถ่ายรูป", value=True)
    if enable_camera:
        st.markdown("<p style='font-size:13px; color:#64748b; margin-top:10px;'>สแกน QR Code พนักงานของคุณ</p>", unsafe_allow_html=True)
        picture = st.camera_input("", label_visibility="collapsed")
        if picture:
            st.query_params["nav"] = "dashboard"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="text-align: center; width: 100%; margin-top: 35px;"><div style="color:#2c3e50; font-size:16px; margin-bottom:15px; font-weight:500;">ต้องการดูข้อมูลสรุปโดยไม่ล็อกอิน?</div></div>', unsafe_allow_html=True)
    
    if st.button("📊 ดูภาพรวม Dashboard", key="btn_login_dash"):
        st.query_params["nav"] = "dashboard"
        st.rerun()

# ---------------- หน้าสอง: Dashboard (3 กราฟแยกสี) ----------------
elif current_page == "dashboard":
    st.markdown('<div style="text-align:center; font-size:20px; font-weight:bold; color:#2c3e50; margin-bottom:15px;">📊 สรุปภาพรวม Dashboard</div>', unsafe_allow_html=True)
    st.caption("👉 ใช้นิ้วปัดเลื่อนซ้าย-ขวาที่ตัวกราฟ เพื่อดูอันดับชิ้นงานเพิ่มเติมได้")

    # กราฟที่ 1
    st.markdown('<div class="login-card"><b>🔥 Defect 260 (Rough Lines)</b></div>', unsafe_allow_html=True)
    df_260 = get_graph_data(260)
    if not df_260.empty:
        st.markdown('<div class="scrollable-graph-container"><div class="inner-graph-box">', unsafe_allow_html=True)
        fig_260 = px.bar(df_260, x='Material', y='rework quantity', text='rework quantity')
        fig_260.update_traces(textposition='outside', marker_color='#ff7f0e')
        fig_260.update_layout(xaxis=dict(type='category', tickangle=45), yaxis=dict(tickformat='d'), margin=dict(l=10, r=10, t=25, b=50), height=250, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_260, use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    # กราฟที่ 2
    st.markdown('<div class="login-card"><b>⚡ Defect 261 (Grinding Structure Visible)</b></div>', unsafe_allow_html=True)
    df_261 = get_graph_data(261)
    if not df_261.empty:
        st.markdown('<div class="scrollable-graph-container"><div class="inner-graph-box">', unsafe_allow_html=True)
        fig_261 = px.bar(df_261, x='Material', y='rework quantity', text='rework quantity')
        fig_261.update_traces(textposition='outside', marker_color='#002060')
        fig_261.update_layout(xaxis=dict(type='category', tickangle=45), yaxis=dict(tickformat='d'), margin=dict(l=10, r=10, t=25, b=50), height=250, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_261, use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    # กราฟที่ 3
    st.markdown('<div class="login-card"><b>💥 Defect 380 (Contour/Design Fault)</b></div>', unsafe_allow_html=True)
    df_380 = get_graph_data(380)
    if not df_380.empty:
        st.markdown('<div class="scrollable-graph-container"><div class="inner-graph-box">', unsafe_allow_html=True)
        fig_380 = px.bar(df_380, x='Material', y='rework quantity', text='rework quantity')
        fig_380.update_traces(textposition='outside', marker_color='#000000')
        fig_380.update_layout(xaxis=dict(type='category', tickangle=45), yaxis=dict(tickformat='d'), margin=dict(l=10, r=10, t=25, b=50), height=250, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_380, use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 ประวัติย้อนหลัง", key="btn_history"):
            st.toast("กำลังพัฒนาส่วนนี้...")
    with col2:
        if st.button("➕ เพิ่มตัว Imp.", key="btn_add"):
            st.toast("กำลังพัฒนาส่วนนี้...")
