import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="TOG App", layout="centered", initial_sidebar_state="collapsed")

# 2. 🛠️ ไม้ตายสุดท้าย: ไล่ล่าลบทุกอย่างที่เป็นส่วนเกินของ Streamlit (Ads/Toolbar/White Bars)
st.markdown("""
    <style>
    /* 🚫 ลบป้าย Deploy, มงกุฎ, และแถบเมนูทั้งหมด (ครอบคลุมทุกชื่อคลาสสุ่ม) */
    [data-testid="stHeader"], 
    [data-testid="stToolbar"], 
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    footer, 
    header, 
    .stDeployButton,
    #stConnectionStatus {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
    }

    /* 📱 ปรับแต่งพื้นหลังแอปให้เป็นสีส้มพาสเทลแบบเต็มจอ */
    .stApp {
        max-width: 420px !important;
        margin: 0 auto !important;
        background: linear-gradient(180deg, #ffb07c 0%, #ffe3d1 30%, #fff7f2 100%) !important;
        border: 10px solid #1e293b !important;
        border-radius: 40px !important;
        padding: 20px !important;
        min-height: 95vh !important;
    }

    /* 🎯 กำจัด "แท่งขาวรีๆ" (White Bars) ที่คั่นกลางระหว่าง Element */
    [data-testid="stVerticalBlock"] > div {
        padding: 0px !important;
        margin: 0px !important;
        gap: 0px !important;
    }
    
    /* 🎯 ลบช่องว่างและเส้นคั่นสีขาวที่ Streamlit ชอบสร้างขึ้นมาเอง */
    [data-testid="element-container"] {
        background: transparent !important;
        border: none !important;
        margin-bottom: 0px !important;
    }

    /* 🏷️ ส่วนหัวแอป (วงกลมดำ TOG) */
    .custom-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 30px;
    }
    .tog-logo {
        width: 48px;
        height: 48px;
        background: #000;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #fff;
        font-weight: bold;
    }

    /* 🪪 การ์ดสีขาวสำหรับส่วน Login */
    .login-box {
        background: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* 🎯 บังคับปุ่ม Streamlit ให้ยาวเต็มจอ ตรงกลาง และเป็นสีฟ้าสดใส */
    div.stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        margin-top: 20px !important;
    }

    div.stButton > button {
        background-color: #007bc3 !important;
        color: white !important;
        border-radius: 30px !important;
        padding: 15px 0px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        width: 100% !important;
        border: none !important;
        box-shadow: 0 5px 15px rgba(0, 123, 195, 0.3) !important;
    }

    /* จัดข้อความ Guest ล่างปุ่มให้อยู่ตรงกลาง */
    .guest-text {
        text-align: center;
        color: #2c3e50;
        font-size: 15px;
        margin-top: 40px;
        width: 100%;
        display: block;
    }
    </style>
""", unsafe_allow_html=True)

# ฟังก์ชันดึงข้อมูล
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

# จัดการ State หน้าเว็บ
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# --- ส่วนหัว (Header) ---
st.markdown("""
<div class="custom-header">
    <div class="tog-logo">TOG</div>
    <div>
        <small style="color:white; opacity:0.8; display:block;">ยินดีต้อนรับ</small>
        <b style="color:white; font-size:17px;">TOG App</b>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- หน้า LOGIN ----------------
if st.session_state.page == 'login':
    # แบนเนอร์ (ใช้คำสั่ง Python ปกติ แต่ CSS จะคุมให้ไม่มีขอบขาว)
    st.markdown('<div style="background:rgba(255,255,255,0.4); border-radius:15px; padding:15px; text-align:center; color:#2c3e50; font-weight:bold; margin-bottom:20px;">✨ ปรับปรุงประสิทธิภาพการทำงานอย่างต่อเนื่อง</div>', unsafe_allow_html=True)
    
    # การ์ด Login
    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown("<h3 style='font-size:18px; margin-top:0; color:#2c3e50;'>🪪 ส่วนพนักงานเข้าใช้งาน</h3>", unsafe_allow_html=True)
        enable_camera = st.checkbox("เปิดสิทธิ์ใช้งานกล้องถ่ายรูป")
        if enable_camera:
            st.camera_input("สแกน QR Code พนักงาน", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

    # ส่วนล่าง: ข้อความและปุ่ม Dashboard (จัดกลาง+เต็มจอด้วย CSS)
    st.markdown('<span class="guest-text">ต้องการดูข้อมูลสรุปโดยไม่ล็อกอิน?</span>', unsafe_allow_html=True)
    if st.button("📊 ดูภาพรวม Dashboard"):
        st.session_state.page = 'dashboard'
        st.rerun()

# ---------------- หน้า DASHBOARD ----------------
elif st.session_state.page == 'dashboard':
    st.markdown('<div class="login-box" style="padding:15px;"><h4 style="margin:0; font-size:16px;">📈 อันดับความสำเร็จ 1-10</h4></div>', unsafe_allow_html=True)
    
    if not df.empty:
        col_name = df.columns[0]
        col_value = df.columns[1] if len(df.columns) > 1 else df.columns[0]
        top_10 = df.sort_values(by=col_value, ascending=False).head(10)
        fig_bar = px.bar(top_10, x=col_name, y=col_value, color=col_value, color_continuous_scale="Oranges")
        fig_bar.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=200, showlegend=False, coloraxis_showscale=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # ปุ่มกลับหน้าแรก (ปุ่มสีแดง)
    st.markdown("<div style='margin-top:30px;'></div>", unsafe_allow_html=True)
    if st.button("🔙 ออกจากระบบ"):
        st.session_state.page = 'login'
        st.rerun()
