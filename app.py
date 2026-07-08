import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บให้ซ่อนเมนูแบบ Built-in
st.set_page_config(page_title="TOG App", layout="centered", initial_sidebar_state="collapsed")

# 2. 🛠️ CSS ชุดทำลายล้างป้ายแอดมินระดับลึก (ลบมงกุฎแดงและวงกลมเขียวบนมือถือให้หายขาด)
st.markdown("""
    <style>
    /* 🚫 ซ่อนปุ่ม Deploy (มงกุฎแดง) แถบเครื่องมือ และปุ่มจุด 3 จุด ทั้งหมด */
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
        opacity: 0 !important;
    }
    
    /* 🚫 ถล่มปุ่มวงกลมเขียว (Manage App) และแถบสถานะเชื่อมต่อส่วนล่างสุดของจอมือถือ */
    [data-testid="stStatusWidget"], 
    #stConnectionStatus,
    .st-emotion-cache-zq59db,
    .st-emotion-cache-1wb763a,
    .st-emotion-cache-6q9sum,
    .st-emotion-cache-15z78k,
    .st-emotion-cache-b9st7z,
    .st-emotion-cache-h5g6vv,
    div[class*="st-emotion-cache-"] button[title="Manage app"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0 !important;
    }

    /* 📱 ดีไซน์กรอบแอปให้เป็นทรงสมาร์ทโฟน สีส้มพาสเทลสวยงาม */
    .stApp {
        max-width: 420px !important;
        margin: 0px auto !important;
        background: linear-gradient(180deg, #ffb07c 0%, #ffe3d1 30%, #fff7f2 100%) !important;
        border: 12px solid #1e293b !important;
        border-radius: 40px !important;
        padding: 24px !important;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3) !important;
        min-height: 90vh !important;
        height: auto !important;
    }
    
    /* 🎯 ล้างบางแท่งขาวรี ๆ หรือเส้นขอบแปลก ๆ ที่มักจะโผล่มาคั่นช่องว่างบนมือถือ */
    div[data-testid="stVerticalBlock"] > div,
    div[data-testid="element-container"],
    [data-testid="stVerticalBlock"] {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0px !important;
        margin: 0px !important;
    }

    /* 🏷️ ส่วนหัวแอปประยุกต์ LOGO วงกลมดำ */
    .bank-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 25px;
        margin-top: 10px;
    }
    .tog-circle-logo {
        width: 45px;
        height: 45px;
        background-color: #000;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #fff;
        font-weight: bold;
        font-size: 14px;
    }

    /* 🪪 กล่องขาว Login Card */
    .login-card {
        background-color: white !important;
        border-radius: 20px !important;
        padding: 20px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ฟังก์ชันดึงข้อมูลจาก Google Sheet
@st.cache_data(ttl=30)
def load_data():
    sheet_id = "1jL7baZKeeuAmuQUCWuEN7cqjya9HoZjCi9riD6DUnB8"
    gid = "0"
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    try:
        return pd.read_csv(csv_url)
    except:
        return pd.DataFrame()

df = load_data()

# ตรวจสอบสถานะหน้าเพจด้วย Session State (กลับมาใช้โครงสร้างสตรีมลิตปกติที่รันเสถียรที่สุด)
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# --- ส่วนแสดงผลบนสุด: Header ---
st.markdown(f"""
<div class="bank-header">
    <div class="tog-circle-logo">TOG</div>
    <div>
        <small style="color:#fff; opacity:0.8; display:block; font-size:11px;">ยินดีต้อนรับ</small>
        <span style="font-size:16px; font-weight:600; color:white;">TOG App</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- หน้าแรก: Login ----------------
if st.session_state.page == 'login':
    st.markdown('<div style="background:rgba(255,255,255,0.4); border:1px solid rgba(255,255,255,0.5); border-radius:20px; padding:15px; text-align:center; color:#2c3e50; font-weight:bold; margin-bottom:20px;">✨ ปรับปรุงประสิทธิภาพการทำงานอย่างต่อเนื่อง</div>', unsafe_allow_html=True)

    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:18px; margin-top:0; color:#2c3e50;'>🪪 ส่วนพนักงานเข้าใช้งาน</h3>", unsafe_allow_html=True)

    enable_camera = st.checkbox("เปิดสิทธิ์ใช้งานกล้องถ่ายรูป")
    if enable_camera:
        st.markdown("<p style='font-size:13px; color:#64748b; margin-top:10px;'>สแกน QR Code พนักงานของคุณ</p>", unsafe_allow_html=True)
        picture = st.camera_input("", label_visibility="collapsed")
        if picture:
            st.session_state.page = 'dashboard'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # 🎯 กล่องคำถาม จัดวางตรงกึ่งกลางหน้าจอ
    st.markdown('<div style="text-align:center; color:#2c3e50; font-size:16px; margin-top:40px; margin-bottom:15px; font-weight:500;">ต้องการดูข้อมูลสรุปโดยไม่ล็อกอิน?</div>', unsafe_allow_html=True)
    
    # 🎯 ใช้ฟังก์ชันดั้งเดิม use_container_width=True ของ Streamlit เพื่อดึงปุ่มขยายยาวเต็มจอ
    if st.button("📊 ดูภาพรวม Dashboard", key="btn_dash", use_container_width=True):
        st.session_state.page = 'dashboard'
        st.rerun()
        
    # สั่งเขียน CSS ฝังเจาะจงเฉพาะปุ่ม key="btn_dash" ให้เปลี่ยนเป็นสีฟ้าสดใส โค้งมนกริบ
    st.markdown("""
        <style>
        div.stButton > button[key="btn_dash"] {
            background-color: #007bc3 !important;
            color: white !important;
            border-radius: 30px !important;
            padding: 14px 0px !important;
            font-weight: bold !important;
            font-size: 16px !important;
            border: none !important;
            box-shadow: 0 4px 12px rgba(0, 123, 195, 0.3) !important;
        }
        </style>
    """, unsafe_allow_html=True)

# ---------------- หน้าหลัก: Dashboard ----------------
elif st.session_state.page == 'dashboard':
    st.markdown('<div class="login-card" style="padding: 15px !important;"><h4 style="margin:0; font-size:16px; color:#2c3e50;">📈 อันดับความสำเร็จ 1-10</h4></div>', unsafe_allow_html=True)

    if not df.empty:
        col_name = df.columns[0]
        col_value = df.columns[1] if len(df.columns) > 1 else df.columns[0]
        top_10 = df.sort_values(by=col_value, ascending=False).head(10)

        fig_bar = px.bar(top_10, x=col_name, y=col_value, color=col_value, color_continuous_scale="Oranges")
        fig_bar.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=180, showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    # กลุ่มปุ่มกดควบคุมในหน้า Dashboard
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 ประวัติ", use_container_width=True):
            st.info("กำลังพัฒนาส่วนนี้...")
    with col2:
        if st.button("➕ เพิ่มงาน", use_container_width=True):
            st.info("กำลังพัฒนาส่วนนี้...")
            
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    if st.button("🔙 ออกจากระบบ", use_container_width=True):
        st.session_state.page = 'login'
        st.rerun()
