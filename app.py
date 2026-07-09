import streamlit as st
import pandas as pd
import requests

# 1. ตั้งค่าหน้าเว็บสไตล์สมาร์ทโฟน
st.set_page_config(page_title="TOG App", layout="centered", initial_sidebar_state="collapsed")

# 2. 🎨 CSS ตกแต่งหน้าจอโทรศัพท์ธีมพาสเทลและกล่องช้อปปิ้งออนไลน์
st.markdown("""
    <style>
    .stDeployButton, [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], header, footer, #MainMenu {
        display: none !important; visibility: hidden !important; height: 0 !important;
    }
    [data-testid="stStatusWidget"], #stConnectionStatus, div[class*="viewerBadge"] {
        display: none !important; visibility: hidden !important;
    }
    .stApp {
        max-width: 420px !important; margin: 0px auto !important;
        background: linear-gradient(180deg, #ffb07c 0%, #ffe3d1 30%, #fff7f2 100%) !important;
        border: 12px solid #1e293b !important; border-radius: 40px !important;
        padding: 95px 24px 24px 24px !important; box-shadow: 0 20px 50px rgba(0,0,0,0.3) !important;
        min-height: 90vh !important; height: auto !important;
    }
    .login-card {
        background-color: white !important; border-radius: 20px !important; padding: 15px !important; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important; margin-bottom: 15px !important; width: 100% !important;
    }
    .custom-top-navbar {
        position: absolute !important; top: 20px !important; left: 20px !important; right: 20px !important; display: flex !important; justify-content: space-between !important; align-items: center !important; z-index: 999999 !important;
    }
    .nav-btn-link {
        background-color: #007bc3 !important; color: white !important; border-radius: 20px !important; padding: 8px 16px !important; font-size: 13px !important; font-weight: bold !important; text-decoration: none !important;
    }
    .center-header-block {
        display: flex !important; flex-direction: column !important; align-items: center !important; justify-content: center !important; text-align: center !important; margin-top: 10px !important; margin-bottom: 25px !important; width: 100% !important;
    }
    
    /* 📦 กล่องดีไซน์แผงพรีวิวรูปภาพคาหน้าแอป */
    .preview-shop-card {
        border: 2px solid #e2e8f0; border-radius: 16px; padding: 12px; text-align: center;
        background-color: #ffffff; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    </style>
""", unsafe_allow_html=True)

# 🌐 ฟังก์ชันดึงข้อมูลพนักงานจาก Google Sheet
def get_employee_from_sheet(input_id):
    sheet_id = "1sRher870S-P1w_kUVfryy-OqM67WjGpwek9y9wm29Ps"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        if 'ID' in df.columns:
            df['ID'] = df['ID'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
            match = df[df['ID'] == str(input_id).strip()]
            if not match.empty:
                row = match.iloc[0]
                return {"status": "success", "found": True, "id": str(row['ID']), "name": str(row['Name']).strip()}
    except:
        pass
    return {"status": "success", "found": False}

# 🌐 ฟังก์ชันดาวน์โหลดดึงรูปภาพสดมาเก็บในหน่วยความจำ เพื่อให้กดปุ่มดาวน์โหลดบนหน้าเว็บได้ทันที
@st.cache_data(show_spinner=False)
def fetch_image_bytes(url):
    try:
        return requests.get(url, timeout=10).content
    except:
        return b""

# 🔗 ฐานข้อมูลแมปปิ้งลิงก์ไฟล์รูปภาพจริง (อันนี้ผมใส่ URL รูปงานจริงจำลองไว้เพื่อให้คุณวีรพันธ์เห็นภาพความสวยงามครับ)
# อนาคตพอคุณเอารูปไปอัปโหลดขึ้น GitHub หรือโฮสติ้งฟรี ก็เอาลิงก์ตรงของรูปภาพมาแปะแทนที่ได้เลยครับ
IMAGE_DATA_MAP = {
    "A": {
        260: [
            {"name": "ชิ้นงานต้นทาง_A1.jpg", "url": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=500"},
            {"name": "ชิ้นงานต้นทาง_A2.jpg", "url": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=500"}
        ]
    }
}

if 'page' not in st.session_state: st.session_state.page = "login"
if 'user_info' not in st.session_state: st.session_state.user_info = None
if 'current_defect' not in st.session_state: st.session_state.current_defect = None

current_page = st.session_state.page

st.markdown('<div class="custom-top-navbar"><a href="?nav=reset" target="_self" class="nav-btn-link">🏠 Home</a><a href="?nav=reset" target="_self" class="nav-btn-link">🚪 Logout</a></div>', unsafe_allow_html=True)
if st.query_params.get("nav") == "reset":
    st.session_state.page = "login"; st.session_state.user_info = None; st.session_state.current_defect = None
    st.query_params.clear(); st.rerun()

st.markdown('<div class="center-header-block"><div style="width:50px; height:50px; background-color:#000000; border-radius:50%; display:flex; justify-content:center; align-items:center; color:#ffffff; font-weight:bold; font-size:15px; margin:0 auto 8px auto;">TOG</div><span style="font-size:18px; font-weight:bold; color:white;">TOG App</span></div>', unsafe_allow_html=True)

# ---------------- หน้าแรก: Login ----------------
if current_page == "login":
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='font-size:16px; margin-top:0; color:#2c3e50; text-align:center;'>🪪 ป้อนรหัสพนักงานเพื่อเข้าระบบ</h4>", unsafe_allow_html=True)
    input_id = st.text_input("กรอกรหัส ID พนักงานของคุณ:", value="", placeholder="พิมพ์ตัวเลขรหัส เช่น 20", label_visibility="collapsed")
    if input_id.strip() != "":
        result = get_employee_from_sheet(input_id)
        if result["status"] == "success" and result.get("found"):
            st.markdown(f'<div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 10px; border-radius: 12px; margin-top: 10px; text-align: center; font-size:13px; color:#16a34a;"><b>✅ ข้อมูลถูกต้อง:</b> {result["name"]}</div>', unsafe_allow_html=True)
            if st.button("🔓 กดเพื่อเข้าระบบ"):
                st.session_state.user_info = {"id": result["id"], "name": result["name"]}
                st.session_state.page = "select_defect"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- หน้าสอง: คัดเลือก Defect ----------------
elif current_page == "select_defect":
    st.markdown('<div class="login-card" style="text-align:center;"><b>🎯 โปรดเลือกประเภท Defect เพื่อตรวจสอบคลังงาน:</b></div>', unsafe_allow_html=True)
    if st.button("🟠 ดูข้อมูล Defect 260 (Rough Lines)"):
        st.session_state.current_defect = 260; st.session_state.page = "defect_view"; st.rerun()
    if st.button("🔵 ดูข้อมูล Defect 261 (Grinding Structure)"):
        st.session_state.current_defect = 261; st.session_state.page = "defect_view"; st.rerun()
    if st.button("⚫ ดูข้อมูล Defect 380 (Contour/Design Fault)"):
        st.session_state.current_defect = 380; st.session_state.page = "defect_view"; st.rerun()

# ---------------- หน้าสาม: 🛍️ ระบบกางรูปภาพของจริงสไตล์แอปช้อปปิ้ง + ปุ่มกดเซฟดาวน์โหลดคาแอปทันที ----------------
elif current_page == "defect_view":
    defect = st.session_state.current_defect
    defect_title = f"Defect {defect}"
    
    if st.button("🔙 กลับไปเลือกประเภท Defect อื่น"):
        st.session_state.page = "select_defect"; st.rerun()
        
    st.markdown(f'<div class="login-card" style="text-align:center;"><b>📊 แผงเลือกรูปชิ้นงานของ {defect_title}</b></div>', unsafe_allow_html=True)
    selected_face = st.radio("เลือกพิกัดหน้างาน:", ["หน้า A", "หน้า B", "หน้า C"], horizontal=True, key=f"rf_{defect}")
    
    if selected_face == "หน้า A" and defect == 260:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#005aab; font-size:14px; display:block; margin-bottom:10px;'>🖼️ รูปภาพของจริงในคลัง (จิ้มปุ่มเพื่อเซฟรูปได้ทันที)</b>", unsafe_allow_html=True)
        
        # ดึงข้อมูลลิสต์รูปภาพจริงออกมากางบนหน้าจอแอป
        photo_items = IMAGE_DATA_MAP["A"][260]
        
        for item in photo_items:
            st.markdown(f"""
            <div class="preview-shop-card">
                <img src="{item['url']}" style="width:100%; max-height:180px; object-fit:contain; border-radius:10px;">
                <div style="font-size:13px; font-weight:bold; margin-top:8px; color:#1e293b;">{item['name']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 📥 ดาวน์โหลดรูปภาพเก็บเข้าแรมแบบสด ๆ 
            img_bytes = fetch_image_bytes(item['url'])
            
            # ปุ่มดาวน์โหลดของตัวแอป Streamlit โดยตรง พนักงานจิ้มปุ๊บ รูปเซฟลงมือถือทันที!
            st.download_button(
                label=f"💾 กดดาวน์โหลดรูป: {item['name']}",
                data=img_bytes,
                file_name=item['name'],
                mime="image/jpeg",
                key=f"dl_{item['name']}",
                use_container_width=True
            )
            st.markdown("<br>", unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 📂 กล่องรับรูปภาพกลับเข้ามาแนบประวัติหลังจากพนักงานเซฟไปแล้ว
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("<b style='font-size:13px; color:#475569;'>📥 แนบรูปภาพที่ดาวน์โหลดมาเข้าสู่ระบบงาน:</b>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("กดจิ้มที่กล่องนี้เพื่อเลือกรูปภาพจากอัลบั้มมาแปะคาแอปเพื่อส่งงาน:", type=["jpg", "png", "jpeg"], key="manual_up")
        if uploaded_file:
            st.image(uploaded_file, caption="✅ รูปภาพที่คุณเลือกแนบสำเร็จ!", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("📂 ส่วนจัดเก็บภาพจริงของแผนกอื่น ๆ กำลังรอคุณวีรพันธ์นำลิงก์รูปภาพมาแปะเชื่อมต่อหลังบ้านครับ")

    # 🔲 ส่วนสรุปรายละเอียดงาน AFTER
    st.markdown('<div class="login-card" style="border-top: 4px solid #10b981;">', unsafe_allow_html=True)
    st.markdown(f"<b style='color:#10b981; font-size:14px; display:block; margin-bottom:5px;'>✨ ส่วนอัปเดตงาน After ({defect_title})</b>", unsafe_allow_html=True)
    st.text_area("พิมพ์ข้อความสรุปรายละเอียดผลงาน After:", value="", key=f"ta_af_{defect}")
    st.camera_input("ถ่ายภาพยืนยันผลงาน After ชิ้นงานจริง", key=f"c_af_{defect}_final")
    st.markdown('</div>', unsafe_allow_html=True)
