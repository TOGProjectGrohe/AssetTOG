import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บพื้นฐานให้กระชับเข้ามุมมองสไตล์สมาร์ทโฟน
st.set_page_config(page_title="TOG App", layout="centered", initial_sidebar_state="collapsed")

# 2. 🛠️ CSS ทลายบล็อกหลัก: แก้อาการปุ่มดื้อชิดซ้าย บังคับยืดเต็มกรอบการ์ดและอยู่ตรงกลาง 100%
st.markdown("""
    <style>
    /* 🚫 ซ่อนเมนูและป้ายส่วนเกินดั้งเดิมของ Streamlit ทั้งหมด */
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
    
    /* 🚫 ซ่อนปุ่ม Manage App มุมขวาล่างไม่ให้โผล่มากวนใจ */
    [data-testid="stStatusWidget"], 
    #stConnectionStatus,
    div[class*="viewerBadge"],
    div[class*="st-emotion-cache-"] button[title="Manage app"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }

    /* 📱 ดีไซน์คุมธีมหน้าจอมือถือ ส้มพาสเทลสวยงาม */
    .stApp {
        max-width: 420px !important;
        margin: 0px auto !important;
        background: linear-gradient(180deg, #ffb07c 0%, #ffe3d1 30%, #fff7f2 100%) !important;
        border: 12px solid #1e293b !important;
        border-radius: 40px !important;
        padding: 95px 24px 24px 24px !important; 
        box-shadow: 0 20px 50px rgba(0,0,0,0.3) !important;
        min-height: 90vh !important;
        height: auto !important;
    }
    
    /* 🎯 ไม้ตายทลายบล็อกหลัก: ล้างค่าความกว้างสูงสุดและตัวกั้นของ Streamlit ที่บีบข้อมูลชิดซ้าย */
    [data-testid="stMainBlockContainer"],
    [data-testid="stVerticalBlock"],
    [data-testid="stVerticalBlockRoot"],
    div[data-testid="element-container"],
    .stColumn {
        width: 100% !important;
        max-width: 100% !important;
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
        width: 100% !important;
    }

    /* 🎯 แถบนำทาง Home / Logout ล็อกตำแหน่งไว้ที่มุมบนสุด */
    .custom-top-navbar {
        position: absolute !important;
        top: 18px !important;
        left: 20px !important;
        right: 20px !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        z-index: 999999 !important;
    }
    
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

    /* จัดบล็อกโลโก้ TOG และข้อความต้อนรับให้อยู่ตรงกึ่งกลางหน้าจอ */
    .center-header-block {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        margin-top: 10px !important;
        margin-bottom: 25px !important;
        width: 100% !important;
    }
    .tog-center-logo {
        width: 50px;
        height: 50px;
        background-color: #000000;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #ffffff;
        font-weight: bold;
        font-size: 15px;
        margin-bottom: 8px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }

    /* 🎯 คำสั่งทุบสตรีมลิตเลเยอร์ในสุด: บังคับยืดแผงปุ่มเต็มจอ 100% ทุกมิติ */
    div.stButton {
        width: 100% !important;
        display: block !important;
        text-align: center !important;
        margin: 10px 0 0 0 !important;
    }
    
    div.stButton > button {
        background-color: #007bc3 !important;
        color: white !important;
        border-radius: 30px !important;
        padding: 14px 0px !important;  /* ถ่างความสูงปุ่ม */
        font-weight: bold !important;
        font-size: 16px !important;
        border: none !important;
        width: 100% !important;         /* กางพื้นหลังสีฟ้ายาวเต็มกรอบ */
        display: block !important;
        margin: 0 auto !important;       /* ล็อกตำแหน่งอยู่เซ็นเตอร์ */
        box-shadow: 0 4px 12px rgba(0, 123, 195, 0.35) !important;
    }

    /* จัดระเบียบตัวอักษรและไอคอนภายในปุ่มชั้นในสุดให้เด้งมาอยู่ตรงกลาง */
    div.stButton > button div, 
    div.stButton > button p,
    div.stButton > button span {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
        width: 100% !important;
        margin: 0 auto !important;
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

# --- แถบปุ่มนำทางด้านบนสุด ---
st.markdown("""
<div class="custom-top-navbar">
    <a href="?nav=login" target="_self" class="nav-btn-link">🏠 Home</a>
    <a href="?nav=login" target="_self" class="nav-btn-link">🚪 Logout</a>
</div>
""", unsafe_allow_html=True)

# --- โลโก้ TOG และข้อความต้อนรับกึ่งกลาง ---
st.markdown("""
<div class="center-header-block">
    <div class="tog-center-logo">TOG</div>
    <div>
        <small style="color:#fff; opacity:0.8; display:block; font-size:11px; margin-bottom:2px;">ยินดีต้อนรับ</small>
        <span style="font-size:18px; font-weight:bold; color:white; letter-spacing: 0.5px;">TOG App</span>
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

    # ข้อความคำอธิบายเหนือปุ่มจัดกึ่งกลาง
    st.markdown('<div style="text-align: center; width: 100%; margin-top: 35px; margin-bottom: 15px;"><div style="color:#2c3e50; font-size:16px; font-weight:500;">ต้องการดูข้อมูลสรุปโดยไม่ล็อกอิน?</div></div>', unsafe_allow_html=True)
    
    # 🎯 ปุ่มเปิดภาพรวม Dashboard (รอบนี้ตีกรอบฟ้ายาวเต็มกรอบ และอักษรอยู่ตรงกลางกึ่งกลางแน่นอน 100%)
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
