import streamlit as st
import pandas as pd
import requests
import re

# 1. ตั้งค่าหน้าเว็บสไตล์สมาร์ทโฟน
st.set_page_config(page_title="TOG App", layout="centered", initial_sidebar_state="collapsed")

# 2. 🎨 CSS ธีมส้มพาสเทล + แผงคัดเลือกรูปภาพสไตล์ Shopping App (กรอบหนาเมื่อเลือกสำเร็จ)
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
    .tog-center-logo {
        width: 50px; height: 50px; background-color: #000000; border-radius: 50%; display: flex; justify-content: center; align-items: center; color: #ffffff; font-weight: bold; font-size: 15px; margin-bottom: 8px;
    }
    
    /* 📦 แผงเลือกรูปสไตล์ Shopping App ของจริง */
    .shop-image-card {
        border: 2px solid #e2e8f0; border-radius: 16px; padding: 8px; text-align: center;
        background-color: #ffffff; transition: all 0.2s ease-in-out; margin-bottom: 12px;
    }
    .shop-image-card-selected {
        border: 4px solid #005aab !important; background-color: #e0f2fe !important;
        box-shadow: 0 8px 25px rgba(0, 90, 171, 0.3) !important; transform: scale(1.02);
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

# 📸 ฟังก์ชันดึงภาพสดจาก Google Drive โฟลเดอร์จริงแบบไม่ต้องใช้คีย์ API (ใช้สิทธิ์เปิดแชร์สาธารณะ)
@st.cache_data(ttl=600, show_spinner="🔄 กำลังดึงรูปภาพชิ้นงานจริงจากคลัง Google Drive...")
def get_actual_images_from_drive(folder_id):
    images = []
    # ใช้เทคนิคจำลองแอปเพื่อไปดึงรายชื่อรูปภาพจากหน้าเว็บ Google Drive ที่เปิดแชร์ไว้
    url = f"https://drive.google.com/embeddedfolderview?id={folder_id}"
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            # ค้นหารหัสไฟล์รูปภาพที่ซ่อนอยู่ในหน้าคลังเก็บของกูเกิล
            matches = re.findall(r'\["([^"]+)"\s*,\s*"([^"]+)"\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*"image/', response.text)
            for m in matches:
                f_id, f_name = m[0], m[1]
                # แปลงรหัสไฟล์ให้กลายเป็นลิงก์แสดงภาพตรง (Direct View URL) คาหน้าแอป
                direct_img_url = f"https://drive.google.com/uc?export=view&id={f_id}"
                images.append({"id": f_id, "name": f_name, "url": direct_img_url})
    except:
        pass
    return images

# 🔗 รายชื่อรหัสโฟลเดอร์ Google Drive ของจริง 100% ทั้ง 18 ตัวที่คุณส่งมาให้ผม
DRIVE_MAP = {
    "A": {
        260: {"main_id": "1QTQuQR8e7DUAYQF0yyYreCi9_bGcX6z0", "main_title": "คลังภาพใหญ่ A_260", "slave_id": "1QTQuQR8e7DUAYQF0yyYreCi9_bGcX6z0", "slave_title": "คลังย่อย SA_260"},
        261: {"main_id": "1phKW7eXcijB4U6P95JHnJm6BgG2bcKyQ", "main_title": "คลังภาพใหญ่ A_261", "slave_id": "1n5KGFnub6z3urE09taiJh4TaUJXqElCF", "slave_title": "คลังย่อย SA_261"},
        380: {"main_id": "1-77ViPZrWhRXiYMvpa2gTp63CDjxIcHu", "main_title": "คลังภาพใหญ่ A_380", "slave_id": "1DlKAZot6QPHXdvuVu8ro_TIk26NsznDz", "slave_title": "คลังย่อย SA_380"}
    },
    "B": {
        260: {"main_id": "1NVgoWHj_WTOU7PDdKyozBYJKL7Ap-s4J", "main_title": "คลังภาพใหญ่ B_260", "slave_id": "1mFPvOUYkuH57QSwkw0nOmFUNsQKhl3Tf", "slave_title": "คลังย่อย SB_260"},
        261: {"main_id": "1q3Kb3ClsvnfulRCug33FoBYlyUvhKz-o", "main_title": "คลังภาพใหญ่ B_261", "slave_id": "1Kf7jjhN1RIcaQG60uIs6bkDs2aafK8OQ", "slave_title": "คลังย่อย SB_261"},
        380: {"main_id": "1b8jDU2ZJwWuFGihYFVqzbpIVgkH61bhK", "main_title": "คลังภาพใหญ่ B_380", "slave_id": "179CQ6uNpDen5hao1a949EXpmYLOCu4LQ", "slave_title": "คลังย่อย SB_380"}
    },
    "C": {
        260: {"main_id": "13k1E0lDkRw4BQWKXCz637gHxo5ou7z3V", "main_title": "คลังภาพใหญ่ C_260", "slave_id": "1P3qw10mB6zs4yC4w3Jd2rOXN6KnmuzNr", "slave_title": "คลังย่อย SC_260"},
        261: {"main_id": "1slgqqMbiRttmRd70hbPkV_DAKoiqGbht", "main_title": "คลังภาพใหญ่ C_261", "slave_id": "1FzfsI-xDgUQPnB_6kDrQ8iGxI5_N075P", "slave_title": "คลังย่อย SC_261"},
        380: {"main_id": "14jkMpOZG-bIN6h0EYbZ3UrqiFAYUQ7A1", "main_title": "คลังภาพใหญ่ C_380", "slave_id": "11OR4QaWPaLcM6EPaSPrMkQTQrpfqMMJT", "slave_title": "คลังย่อย SC_380"}
    }
}

if 'page' not in st.session_state: st.session_state.page = "login"
if 'user_info' not in st.session_state: st.session_state.user_info = None
if 'current_defect' not in st.session_state: st.session_state.current_defect = None
if 'picked_main_id' not in st.session_state: st.session_state.picked_main_id = None
if 'picked_slave_id' not in st.session_state: st.session_state.picked_slave_id = None

current_page = st.session_state.page

st.markdown('<div class="custom-top-navbar"><a href="?nav=reset" target="_self" class="nav-btn-link">🏠 Home</a><a href="?nav=reset" target="_self" class="nav-btn-link">🚪 Logout</a></div>', unsafe_allow_html=True)
if st.query_params.get("nav") == "reset":
    st.session_state.page = "login"; st.session_state.user_info = None; st.session_state.current_defect = None
    st.session_state.picked_main_id = None; st.session_state.picked_slave_id = None
    st.query_params.clear(); st.rerun()

st.markdown('<div class="center-header-block"><div class="tog-center-logo">TOG</div><span style="font-size:18px; font-weight:bold; color:white;">TOG App</span></div>', unsafe_allow_html=True)

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

# ---------------- หน้าสาม: 🛍️ แผงช้อปปิ้งออนไลน์ ดึงรูปภาพจริงจาก Google Drive มาโชว์คาแอปจริง ----------------
elif current_page == "defect_view":
    defect = st.session_state.current_defect
    defect_title = f"Defect {defect}"
    
    if st.button("🔙 กลับไปเลือกประเภท Defect อื่น"):
        st.session_state.page = "select_defect"; st.rerun()
        
    st.markdown(f'<div class="login-card" style="text-align:center;"><b>📊 แผงเลือกรูป Before ของ {defect_title}</b></div>', unsafe_allow_html=True)
    selected_face = st.radio("เลือกพิกัดหน้างาน:", ["หน้า A", "หน้า B", "หน้า C"], horizontal=True, key=f"rf_{defect}")
    
    if selected_face in ["หน้า A", "หน้า B", "หน้า C"]:
        face_char = selected_face.split()[-1]
        folder_info = DRIVE_MAP[face_char][defect]
        
        # 🟢 ส่วนที่ 1: ดึงภาพใหญ่จริงจาก Google Drive มาสตรีมโชว์คาจอ
        st.markdown(f'<div class="login-card">', unsafe_allow_html=True)
        st.markdown(f"<b style='color:#005aab; font-size:13px;'>🛒 ส่วนที่ 1: จิ้มเลือกภาพใหญ่ ({folder_info['main_title']})</b>", unsafe_allow_html=True)
        
        main_images = get_actual_images_from_drive(folder_info['main_id'])
        if main_images:
            for img in main_images:
                is_picked = st.session_state.picked_main_id == img['id']
                card_style = "shop-image-card-selected" if is_picked else "shop-image-card"
                
                # พ่นโครงรูปภาพของจริงจาก Google Drive ขึ้นจอโทรศัพท์จำลอง
                st.markdown(f"""
                <div class="{card_style}">
                    <img src="{img['url']}" style="width:100%; max-height:160px; object-fit:contain; border-radius:10px;">
                    <div style="font-size:12px; font-weight:bold; margin-top:6px; color:#1e293b;">{img['name']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"👇 คลิกเลือกรูป: {img['name']}", key=f"btn_m_{img['id']}", use_container_width=True):
                    st.session_state.picked_main_id = img['id']
                    st.rerun()
        else:
            st.warning("⚠️ ไม่พบรูปภาพในโฟลเดอร์นี้ หรือยังไม่ได้เปิดแชร์โฟลเดอร์เป็นสาธารณะ")
        st.markdown('</div>', unsafe_allow_html=True)

        # 🔵 ส่วนที่ 2: ดึงภาพรายละเอียดจุดย่อยจริงมาสตรีมโชว์คาจอ
        st.markdown(f'<div class="login-card">', unsafe_allow_html=True)
        st.markdown(f"<b style='color:#007bc3; font-size:13px;'>🛒 ส่วนที่ 2: จิ้มเลือกภาพย่อย ({folder_info['slave_title']})</b>", unsafe_allow_html=True)
        
        slave_images = get_actual_images_from_drive(folder_info['slave_id'])
        if slave_images:
            for img_s in slave_images:
                is_s_picked = st.session_state.picked_slave_id == img_s['id']
                card_s_style = "shop-image-card-selected" if is_s_picked else "shop-image-card"
                
                st.markdown(f"""
                <div class="{card_s_style}">
                    <img src="{img_s['url']}" style="width:100%; max-height:160px; object-fit:contain; border-radius:10px;">
                    <div style="font-size:11px; margin-top:6px; color:#475569;">{img_s['name']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"👇 คลิกเลือกรูปย่อย: {img_s['name']}", key=f"btn_s_{img_s['id']}", use_container_width=True):
                    st.session_state.picked_slave_id = img_s['id']
                    st.rerun()
        else:
            st.warning("⚠️ ไม่พบรูปภาพรายละเอียดในโฟลเดอร์นี้")
        st.markdown('</div>', unsafe_allow_html=True)

    # 🔲 ส่วนสรุปผลงาน AFTER
    st.markdown('<div class="login-card" style="border-top: 4px solid #10b981;">', unsafe_allow_html=True)
    st.markdown(f"<b style='color:#10b981; font-size:14px; display:block; margin-bottom:5px;'>✨ ส่วนอัปเดตงาน After ({defect_title})</b>", unsafe_allow_html=True)
    st.text_area("พิมพ์ข้อความสรุปรายละเอียดผลงาน After:", value="", key=f"ta_af_{defect}")
    st.camera_input("ถ่ายภาพยืนยันผลงาน After ชิ้นงานจริง", key=f"c_af_{defect}_final")
    st.markdown('</div>', unsafe_allow_html=True)
