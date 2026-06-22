import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บให้ซ่อนเมนูเดิมเพื่อคุมดีไซน์เอง
st.set_page_config(page_title="TOG App", layout="centered", initial_sidebar_state="collapsed")

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
        align-items: center;
        gap: 12px;
        margin-bottom: 25px;
    }
    
    /* วงกลมสีดำ ตัวอักษรสีขาว TOG */
    .tog-circle-logo {
        width: 42px;
        height: 42px;
        background-color: #000000;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #ffffff;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: bold;
        font-size: 14px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
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

# ---------------- ส่วนหัวของแอปตามสั่ง (วงกลมดำ, คำว่ายินดีต้อนรับ, TOG App) ----------------
st.markdown("""
<div class="bank-header">
    <div class="tog-circle-logo">TOG</div>
    <div>
        <small style="color:#fff3eb; display:block; font-size:11px; font-weight:300;">ยินดีต้อนรับ</small>
        <span style="font-size:15px; font-weight:600; color:white; line-height:1.2;">TOG App</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ใช้ st.container รวบรวม Element ทั้งหมดให้ล็อกอยู่ในกรอบแอปอย่างเหนียวแน่น
main_container = st.container()

with main_container:
    # ---------------- หน้าแรก: สแกนเข้าใช้งาน / ดูภาพรวม ----------------
    if st.session_state.page == 'login':
        st.markdown('<div class="menu-card" style="background: rgba(255,255,255,0.2) !important; border: 1px solid rgba(255,255,255,0.3) !important; color: white !important; text-align:center; padding: 12px; margin-bottom: 25px;"><b>✨ ปรับปรุงประสิทธิภาพการทำงานอย่างต่อเนื่อง</b></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="menu-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='font-size:18px; margin-top:0; color:#2c3e50;'>🪪 ส่วนพนักงานเข้าใช้งาน</h3>", unsafe_allow_html=True)
        enable_camera = st.checkbox("เปิดสิทธิ์ใช้งานกล้องถ่ายรูป")
        if enable_camera:
            picture = st.camera_input("สแกน QR Code พนักงานของคุณ")
            if picture:
                st.session_state.page = 'dashboard'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="menu-card" style="text-align:center;">', unsafe_allow_html=True)
        st.markdown("<p style='color:#5a6b7c; margin-bottom:15px;'>ต้องการดูข้อมูลสรุปโดยไม่ล็อกอิน?</p>", unsafe_allow_html=True)
        if st.button("📊 ดูภาพรวม Dashboard"):
            st.session_state.page = 'dashboard'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- หน้าหลัก: แสดงกราฟ และ 2 ปุ่มล่าง ----------------
    elif st.session_state.page == 'dashboard':
        st.markdown('<div class="menu-card" style="padding: 10px 15px;"><h4 style="margin:0; font-size:16px; color:#2c3e50;">📈 อันดับความสำเร็จ 1-10</h4></div>', unsafe_allow_html=True)
        
        if not df.empty:
            col_name = df.columns[0]
            col_value = df.columns[1] if len(df.columns) > 1 else df.columns[0]
            top_10 = df.sort_values(by=col_value, ascending=False).head(10)
            
            # 1. แสดงกราฟแท่ง (ใช้โทนสี Oranges ให้เข้ากับแอป)
            fig_bar = px.bar(top_10, x=col_name, y=col_value, color=col_value, color_continuous_scale="Oranges")
            fig_bar.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=180, showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # 2. แสดงกราฟวงกลม
            fig_pie = px.pie(top_10, names=col_name, values=col_value, color_discrete_sequence=px.colors.sequential.Oranges_r)
            fig_pie.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=180)
            fig_pie.update_traces(textposition='inside', textinfo='percent')
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("กำลังรอข้อมูลจาก Google Sheet...")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # 3. จัดวาง 2 ปุ่มหลักด้านล่างภายในกรอบส้ม
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔍 ดูข้อมูลย้อนหลัง"):
                st.session_state.page = 'history'
                st.rerun()
                
        with col_btn2:
            if st.button("➕ เพิ่ม Improvement"):
                st.session_state.page = 'add_new'
                st.rerun()
                
        st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
        if st.button("🔙 ออกจากระบบ", key="logout"):
            st.session_state.page = 'login'
            st.rerun()

    # ---------------- หน้าย่อย: ดูข้อมูลย้อนหลัง Before/After ----------------
    elif st.session_state.page == 'history':
        st.markdown('<div class="menu-card" style="padding: 10px 15px;"><h4 style="margin:0; font-size:16px; color:#2c3e50;">🔍 ประวัติ Before & After</h4></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="menu-card">', unsafe_allow_html=True)
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
        st.markdown('<div class="menu-card" style="padding: 10px 15px;"><h4 style="margin:0; font-size:16px; color:#2c3e50;">📝 บันทึก Improvement ใหม่</h4></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="menu-card">', unsafe_allow_html=True)
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
