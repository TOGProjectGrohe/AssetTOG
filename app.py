import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บให้ซ่อนเมนูเดิมเพื่อคุมดีไซน์เอง
st.set_page_config(page_title="TOG App", layout="centered", initial_sidebar_state="collapsed")

# 2. ปรับแต่ง CSS เคลียร์ค่าว่าง จัดวางตำแหน่งให้อยู่ตรงกลางมือถืออย่างสมบูรณ์
st.markdown("""
    <style>
    /* ซ่อนแถบเมนูข้างและส่วนหัวเดิมของ Streamlit */
    [data-testid="stSidebar"] {display: none !important;}
    [data-testid="collapsedControl"] {display: none !important;}
    header {visibility: hidden !important;}
    
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
        margin-bottom: 25px !important;
    }

    /* โซนด้านล่าง จัดข้อความและปุ่มให้อยู่กึ่งกลางหน้าจอมือถืออย่างสมบูรณ์ */
    .center-action-block {
        display: block !important;
        text-align: center !important;
        width: 100% !important;
        margin: 30px auto 10px auto !important;
    }

    .center-action-block p {
        color: #2c3e50 !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        margin-bottom: 15px !important;
        text-align: center !important;
    }

    /* ตกแต่งปุ่ม Dashboard สีน้ำเงินให้โค้งมนและล็อกอยู่กึ่งกลางจอมือถือ */
    div.stButton > button {
        background-color: #007bc3 !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 12px 30px !important;
        font-weight: bold !important;
        border: none !important;
        width: 85% !important;        /* บีบขนาดปุ่มให้พอดีสายตา */
        margin: 0 auto !important;    /* สั่งเลื่อนปุ่มมาตรงกลางหน้าจอ */
        display: block !important;
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
    
    # 2. การ์ดส่วนพนักงานเข้าใช้งาน (คลีน ไม่มีส่วนเกินหลุดหลง)
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

    # 3. โซนปุ่มดูภาพรวมด้านล่าง (ล้างโครงสร้างเก่า ครอบด้วย Class ใหม่ บังคับข้อความและปุ่มอยู่กึ่งกลางเป๊ะ)
    st.markdown('<div class="center-action-block">', unsafe_allow_html=True)
    st.markdown('<p>ต้องการดูข้อมูลสรุปโดยไม่ล็อกอิน?</p>', unsafe_allow_html=True)
    if st.button("📊 ดูภาพรวม Dashboard"):
        st.session_state.page = 'dashboard'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

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
        
        # กราฟวงกลom
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
    st.image("https://images.unsplash.com/photo-1581092335397-9583fe92d232?w=400", use_container_width=True)
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
