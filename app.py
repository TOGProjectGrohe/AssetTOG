import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. ตั้งค่าหน้าเว็บพื้นฐานให้กระชับเข้ามุมมองสไตล์สมาร์ทโฟน
st.set_page_config(page_title="TOG App", layout="centered", initial_sidebar_state="collapsed")

# 2. 🛠️ ชุดคำสั่ง CSS จัดโครงสร้างดีไซน์ปุ่มจิ้มเลือกรูปภาพและการไฮไลท์ขอบเมื่อถูกคลิก
st.markdown("""
    <style>
    /* ซ่อนเมนูส่วนเกินดั้งเดิมของ Streamlit */
    .stDeployButton, [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], header, footer, #MainMenu {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }
    [data-testid="stStatusWidget"], #stConnectionStatus, div[class*="viewerBadge"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* ดีไซน์ธีมหน้าจอมือถือ ส้มพาสเทล */
    .stApp {
        max-width: 420px !important;
        margin: 0px auto !important;
        background: linear-gradient(180deg, #ffb07c 0%, #ffe3d1 30%, #fff7f2 100%) !important;
        border: 12px solid #1e293b !important;
        border-radius: 40px !important;
        padding: 95px 24px 24px 24px !important; 
        box-shadow: 0 20px 50px rgba(0,0,0,0.3) !important;
        min-height: 90vh !important;
        height: auto !important;
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

    /* ตกแต่งการเลือกภาพ */
    .image-gallery-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        margin-top: 10px;
    }
    
    /* สไตล์กล่องภาพเดี่ยวทั่วไป */
    .gallery-item-box {
        border: 2px solid #cbd5e1;
        border-radius: 12px;
        padding: 6px;
        text-align: center;
        background-color: #f8fafc;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
    }
    
    /* สไตล์เมื่อรูปภาพถูกคลิกเลือก (ขอบจะเปลี่ยนเป็นสีน้ำเงินและหนาขึ้นชัดเจน) */
    .gallery-item-box-selected {
        border: 3px solid #007bc3 !important;
        background-color: #eff6ff !important;
        box-shadow: 0 4px 12px rgba(0, 123, 195, 0.15);
    }
    </style>
""", unsafe_allow_html=True)

# 🌐 ฟังก์ชันข้อมูลรายชื่อพนักงาน
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

# 🔗 🔗 ฐานข้อมูลจับคู่ลิงก์โฟลเดอร์ Google Drive ของคุณตรงตามโครงสร้างเงื่อนไขเป๊ะ ๆ
# (หมายเหตุ: สถาปัตยกรรมการดึงรูปภาพของ Google Drive มาโชว์บนหน้าเว็บโดยตรง จะต้องนำ ID หลังคำว่า /folders/ ไปแปลงเป็นลิงก์ภาพพรีวิวต้นทางครับ)
DRIVE_MAP = {
    "A": {
        260: {"main_folder": "1QTQuQR8e7DUAYQF0yyYreCi9_bGcX6z0", "main_title": "A_260", "slave_folder": "1QTQuQR8e7DUAYQF0yyYreCi9_bGcX6z0", "slave_title": "SA_260"},
        261: {"main_folder": "1phKW7eXcijB4U6P95JHnJm6BgG2bcKyQ", "main_title": "A_261", "slave_folder": "1n5KGFnub6z3urE09taiJh4TaUJXqElCF", "slave_title": "SA_261"},
        380: {"main_folder": "1-77ViPZrWhRXiYMvpa2gTp63CDjxIcHu", "main_title": "A_380", "slave_folder": "1DlKAZot6QPHXdvuVu8ro_TIk26NsznDz", "slave_title": "SA_380"}
    },
    "B": {
        260: {"main_folder": "1NVgoWHj_WTOU7PDdKyozBYJKL7Ap-s4J", "main_title": "B_260", "slave_folder": "1mFPvOUYkuH57QSwkw0nOmFUNsQKhl3Tf", "slave_title": "SB_260"},
        261: {"main_folder": "1q3Kb3ClsvnfulRCug33FoBYlyUvhKz-o", "main_title": "B_261", "slave_folder": "1Kf7jjhN1RIcaQG60uIs6bkDs2aafK8OQ", "slave_title": "SB_261"},
        380: {"main_folder": "1b8jDU2ZJwWuFGihYFVqzbpIVgkH61bhK", "main_title": "B_380", "slave_folder": "179CQ6uNpDen5hao1a949EXpmYLOCu4LQ", "slave_title": "SB_380"}
    },
    "C": {
        260: {"main_folder": "13k1E0lDkRw4BQWKXCz637gHxo5ou7z3V", "main_title": "C_260", "slave_folder": "1P3qw10mB6zs4yC4w3Jd2rOXN6KnmuzNr", "slave_title": "SC_260"},
        261: {"main_folder": "1slgqqMbiRttmRd70hbPkV_DAKoiqGbht", "main_title": "C_261", "slave_folder": "1FzfsI-xDgUQPnB_6kDrQ8iGxI5_N075P", "slave_title": "SC_261"},
        380: {"main_folder": "14jkMpOZG-bIN6h0EYbZ3UrqiFAYUQ7A1", "main_title": "C_380", "slave_folder": "11OR4QaWPaLcM6EPaSPrMkQTQrpfqMMJT", "slave_title": "SC_380"}
    }
}

if 'page' not in st.session_state: st.session_state.page = "login"
if 'user_info' not in st.session_state: st.session_state.user_info = None
if 'current_defect' not in st.session_state: st.session_state.current_defect = None

# รักษาสถานะการเลือกภาพในเซสชัน เพื่อไม่ให้รูปภาพเด้งหลุดเวลาทำงานอื่น
if 'selected_main_img' not in st.session_state: st.session_state.selected_main_img = None
if 'selected_slave_imgs' not in st.session_state: st.session_state.selected_slave_imgs = {1: None, 2: None, 3: None, 4: None, 5: None}

current_page = st.session_state.page

# --- แถบนำทางด้านบนสุด ---
st.markdown('<div class="custom-top-navbar"><a href="?nav=reset" target="_self" class="nav-btn-link">🏠 Home</a><a href="?nav=reset" target="_self" class="nav-btn-link">🚪 Logout</a></div>', unsafe_allow_html=True)
if st.query_params.get("nav") == "reset":
    st.session_state.page = "login"; st.session_state.user_info = None; st.session_state.current_defect = None
    st.session_state.selected_main_img = None; st.session_state.selected_slave_imgs = {1: None, 2: None, 3: None, 4: None, 5: None}
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

# ---------------- หน้าสาม: ระบบเลือกรูปภาพแบบจำลองดึงจาก Drive โดยตรง ----------------
elif current_page == "defect_view":
    defect = st.session_state.current_defect
    defect_title = f"Defect {defect}"
    
    if st.button("🔙 กลับไปเลือกประเภท Defect อื่น"):
        st.session_state.page = "select_defect"; st.rerun()
        
    st.markdown(f'<div class="login-card" style="text-align:center;"><b>📊 ส่วนคัดเลือกชิ้นงาน Before ของ {defect_title}</b></div>', unsafe_allow_html=True)
    
    selected_face = st.radio("เลือกพิกัดหน้างานเพื่อกางคลังภาพ:", ["หน้า A", "หน้า B", "หน้า C"], horizontal=True, key=f"rf_{defect}")
    
    if selected_face in ["หน้า A", "หน้า B", "หน้า C"]:
        face_char = selected_face.split()[-1]
        folder_info = DRIVE_MAP[face_char][defect]
        
        # ----------------------------------------------------
        # 🟢 ส่วนที่ 1: แผงแสดงภาพใหญ่ (Main) เพื่อให้จิ้มเลือกรูปภาพคาแอป
        # ----------------------------------------------------
        st.markdown(f'<div class="login-card">', unsafe_allow_html=True)
        st.markdown(f"<b style='color:#005aab; font-size:13px;'>🖼️ ส่วนที่ 1: เลือกภาพใหญ่ชิ้นงานต้นทาง (คลัง {folder_info['main_title']})</b>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:11px; color:#64748b; margin:0;'>*คลิกเลือกรูปภาพที่พนักงานต้องการดึงไปใช้งานจริงด้านล่างนี้:</p>", unsafe_allow_html=True)
        
        # จำลองชุดรูปภาพที่มีสิทธิ์อยู่ในโฟลเดอร์ Google Drive ใหญ่ (เช่นชุดทดสอบรูปภาพตัวอย่าง 3 ภาพ)
        # เวลาใช้งานจริง ลิงก์ตรงรูปภาพจะถูกดึงแบบไร้รอยต่อผ่านโครงสร้างเว็บคอมโพเนนต์
        sample_main_images = [
            {"id": "m1", "url": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=300", "name": "ภาพหลัก_01.jpg"},
            {"id": "m2", "url": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=300", "name": "ภาพหลัก_02.jpg"},
            {"id": "m3", "url": "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=300", "name": "ภาพหลัก_03.jpg"}
        ]
        
        # แสดงผลรูปภาพแบบตาราง เพื่อให้ผู้ใช้คลิกเลือกได้โดยตรงจากหน้าโปรแกรม
        col1, col2, col3 = st.columns(3)
        for idx, img in enumerate(sample_main_images):
            with [col1, col2, col3][idx]:
                is_selected = st.session_state.selected_main_img == img["id"]
                border_class = "gallery-item-box-selected" if is_selected else ""
                
                st.markdown(f"""
                <div class="gallery-item-box {border_class}">
                    <img src="{img['url']}" style="width:100%; border-radius:8px; object-fit:cover; height:70px;">
                    <div style="font-size:10px; font-weight:bold; margin-top:4px; color:#1e293b;">{img['name']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"เลือกภาพที่ {idx+1}", key=f"btn_m_{img['id']}", use_container_width=True):
                    st.session_state.selected_main_img = img["id"]
                    st.rerun()
                    
        if st.session_state.selected_main_img:
            st.info(f"✅ ล็อกรูปภาพใหญ่สำเร็จ (ID รูปภาพ: {st.session_state.selected_main_img})")
        st.markdown('</div>', unsafe_allow_html=True)

        # ----------------------------------------------------
        # 🔵 ส่วนที่ 2: แผงแสดงภาพรายละเอียดจุดย่อย 5 ภาพ (Slave)
        # ----------------------------------------------------
        st.markdown(f'<div class="login-card">', unsafe_allow_html=True)
        st.markdown(f"<b style='color:#007bc3; font-size:13px;'>📥 ส่วนที่ 2: เลือกรูปรายละเอียดจุดย่อย 5 ภาพ (คลัง {folder_info['slave_title']})</b>", unsafe_allow_html=True)
        
        # วนลูปกางแผงตัวเลือกทีละจุด รวม 5 จุดแยกออกจากกันชัดเจนตามเงื่อนไข
        for point_num in range(1, 6):
            st.markdown(f"<span style='font-size:12px; font-weight:bold; color:#1e293b; display:block; margin-top:10px;'>📸 แผงคลังรูปย่อยของ จุดที่ {point_num}:</span>", unsafe_allow_html=True)
            
            # จำลองข้อมูลไฟล์ภาพรายละเอียดใน Folder SA_XX, SB_XX ที่ดึงขึ้นมาให้เลือก
            sample_sub_images = [
                {"id": f"s_{point_num}_1", "url": "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=200", "name": f"ดีเฟคจุด_{point_num}_A.jpg"},
                {"id": f"s_{point_num}_2", "url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=200", "name": f"ดีเฟคจุด_{point_num}_B.jpg"}
            ]
            
            sub_col1, sub_col2 = st.columns(2)
            for s_idx, s_img in enumerate(sample_sub_images):
                with [sub_col1, sub_col2][s_idx]:
                    is_sub_selected = st.session_state.selected_slave_imgs[point_num] == s_img["id"]
                    sub_border_class = "gallery-item-box-selected" if is_sub_selected else ""
                    
                    st.markdown(f"""
                    <div class="gallery-item-box {sub_border_class}">
                        <img src="{s_img['url']}" style="width:100%; border-radius:8px; object-fit:cover; height:60px;">
                        <div style="font-size:9px; color:#475569; margin-top:2px;">{s_img['name']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"เลือกภาพนี้", key=f"btn_s_{s_img['id']}", use_container_width=True):
                        st.session_state.selected_slave_imgs[point_num] = s_img["id"]
                        st.rerun()
                        
            if st.session_state.selected_slave_imgs[point_num]:
                st.markdown(f"<span style='font-size:11px; color:#16a34a; font-weight:bold;'>✔️ ล็อกภาพจุดที่ {point_num} เรียบร้อยแล้ว</span>", unsafe_allow_html=True)
            st.markdown("<div style='border-top:1px solid #f1f5f9; margin-top:8px;'></div>", unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    # 🔲 กรอบย่อยส่วนปิดท้าย: ส่วนสรุปรายละเอียดงาน AFTER 
    st.markdown('<div class="login-card" style="border-top: 4px solid #10b981;">', unsafe_allow_html=True)
    st.markdown(f"<b style='color:#10b981; font-size:14px; display:block; margin-bottom:5px;'>✨ ส่วนอัปเดตงาน After ({defect_title})</b>", unsafe_allow_html=True)
    st.text_area("พิมพ์ข้อความสรุปรายละเอียดผลงาน After:", value="", key=f"ta_af_{defect}")
    st.camera_input("ถ่ายภาพยืนยันผลงาน After ชิ้นงานจริง", key=f"c_af_{defect}_final")
    st.markdown('</div>', unsafe_allow_html=True)
