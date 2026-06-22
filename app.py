
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บให้ซ่อนเมนูเดิมเพื่อคุมดีไซน์เอง
st.set_page_config(page_title="TOG App", layout="centered", initial_sidebar_state="collapsed")

# 2. 🛠️ ถล่ม CSS บังคับปุ่ม Dashboard ขยายใหญ่เต็มจอ สีฟ้าสดใส และล้างบางขอบขาวส่วนเกินทั้งหมด
st.markdown("""
    <style>
    /* ซ่อนแถบเมนูข้างและส่วนหัวเดิมของ Streamlit */
    [data-testid="stSidebar"] {display: none !important;}
    [data-testid="collapsedControl"] {display: none !important;}
    header {visibility: hidden !important;}
    [data-testid="stHeader"] {display: none !important;}
    
    /* กรอบมือถือสีส้มพาสเทล */
    .stApp {
        max-width: 420px !important;
        margin: 20px auto !important;
        background: linear-gradient(180deg, #ffb07c 0%, #ffe3d1 30%, #fff7f2 100%) !important;
        border: 12px solid #1e293b !important;
        border-radius: 40px !important;
        padding: 24px !important;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3) !important;
        min-height: 850px !important;
        height: auto !important;
    }
    
    /* ส่วนหัว Header (วงกลมดำ, TOG) */
    .bank-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 25px;
    }
    .tog-circle-logo {
        width: 45px;
        height: 45px;
        background-color: #000000;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #ffffff;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: bold;
        font-size: 14px;
    }

    /* แบนเนอร์ข้อความด้านบน */
    .promo-banner {
        background: rgba(255, 255, 255, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        color: #2c3e50;
        font-weight: bold;
        margin-bottom: 20px;
    }

    /* กล่องสีขาว (Card) สำหรับ Login */
    .login-card {
        background-color: white !important;
        border-radius: 20px !important;
        padding: 20px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 5px !important;
    }

    /* ล้างบางแท่งขาวรีๆ คั่นกลาง และรีเซ็ตพื้นหลังส่วนเกินของ Streamlit */
    div[data-testid="element-container"] {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    div[data-testid="stVerticalBlock"] > div {
        padding: 0px !important;
        margin: 0px !important;
        background: transparent !important;
    }
    
    /* จัดข้อความถามก่อนล็อกอินให้อยู่ตรงกลางหน้าจอ */
    .center-text-only {
        color: #2c3e50 !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        text-align: center !important;
        margin-top: 50px !important;
        margin-bottom: 20px !important;
        width: 100% !important;
        display: block !important;
    }

    /* 🎯 จัดการ Container ของปุ่มให้เป็นแบบ Block เพื่อให้ขยายได้เต็มความกว้าง */
    div.stButton {
        display: block !important;
        width: 100% !important;
        text-align: center !important;
    }

    /* 🎯 ปรับปรุงตามสั่ง: ขยายปุ่ม Dashboard สีฟ้าให้ใหญ่ยาวเต็มหน้าจอมือถือและอยู่ตรงกลางเป๊ะๆ */
    div.stButton > button {
        background-color: #007bc3 !important; /* สีฟ้า/น้ำเงิน สดใสตามรูป */
        color: white !important;
        border-radius: 30px !important; /* ปรับให้โค้งมนเรียบเนียนขึ้น */
        padding: 14px 0px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        border: none !important;
        width: 100% !important; /* ขยายให้ยาวสุดขอบการ์ดซ้าย-ขวา */
        max-width: 100% !important;
        display: block !important;
        margin: 0 auto !important; /* บังคับอยู่ตรงกลาง */
        box-shadow: 0 4px 12px rgba(0, 123, 195, 0.3) !important; /* เพิ่มมิติให้ปุ่มเด่นขึ้น */
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

# จัดการ State การเปลี่ยนหน้า
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# --- ส่วนหัวของแอป (Header) ---
st.markdown(f"""
<div class="bank-header">
    <div class="tog-circle-logo">TOG</div>
    <div>
        <small style="color:#ffffff; opacity:0.8; display:block; font-size:11px;">ยินดีต้อนรับ</small>
        <span style="font-size:16px; font-weight:600; color:white;">TOG App</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- หน้าแรก: สแกนเข้าใช้งาน / ดูภาพรวม ----------------
if st.session_state.page == 'login':
    # 1. แบนเนอร์ด้านบนสุด
    st.markdown('<div class="promo-banner">✨ ปรับปรุงประสิทธิภาพการทำงานอย่างต่อเนื่อง</div>', unsafe_allow_html=True)
    
    # 2. การ์ดส่วนพนักงานเข้าใช้งาน
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

    # 3. โซนปุ่มดูภาพรวมด้านล่าง (ปุ่มสีฟ้ายาวใหญ่เต็มหน้าจอ และตัวหนังสืออยู่กึ่งกลางเป๊ะ)
    st.markdown('<span class="center-text-only">ต้องการดูข้อมูลสรุปโดยไม่ล็อกอิน?</span>', unsafe_allow_html=True)
    if st.button("📊 ดูภาพรวม Dashboard"):
        st.session_state.page = 'dashboard'
        st.rerun()

# ---------------- หน้าหลัก: แสดงกราฟ และ 2 ปุ่มล่าง ----------------
elif st.session_state.page == 'dashboard':
    st.markdown('<div class="login-card" style="padding: 15px !important;"><h4 style="margin:0; font-size:16px; color:#2c3e50;">📈 อันดับความสำเร็จ 1-10</h4></div>', unsafe_allow_html=True)
    
    if not df.empty:
        col_name = df.columns[0]
        col_value = df.columns[1] if len(df.columns) > 1 else df.columns[0]
        top_10 = df.sort_values(by=col_value, ascending=False).head(10)
        
        # กราฟแท่ง
        fig_bar = px.bar(top_10, x=col_name, y=col_value, color=col_value, color_continuous_scale="Oranges")
        fig_bar.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=180, showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # กราฟวงกลม
        fig_pie = px.pie(top_10, names=col_name, values=col_value, color_discrete_sequence=px.colors.sequential.Oranges_r)
        fig_pie.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=180)
        fig_pie.update_traces(textposition='inside', textinfo='percent')
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("กำลังรอข้อมูลจาก Google Sheet...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2 ปุ่มล่างหลัก
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 ข้อมูลย้อนหลัง"):
            st.session_state.page = 'history'
            st.rerun()
    with col2:
        if st.button("➕ เพิ่ม Imp."):
            st.session_state.page = 'add_new'
            st.rerun()
            
    st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
    if st.button("🔙 ออกจากระบบ", key="logout"):
        st.session_state.page = 'login'
        st.rerun()

# ---------------- หน้าย่อย: ดูข้อมูลย้อนหลัง Before/After ----------------
elif st.session_state.page == 'history':
    st.markdown('<div class="login-card" style="padding: 10px 15px;"><h4 style="margin:0; font-size:16px; color:#2c3e50;">🔍 ประวัติ Before & After</h4></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.write("📸 ภาพเปรียบเทียบผลงาน")
    st.error("🔴 ก่อนแก้ไข (Before)")
    st.image("https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=400", use_container_width=True)
    
    st.success("🟢 หลังแก้ไข (After)")
    st.image("https://images.unsplash.com/photo-158109335397-9583fe92d232?w=400", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🏠 กลับหน้าหลัก"):
        st.session_state.page = 'dashboard'
        st.rerun()

# ---------------- หน้าย่อย: ฟอร์มเพิ่ม Improvement ----------------
elif st.session_state.page == 'add_new':
    st.markdown('<div class="login-card" style="padding: 10px 15px;"><h4 style="margin:0; font-size:16px; color:#2c3e50;">📝 บันทึก Improvement ใหม่</h4></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    with st.form("mobile_form"):
        title = st.text_input("ชื่อหัวข้อการปรับปรุง")
        detail = st.text_area("รายละเอียดการแก้ไข")
        f_before = st.file_uploader("ภาพก่อนแก้ไข", type=["jpg","png"])
        f_after = st.file_uploader("ภาพหลังแก้ไข", type=["jpg","png"])
        
        if st.form_submit_button("🚀 บันทึกข้อมูล"):
            st.success("ส่งข้อมูลเข้า Google Sheet สำเร็จ!")
    st.markdown('</div>', unsafe_allow_html=True)
            
    if st.button("🏠 กลับหน้าหลัก", key="back_home"):
        st.session_state.page = 'dashboard'
        st.rerun()
