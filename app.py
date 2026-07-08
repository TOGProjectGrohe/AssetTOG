import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="TOG App", layout="centered", initial_sidebar_state="collapsed")

# 2. 🛠️ NUCLEAR CSS: ล้างระบบแสดงผลเดิมของ Streamlit ทิ้งให้หมด
st.markdown("""
    <style>
    /* 🚫 1. ลบส่วนเกิน Streamlit (Ads/Toolbar/Footer) */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
    footer, .stDeployButton, #stConnectionStatus, [data-testid="stStatusWidget"] {
        display: none !important;
        height: 0 !important;
    }

    /* 📱 2. ปรับแต่งพื้นหลังส้มพาสเทลให้เนียนกริบทั้งหน้าจอ */
    .stApp {
        background: linear-gradient(180deg, #ffb07c 0%, #ffe3d1 30%, #fff7f2 100%) !important;
        max-width: 420px !important;
        margin: 0 auto !important;
        border: 10px solid #1e293b !important;
        border-radius: 40px !important;
        height: 92vh !important;
        overflow-y: auto !important;
    }

    /* 🎯 3. วิธีกำจัด "แท่งขาวรีๆ" (White Bars) ที่ได้ผลเด็ดขาดที่สุด */
    /* ลบช่องว่าง (Gap) ระหว่างทุก Element ใน Streamlit */
    [data-testid="stVerticalBlock"] {
        gap: 0rem !important;
    }
    [data-testid="stVerticalBlock"] > div {
        padding: 0px !important;
        margin: 0px !important;
    }

    /* 🏷️ 4. ส่วนหัว (Header) */
    .app-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 20px 0 30px 0;
    }
    .tog-logo {
        width: 45px;
        height: 45px;
        background: black;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        font-weight: bold;
    }

    /* 🪪 5. การ์ด Login (ใช้ CSS ครอบกล่องเดิมของ Streamlit) */
    div[data-testid="stVerticalBlock"] > div:nth-child(3) {
        background: white;
        border-radius: 20px;
        padding: 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin: 10px 0 !important;
    }

    /* 🎯 6. จัดปุ่ม Dashboard ให้อยู่ "กึ่งกลาง" และ "ขยายเต็มจอ" */
    div.stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        padding: 20px 0 !important;
    }
    div.stButton > button {
        width: 100% !important;
        max-width: 320px !important;
        background-color: #007bc3 !important;
        color: white !important;
        border-radius: 30px !important;
        padding: 15px 0 !important;
        font-weight: bold !important;
        font-size: 16px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(0, 123, 195, 0.4) !important;
    }
    
    /* จัดข้อความ Guest */
    .guest-prompt {
        text-align: center;
        width: 100%;
        color: #2c3e50;
        font-size: 15px;
        margin-top: 30px;
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

# ลอจิกหน้าเว็บ
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# --- 1. Header (รวมเป็นชิ้นเดียว) ---
st.markdown("""
<div class="app-header">
    <div class="tog-logo">TOG</div>
    <div>
        <div style="color:white; font-size:12px; opacity:0.8;">ยินดีต้อนรับ</div>
        <div style="color:white; font-size:18px; font-weight:bold;">TOG App</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- หน้าแรก (Login) ----------------
if st.session_state.page == 'login':
    # แบนเนอร์
    st.markdown('<div style="background:rgba(255,255,255,0.4); border-radius:15px; padding:15px; text-align:center; color:#2c3e50; font-weight:bold; margin-bottom:10px;">✨ ปรับปรุงประสิทธิภาพอย่างต่อเนื่อง</div>', unsafe_allow_html=True)
    
    # ส่วนพนักงาน (CSS จะทำให้กล่องนี้กลายเป็นสีขาวเองอัตโนมัติ)
    with st.container():
        st.markdown("<b style='color:#2c3e50; font-size:18px;'>🪪 ส่วนพนักงานเข้าใช้งาน</b>", unsafe_allow_html=True)
        enable_camera = st.checkbox("เปิดสิทธิ์ใช้งานกล้องถ่ายรูป")
        if enable_camera:
            st.camera_input("สแกน QR Code", label_visibility="collapsed")

    # ส่วน Guest (ปุ่มจะขยายเต็มและอยู่กลางตาม CSS)
    st.markdown('<span class="guest-prompt">ต้องการดูข้อมูลสรุปโดยไม่ล็อกอิน?</span>', unsafe_allow_html=True)
    if st.button("📊 ดูภาพรวม Dashboard"):
        st.session_state.page = 'dashboard'
        st.rerun()

# ---------------- หน้า Dashboard ----------------
elif st.session_state.page == 'dashboard':
    st.markdown('<div style="background:white; border-radius:15px; padding:15px; margin-bottom:10px;"><h4 style="margin:0;">📈 อันดับความสำเร็จ 1-10</h4></div>', unsafe_allow_html=True)
    
    if not df.empty:
        col_name = df.columns[0]
        col_value = df.columns[1] if len(df.columns) > 1 else df.columns[0]
        top_10 = df.sort_values(by=col_value, ascending=False).head(10)
        fig = px.bar(top_10, x=col_name, y=col_value, color=col_value, color_continuous_scale="Oranges")
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=200, showlegend=False, coloraxis_showscale=False, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    if st.button("🔙 ออกจากระบบ"):
        st.session_state.page = 'login'
        st.rerun()
