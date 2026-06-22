import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บให้ซ่อนเมนูเดิมเพื่อคุมดีไซน์เอง
st.set_page_config(page_title="TOG NEXT", layout="centered", initial_sidebar_state="collapsed")

# 2. ฝัง CSS ดีไซน์โทนสีส้มพาสเทลอุ่นสบายตา และล็อกให้อยู่ในกรอบมือถืออย่างสมบูรณ์
st.markdown("""
    <style>
    /* ซ่อนแถบเมนูข้างของ Streamlit */
    [data-testid="stSidebar"] {display: none !important;}
    [data-testid="collapsedControl"] {display: none !important;}
    
    /* บังคับตัวแอปทั้งหมดให้อยู่ในกรอบมือถือและเปลี่ยนเป็นพื้นหลังสีส้มพาสเทลไล่เฉด */
    .stApp {
        max-width: 420px !important;
        margin: 20px auto !important;
        background: linear-gradient(180deg, #ffb07c 0%, #ffe3d1 30%, #fff7f2 100%) !important;
        border: 12px solid #1e293b !important;
        border-radius: 40px !important;
        padding: 24px !important;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3) !important;
        min-height: 800px !important;
        height: auto !important;
    }
    
    /* สไตล์หัวแอป (Header) */
    .bank-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
        margin-bottom: 25px;
    }
    
    /* การ์ดเมนูสีขาวภายในกรอบ */
    .menu-card {
        background-color: white !important;
        border-radius: 18px !important;
        padding: 20px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 18px !important;
        color: #2c3e50 !important;
    }
    
    /* ตกแต่งปุ่มกดหลักให้โค้งมนเป็นสีน้ำเงิน/ฟ้า เพื่อให้ตัดกับสีส้มได้อย่างสวยงามและเด่นชัด */
    div.stButton > button {
        width: 100% !important;
        background-color: #007bc3 !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 11px 20px !important;
        font-weight: bold !important;
        border: none !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #0c2340 !important;
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

# ---------------- ส่วนหัวของแอปโทนสีขาวบนพื้นส้ม (Header) ----------------
st.markdown("""
<div class="bank-header">
    <div style="display:flex; align-items:center; gap:10px;">
        <div style="width:35px; height:35px; background:#fff; border-radius:50%; display:flex; align-items:center; justify-content:center; color:#ff8c42; font-weight:bold; font-size:14px;">TG</div>
        <div>
            <small style="color:#fff3eb; display:block; font-size:11px;">ยินดีต้อนรับ</small>
            <span style="font-size:14px; font-weight:bold; color:white;">TOG NEXT App</span>
        </div>
    </div>
    <div style="font-size: 20px; font-weight: bold; letter-spacing: 1px; color:white;">NEXT</div>
</div>
""", unsafe_allow_html=True)

# ใช้ st.container รวบรวม Element ทั้งหมดให้ล็อกอยู่ในกรอบแอปอย่างเหนียวแน่น
main_container = st.container()

with main_container:
    # ---------------- หน้าแรก: สแกนเข้าใช้งาน / ดูภาพรวม ----------------
    if st.session_state.page == 'login':
        st.markdown('<div class="menu-card" style="background: rgba(255,255,255,0.2) !important; border: 1px solid rgba(255,255,255,0.3) !important; color: white !important; text-align:center; padding: 12px; margin-
