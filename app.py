import streamlit as st
import pandas as pd
import plotly.express as px

# ตั้งค่าหน้าเว็บให้ซ่อนเมนูเดิมเพื่อคุมดีไซน์เอง
st.set_page_config(page_title="TOG NEXT", layout="centered", initial_sidebar_state="collapsed")

# ปรับปรุง CSS ขยายขนาดกรอบสีฟ้าให้คลุมพื้นที่ทั้งหมด และล็อกเนื้อหาให้อยู่ตรงกลางสวยๆ
st.markdown("""
    <style>
    /* ซ่อนแถบเมนูข้างของ Streamlit */
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
    
    /* จำลองกรอบโทรศัพท์มือถือที่ยืดหยุ่นตามความสูงของเนื้อหา */
    .mobile-container {
        max-width: 410px;
        margin: 20px auto;
        background: linear-gradient(180deg, #00a3e0 0%, #dbeafe 35%, #f4f9fc 100%);
        border: 12px solid #1e293b;
        border-radius: 40px;
        padding: 28px 24px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.25);
        min-height: 780px; /* ความสูงขั้นต่ำ */
        height: auto;       /* ให้ยืดขยายตามเนื้อหาอัตโนมัติ */
        overflow: hidden;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* สไตล์หัวแอปธนาคาร (Header) */
    .bank-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
        margin-bottom: 25px;
    }
    .bank-logo {
        font-size: 20px;
        font-weight: bold;
        letter-spacing: 1px;
    }
    
    /* การ์ดเมนูสีขาวภายในกรอบ */
    .menu-card {
        background-color: white;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
        margin-bottom: 18px;
    }
    
    /* ตกแต่งปุ่มกดหลักให้โค้งมนสไตล์แอปธนาคาร */
    div.stButton > button {
        width: 100%;
        background-color: #007bc3;
        color: white;
        border-radius: 25px;
        padding: 11px 20px;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #0c2340;
        color: white;
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

# จัดการ State การเปลี่ยนหน้าในแอป
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# เริ่มต้นเปิดกล่องโทรศัพท์มือถือ (ครอบคลุมเนื้อหาทั้งหมดด้านล่าง)
st.markdown('<div class="mobile-container">', unsafe_allow_html=True)

# ---------------- ส่วนหัวของแอป (Header) ----------------
st.markdown("""
<div class="bank-header">
    <div style="display:flex; align-items:center; gap:10px;">
        <div style="width:35px; height:35px; background:#fff; border-radius:50%; display:flex; align-items:center; justify-content:center; color:#00a3e0; font-weight:bold; font-size:14px;">TG</div>
        <div>
            <small style="color:#e0f2fe; display:block; font-size:11px;">ยินดีต้อนรับ</small>
            <span style="font-size:14px; font-weight:bold;">TOG NEXT App</span>
        </div>
    </div>
    <div class="bank-logo">NEXT</div>
</div>
""", unsafe_allow_html=True)

# ---------------- หน้าแรก: สแกนเข้าใช้งาน / ดูภาพรวม ----------------
if st.session_state.page == 'login':
    st.markdown('<div class="menu-card" style="background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); color: white; text-align:center; padding: 12px; margin-bottom: 25px;"><b>✨ ปรับปรุงประสิทธิภาพการทำงานอย่างต่อเนื่อง</b></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="menu-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:18px; margin-top:0; color:#0c2340;'>🪪 ส่วนพนักงานเข้าใช้งาน</h3>", unsafe_allow_html=True)
    enable_camera = st.checkbox("เปิดสิทธิ์ใช้งานกล้องถ่ายรูป")
    if enable_camera:
        picture = st.camera_input("สแกน QR Code พนักงานของคุณ")
        if picture:
            st.session_state.page = 'dashboard'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="menu-card" style="text-align:center;">', unsafe_allow_html=True)
    st.markdown("<p style='color:#475569; margin-bottom:15px;'>ต้องการดูข้อมูลสรุปโดยไม่ล็อกอิน?</p>", unsafe_allow_html=True)
    if st.button("📊 ดูภาพรวม
