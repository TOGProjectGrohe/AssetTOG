import streamlit as st
import pandas as pd
import requests

# 1. ตั้งค่าหน้าเว็บสไตล์สมาร์ทโฟน
st.set_page_config(page_title="TOG App", layout="centered", initial_sidebar_state="collapsed")

# 2. 🎨 CSS ตกแต่งหน้าจอธีมส้มพาสเทล และแผงภาพสไตล์ Shopping Online (ดึงภาพสด ไม่รกเครื่องพนักงาน)
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
    
    /* 📦 แผงเลือกรูปสไตล์ Shopping App */
    .shop-image-card {
        border: 2px solid #e2e8f0; border-radius: 16px; padding: 8px; text-align: center;
        background-color: #ffffff; transition: all 0.2s ease-in-out; margin-bottom: 12px;
    }
    .shop-image-card-selected {
        border: 3.5px solid #007bc3 !important; background-color: #f0f7ff !important;
        box-shadow: 0 8px 20px rgba(0, 123, 195, 0.2) !important; transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# 🌐 ฟังก์ชันข้อมูลพนักงานจาก Google Sheet (คงไว้เหมือนเดิม)
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

# 🌐 ฟังก์ชันดึงภาพสดจาก Microsoft OneDrive (ไม่ต้องผุกบัตรเครดิต)
@st.cache_resource(show_spinner="🔄 กำลังสแกนรูปภาพจาก Microsoft OneDrive...")
def get_images_from_onedrive(folder_id):
    # ตรงนี้อนาคตเราจะเอา Access Token ของ Microsoft มาใส่แทนคีย์กุญแจของกูเกิลครับ
    access_token = "YOUR_MICROSOFT_ACCESS_TOKEN"
    
    # ถ้าใส่คีย์แล้ว มันจะยิงไปดึงรูปภาพจากโฟลเดอร์ของ OneDrive ตรงๆ
    if access_token != "YOUR_MICROSOFT_ACCESS_TOKEN":
        try:
            url = f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}/children"
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(url, headers=headers).json()
            
            image_list = []
            for item in response.get('value', []):
                if 'image' in item:
                    image_list.append({
                        "id": item['id'], "name": item['name'],
                        "embed_url": item['@microsoft.graph.downloadUrl'] # ลิงก์รูปภาพตรงของไมโครซอฟท์
                    })
            return image_list
        except:
            pass

    # ระบบจำลองรูปภาพจริงให้เห็นความสวยงามก่อนเชื่อมต่อคีย์จริง
    return [
        {"id": "od_1", "name": "รูปชิ้นงานจากOneDrive_01.jpg", "embed_url": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=300"},
        {"id": "od_2", "name": "รูปชิ้นงานจากOneDrive_02.jpg", "embed_url": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=300"}
    ]

# 🔗 คลังจับคู่รหัสโฟลเดอร์ของ Microsoft OneDrive (เปลี่ยนจากลิงก์ Google Drive)
# อนาคตเราแค่เอา ID โฟลเดอร์ที่อยู่บน OneDrive มากรอกแทนที่ตัวเลขจำลองด้านล่างนี้ครับ
ONEDRIVE_MAP = {
    "A": {
        260: {"main_id": "OD_FOLDER_ID_A_260", "main_title": "A_260", "slave_id": "OD_FOLDER_ID_SA_260", "slave_title": "SA_260"},
        261: {"main_id": "OD_FOLDER_ID_A_261", "main_title": "A_261", "slave_id": "OD_FOLDER_ID_SA_261", "slave_title": "SA_261"},
        380: {"main_id": "OD_FOLDER_ID_A_380", "main_title": "A_380", "slave_id": "OD_FOLDER_ID_SA_380", "slave_title": "SA_380"}
    },
    "B": {
        260: {"main_id": "OD_FOLDER_ID_B_260", "main_title": "B_260", "slave_id": "OD_FOLDER_ID_SB_260", "slave_title": "SB_260"},
        261: {"main_id": "OD_FOLDER_ID_B_261", "main_title": "B_261", "slave_id": "OD_FOLDER_ID_SB_261", "slave_title": "SB_261"},
        380: {"main_id": "OD_FOLDER_ID_B_380", "main_title": "B_380", "slave_id": "OD_FOLDER_ID_SB_380", "slave_title": "SB_380"}
    },
    "C": {
        260: {"main_id": "OD_FOLDER_ID_C_260", "main_title": "C_260", "slave_id": "OD_FOLDER_ID_SC_260", "slave_title": "SC_260"},
        261: {"main_id": "OD_FOLDER_ID_C_261", "main_title": "C_261", "slave_id": "OD_FOLDER_ID_SC_261", "slave_title": "SC_261"},
        380: {"main_id": "OD_FOLDER_ID_C_380", "main_title": "C_380", "slave_id": "OD_FOLDER_ID_SC_380", "slave_title": "SC_380"}
    }
}

if 'page' not in st.session_state: st.session_state.page = "login"
if 'user_info' not in st.session_state: st.session_state.user_info = None
if 'current_defect' not in st.session_state: st.session_state.current_defect = None
if 'selected_main_photo_id' not in st.session_state: st.session_state.selected_main_photo_id = None
if 'selected_slave_photo_id' not in st.session_state: st.session_state.selected_slave_photo_id = None

current_page = st.session_state.page

st.markdown('<div class="custom-top-navbar"><a href="?nav=reset" target="_self" class="nav-btn-link">🏠 Home</a><a href="?nav=reset" target="_self" class="nav-btn-link">🚪 Logout</a></div>', unsafe_allow_html=True)
if st.query_params.get("nav") == "reset":
    st.session_state.page = "login"; st.session_state.user_info = None; st.session_state.current_defect = None
    st.session_state.selected_main_photo_id = None; st.session_state.selected_slave_photo_id = None
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

# ---------------- หน้าสาม: 🛍️ ระบบคัดรูปสไตล์ร้านช้อปปิ้งออนไลน์ ดึงรูปภาพสดจาก OneDrive (กรอบละ 1 รูปถ้วน) ----------------
elif current_page == "defect_view":
    defect = st.session_state.current_defect
    defect_title = f"Defect {defect}"
    
    if st.button("🔙 กลับไปเลือกประเภท Defect อื่น"):
        st.session_state.page = "select_defect"; st.rerun()
        
    st.markdown(f'<div class="login-card" style="text-align:center;"><b>📊 ส่วนคัดเลือกชิ้นงาน Before ของ {defect_title}</b></div>', unsafe_allow_html=True)
    selected_face = st.radio("เลือกพิกัดหน้างาน:", ["หน้า A", "หน้า B", "หน้า C"], horizontal=True, key=f"rf_{defect}")
    
    if selected_face in ["หน้า A", "หน้า B", "หน้า C"]:
        face_char = selected_face.split()[-1]
        folder_info = ONEDRIVE_MAP[face_char][defect]
        
        # 🟢 กรอบที่ 1: ภาพใหญ่ (ดึงสดจาก OneDrive คลังหลัก)
        st.markdown(f'<div class="login-card">', unsafe_allow_html=True)
        st.markdown(f"<b style='color:#005aab; font-size:13px;'>🛒 ส่วนที่ 1: จิ้มเลือกภาพใหญ่ต้นทาง (คลัง OneDrive: {folder_info['main_title']})</b>", unsafe_allow_html=True)
        
        main_photos = get_images_from_onedrive(folder_info['main_id'])
        if main_photos:
            for item in main_photos:
                is_picked = st.session_state.selected_main_photo_id == item['id']
                selected_css = "shop-image-card-selected" if is_picked else ""
                
                st.markdown(f"""
                <div class="shop-image-card {selected_css}">
                    <img src="{item['embed_url']}" style="width:100%; max-height:160px; object-fit:contain; border-radius:10px;">
                    <div style="font-size:12px; font-weight:bold; margin-top:6px; color:#1e293b;">{item['name']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"👇 เลือกรูปภาพ: {item['name']}", key=f"pick_main_{item['id']}", use_container_width=True):
                    st.session_state.selected_main_photo_id = item['id']
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # 🔵 กรอบที่ 2: ภาพรายละเอียดจุดย่อย (ดึงสดจาก OneDrive คลังย่อย - เหลือ 1 รูปถ้วนตามสเปก)
        st.markdown(f'<div class="login-card">', unsafe_allow_html=True)
        st.markdown(f"<b style='color:#007bc3; font-size:13px;'>🛒 ส่วนที่ 2: จิ้มเลือกภาพรายละเอียด (คลัง OneDrive: {folder_info['slave_title']})</b>", unsafe_allow_html=True)
        
        slave_photos = get_images_from_onedrive(folder_info['slave_id'])
        if slave_photos:
            for sub_item in slave_photos:
                is_sub_picked = st.session_state.selected_slave_photo_id == sub_item['id']
                sub_selected_css = "shop-image-card-selected" if is_sub_picked else ""
                
                st.markdown(f"""
                <div class="shop-image-card {sub_selected_css}">
                    <img src="{sub_item['embed_url']}" style="width:100%; max-height:160px; object-fit:contain; border-radius:10px;">
                    <div style="font-size:11px; margin-top:6px; color:#475569;">{sub_item['name']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"👇 เลือกรูปภาพ: {sub_item['name']}", key=f"pick_slave_{sub_item['id']}", use_container_width=True):
                    st.session_state.selected_slave_photo_id = sub_item['id']
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # 🔲 ส่วนสรุปรายละเอียดงาน AFTER
    st.markdown('<div class="login-card" style="border-top: 4px solid #10b981;">', unsafe_allow_html=True)
    st.markdown(f"<b style='color:#10b981; font-size:14px; display:block; margin-bottom:5px;'>✨ ส่วนอัปเดตงาน After ({defect_title})</b>", unsafe_allow_html=True)
    st.text_area("พิมพ์ข้อความสรุปรายละเอียดผลงาน After:", value="", key=f"ta_af_{defect}")
    st.camera_input("ถ่ายภาพยืนยันผลงาน After ชิ้นงานจริง", key=f"c_af_{defect}_final")
    st.markdown('</div>', unsafe_allow_html=True)
