import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บ (พื้นฐาน)
st.set_page_config(page_title="TOG App", layout="centered", initial_sidebar_state="collapsed")

# 2. 🛠️ ชุดคำสั่งทำลายล้าง Toolbar และป้าย Deploy (Extreme Kill)
st.markdown("""
    <style>
    /* 🚫 1. ลบปุ่ม Deploy (มงกุฎแดง) และ MainMenu (จุด 3 จุด) แบบถาวร */
    .stDeployButton, .st-emotion-cache-15z78k, .st-emotion-cache-6q9sum, .st-emotion-cache-1wb763a {
        display: none !important;
    }
    
    /* 🚫 2. ลบแถบ Toolbar ด้านบนและสถานะการเชื่อมต่อ */
    [data-testid="stHeader"], [data-testid="stDecoration"], [data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* 🚫 3. ลบปุ่ม Manage App (วงกลมเขียว) ที่มุมล่างขวาบนมือถือ */
    footer {visibility: hidden !important;}
    [data-testid="stStatusWidget"], #stConnectionStatus, .st-emotion-cache-zq59db {
        display: none !important;
    }
    
    /* 🚫 4. ลบเมนูที่แอบขึ้นมาเวลาคลิกขวาหรือกดค้าง */
    #MainMenu {visibility: hidden !important;}

    /* 📱 ปรับแต่งกรอบมือถือ (TOG Orange Theme) */
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
    
    /* 🎯 ล้างบางแท่งขาว/กล่องขาวรีๆ ที่หลุดมาคั่นกลาง */
    div[data-testid="stVerticalBlock"] > div,
    div[data-testid="element-container"],
    .st-emotion-cache-1v07afm {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        margin: 0px !important;
        padding: 0px !important;
    }

    /* 🏷️ ดีไซน์ส่วนหัว (วงกลมดำ TOG) */
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

    /* 🪪 กล่อง Login Card */
    .login-card {
        background-color: white !important;
        border-radius: 20px !important;
        padding: 20px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 10px !important;
    }

    /* 🎯 จัดโซนข้อความและปุ่ม Dashboard ให้อยู่กึ่งกลางหน้าจอมือถือ */
    .center-wrapper {
        text-align: center !important;
        width: 100% !important;
        margin: 40px 0 20px 0 !important;
    }

    /* 🎯 ปุ่ม Custom สีฟ้ายาวเต็มจอ (ล็อกตำแหน่งกึ่งกลาง) */
    .btn-full-width {
        background-color: #007bc3 !important;
        color: white !important;
        border-radius: 30px !important;
        padding: 14px 0px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        width: 100% !important;
        display: block !important;
        text-align: center !important;
        text-decoration: none !important;
        box-shadow: 0 4px 12px rgba(0, 123, 195, 0.3) !important;
        margin: 10px 0 !important;
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

# ระบบเปลี่ยนหน้า (Query Params)
if "nav" not in st.query_params:
    st.query_params["nav"] = "login"
current_page = st.query_params["nav"]

# --- ส่วนหัว (Header) ---
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
if current_page == "login":
    st.markdown('<div style="background:rgba(255,255,255,0.4); border:1px solid rgba(255,255,255,0.5); border-radius:20px; padding:15px; text-align:center; color:#2c3e50; font-weight:bold; margin-bottom:20px;">✨ ปรับปรุงประสิทธิภาพการทำงานอย่างต่อเนื่อง</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:18px; margin-top:0; color:#2c3e50;'>🪪 ส่วนพนักงานเข้าใช้งาน</h3>", unsafe_allow_html=True)
    
    enable_camera = st.checkbox("เปิดสิทธิ์ใช้งานกล้องถ่ายรูป")
    if enable_camera:
        st.markdown("<p style='font-size:13px; color:#64748b; margin-top:10px;'>สแกน QR Code พนักงานของคุณ</p>", unsafe_allow_html=True)
        picture = st.camera_input("", label_visibility="collapsed")
        if picture:
            st.query_params["nav"] = "dashboard"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # 🎯 โซนล่างสุด: ปุ่ม Dashboard ยาวเต็มจอ ตรงกลางเป๊ะ ไม่มีเส้นคั่น
    st.markdown("""
        <div class="center-wrapper">
            <div style="color:#2c3e50; font-size:16px; margin-bottom:15px;">ต้องการดูข้อมูลสรุปโดยไม่ล็อกอิน?</div>
            <a href="?nav=dashboard" target="_self" class="btn-full-width">📊 ดูภาพรวม Dashboard</a>
        </div>
    """, unsafe_allow_html=True)

# ---------------- หน้าหลัก: Dashboard ----------------
elif current_page == "dashboard":
    st.markdown('<div class="login-card" style="padding: 15px !important;"><h4 style="margin:0; font-size:16px; color:#2c3e50;">📈 อันดับความสำเร็จ 1-10</h4></div>', unsafe_allow_html=True)
    
    if not df.empty:
        col_name = df.columns[0]
        col_value = df.columns[1] if len(df.columns) > 1 else df.columns[0]
        top_10 = df.sort_values(by=col_value, ascending=False).head(10)
        
        fig_bar = px.bar(top_10, x=col_name, y=col_value, color=col_value, color_continuous_scale="Oranges")
        fig_bar.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=180, showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 20px;">
            <a href="?nav=history" target="_self" class="btn-full-width" style="font-size:14px !important;">🔍 ประวัติ</a>
            <a href="?nav=add_new" target="_self" class="btn-full-width" style="font-size:14px !important;">➕ เพิ่มงาน</a>
        </div>
        <a href="?nav=login" target="_self" class="btn-full-width" style="background-color: #ef4444 !important; margin-top:20px !important;">🔙 ออกจากระบบ</a>
    """, unsafe_allow_html=True)

# ---------------- หน้าย่อยอื่นๆ ----------------
else:
    st.info("กำลังพัฒนาส่วนนี้...")
    st.markdown('<a href="?nav=dashboard" target="_self" class="btn-full-width">🏠 กลับหน้าหลัก</a>', unsafe_allow_html=True)
