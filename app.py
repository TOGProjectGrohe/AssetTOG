import streamlit as st
import pandas as pd
import re

# 1. ตั้งค่าหน้าเว็บพื้นฐานให้กระชับเข้ามุมมองสไตล์สมาร์ทโฟน
st.set_page_config(page_title="TOG App", layout="centered", initial_sidebar_state="collapsed")

# 2. 🛠️ ชุดคำสั่ง CSS จัดโครงสร้างดีไซน์ปุ่มและช่องกรอกลิงก์ให้สวยงาม ส้มพาสเทลคลีน ๆ
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

    /* ดีไซน์ธีมหน้าจอมือถือส้มพาสเทล */
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

    /* ปุ่มทางลัดเปิดโฟลเดอร์ Google Drive สีน้ำเงินเด่นชัด */
    .drive-action-link-btn {
        display: block !important;
        text-align: center !important;
        background-color: #007bc3 !important;
        color: white !important;
        padding: 10px 15px !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        font-size: 13px !important;
        text-decoration: none !important;
        margin-top: 8px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🌐 ฟังก์ชันแปลงลิงก์ Google Drive แชร์ธรรมดา ให้เป็นลิงก์รูปภาพตรงเพื่อนำมาส่องพรีวิวในหน้าแอปได้ทันที
def convert_drive_url_to_embed(url):
    if not url:
        return None
    # แกะสกัดเอา File ID จากลิงก์รูปแบบต่าง ๆ ของ Google Drive
    match = re.search(r'/file/d/([a-zA-Z0-9-_]+)', url)
    if not match:
        match = re.search(r'id=([a-zA-Z0-9-_]+)', url)
    if match:
        file_id = match.group(1)
        # แปลงเป็น URL พรีวิวแบบ Direct Link ของ Google Docs/Drive
        return f"https://docs.google.com/uc?export=view&id={file_id}"
    return None

# 🌐 ฟังก์ชันข้อมูลรายชื่อพนักงานจาก Google Sheet
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

# 🔗 คลังแมปปิ้งลิงก์โฟลเดอร์ Google Drive 18 ปลายทางตรงตามบรีฟเป๊ะ ๆ
DRIVE_MAP = {
    "A": {
        260: {"main_url": "https://drive.google.com/drive/folders/1QTQuQR8e7DUAYQF0yyYreCi9_bGcX6z0?usp=sharing", "main_title": "A_260", "slave_url": "https://drive.google.com/drive/folders/1QTQuQR8e7DUAYQF0yyYreCi9_bGcX6z0?usp=sharing", "slave_title": "SA_260"},
        261: {"main_url": "https://drive.google.com/drive/folders/1phKW7eXcijB4U6P95JHnJm6BgG2bcKyQ?usp=sharing", "main_title": "A_261", "slave_url": "https://drive.google.com/drive/folders/1n5KGFnub6z3urE09taiJh4TaUJXqElCF?usp=sharing", "slave_title": "SA_261"},
        380: {"main_url": "https://drive.google.com/drive/folders/1-77ViPZrWhRXiYMvpa2gTp63CDjxIcHu?usp=sharing", "main_title": "A_380", "slave_url": "https://drive.google.com/drive/folders/1DlKAZot6QPHXdvuVu8ro_TIk26NsznDz?usp=sharing", "slave_title": "SA_380"}
    },
    "B": {
        260: {"main_url": "https://drive.google.com/drive/folders/1NVgoWHj_WTOU7PDdKyozBYJKL7Ap-s4J?usp=sharing", "main_title": "B_260", "slave_url": "https://drive.google.com/drive/folders/1mFPvOUYkuH57QSwkw0nOmFUNsQKhl3Tf?usp=sharing", "slave_title": "SB_260"},
        261: {"main_url": "https://drive.google.com/drive/folders/1q3Kb3ClsvnfulRCug33FoBYlyUvhKz-o?usp=sharing", "main_title": "B_261", "slave_url": "https://drive.google.com/drive/folders/1Kf7jjhN1RIcaQG60uIs6bkDs2aafK8OQ?usp=sharing", "slave_title": "SB_261"},
        380: {"main_url": "https://drive.google.com/drive/folders/1b8jDU2ZJwWuFGihYFVqzbpIVgkH61bhK?usp=sharing", "main_title": "B_380", "slave_url": "https://drive.google.com/drive/folders/179CQ6uNpDen5hao1a949EXpmYLOCu4LQ?usp=sharing", "slave_title": "SB_380"}
    },
    "C": {
        260: {"main_url": "https://drive.google.com/drive/folders/13k1E0lDkRw4BQWKXCz637gHxo5ou7z3V?usp=sharing", "main_title": "C_260", "slave_url": "https://drive.google.com/drive/folders/1P3qw10mB6zs4yC4w3Jd2rOXN6KnmuzNr?usp=sharing", "slave_title": "SC_260"},
        261: {"main_url": "https://drive.google.com/drive/folders/1slgqqMbiRttmRd70hbPkV_DAKoiqGbht?usp=sharing", "main_title": "C_261", "slave_url": "https://drive.google.com/drive/folders/1FzfsI-xDgUQPnB_6kDrQ8iGxI5_N075P?usp=sharing", "slave_title": "SC_261"},
        380: {"main_url": "https://drive.google.com/drive/folders/14jkMpOZG-bIN6h0EYbZ3UrqiFAYUQ7A1?usp=sharing", "main_title": "C_380", "slave_url": "https://drive.google.com/drive/folders/11OR4QaWPaLcM6EPaSPrMkQTQrpfqMMJT?usp=sharing", "slave_title": "SC_380"}
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

# ---------------- หน้าสาม: กรอบละ 1 ภาพ + ลอจิกวางลิงก์แล้วภาพเด้งโชว์คาโปรแกรมทันที ----------------
elif current_page == "defect_view":
    defect = st.session_state.current_defect
    defect_title = f"Defect {defect}"
    
    if st.button("🔙 กลับไปเลือกประเภท Defect อื่น"):
        st.session_state.page = "select_defect"; st.rerun()
        
    st.markdown(f'<div class="login-card" style="text-align:center;"><b>📊 ส่วนคัดเลือกชิ้นงาน Before ของ {defect_title}</b></div>', unsafe_allow_html=True)
    selected_face = st.radio("เลือกพิกัดหน้างานเพื่อดึงข้อมูลคลังภาพ:", ["หน้า A", "หน้า B", "หน้า C"], horizontal=True, key=f"rf_{defect}")
    
    if selected_face in ["หน้า A", "หน้า B", "หน้า C"]:
        face_char = selected_face.split()[-1]
        folder_info = DRIVE_MAP[face_char][defect]
        
        # ----------------------------------------------------
        # 🟢 กรอบที่ 1: ส่วนภาพใหญ่ ก่อนการแก้ไข (กรอบเดี่ยว 1 ปุ่มตามสเปก)
        # ----------------------------------------------------
        st.markdown(f'<div class="login-card">', unsafe_allow_html=True)
        st.markdown(f"<b style='color:#005aab; font-size:13px;'>🖼️ ส่วนที่ 1: เลือกภาพใหญ่ชิ้นงานต้นทาง (คลัง {folder_info['main_title']})</b>", unsafe_allow_html=True)
        
        # 1. พนักงานกดปุ่มสีน้ำเงินเพื่อแวบไปส่องหรือก๊อปปี้ลิงก์ภาพในโฟลเดอร์ Google Drive
        st.markdown(f'<a href="{folder_info["main_url"]}" target="_blank" class="drive-action-link-btn">🔗 1. กดไปก๊อปปี้ลิงก์ภาพในคลังส่องดูภาพจริง</a>', unsafe_allow_html=True)
        
        # 2. นำลิงก์รูปที่พนักงานก๊อปปี้มาวางในช่องนี้เพื่อให้รูปแนบโชว์คาโปรแกรมทันที!
        main_url_input = st.text_input("✍️ 2. วางลิงก์รูปภาพใหญ่ที่นี่เพื่อแนบโชว์:", key=f"input_main_link_{face_char}_{defect}", placeholder="วางลิงก์รูปภาพที่ก๊อปปี้มาจาก Drive...")
        
        if main_url_input.strip() != "":
            embed_main_img = convert_drive_url_to_embed(main_url_input)
            if embed_main_img:
                st.image(embed_main_img, use_container_width=True, caption=f"🖼️ แนบภาพใหญ่จากแฟ้ม {folder_info['main_title']} สำเร็จ!")
            else:
                st.warning("⚠️ ลิงก์ไม่ถูกต้อง โปรดคัดลอกลิงก์แชร์ของ 'ไฟล์รูปภาพ' มาวางแทนลิงก์โฟลเดอร์ครับ")
        st.markdown('</div>', unsafe_allow_html=True)

        # ----------------------------------------------------
        # 🔵 กรอบที่ 2: ส่วนรายละเอียดรูปย่อย (กรอบเดี่ยว 1 ปุ่มตามสเปก)
        # ----------------------------------------------------
        st.markdown(f'<div class="login-card">', unsafe_allow_html=True)
        st.markdown(f"<b style='color:#007bc3; font-size:13px;'>📥 ส่วนที่ 2: เลือกรูปรายละเอียดจุดย่อย (คลัง {folder_info['slave_title']})</b>", unsafe_allow_html=True)
        
        # 1. พนักงานกดปุ่มสีน้ำเงินแวบไปส่องหรือก๊อปปี้ลิงก์ภาพย่อย
        st.markdown(f'<a href="{folder_info["slave_url"]}" target="_blank" class="drive-action-link-btn">🔗 1. กดไปก๊อปปี้ลิงก์ภาพย่อยในคลังส่องดูภาพจริง</a>', unsafe_allow_html=True)
        
        # 2. นำลิงก์รูปย่อยมาวางเพื่อให้ระบบดึงมาแนบโชว์คาโปรแกรมทันที
        slave_url_input = st.text_input("✍️ 2. วางลิงก์รูปภาพย่อยที่นี่เพื่อแนบโชว์:", key=f"input_slave_link_{face_char}_{defect}", placeholder="วางลิงก์รูปภาพย่อยที่ก๊อปปี้มาจาก Drive...")
        
        if slave_url_input.strip() != "":
            embed_slave_img = convert_drive_url_to_embed(slave_url_input)
            if embed_slave_img:
                st.image(embed_slave_img, use_container_width=True, caption=f"📸 แนบภาพรายละเอียดจากแฟ้ม {folder_info['slave_title']} สำเร็จ!")
            else:
                st.warning("⚠️ ลิงก์ไม่ถูกต้อง โปรดคัดลอกลิงก์แชร์ของ 'ไฟล์รูปภาพ' มาวางแทนลิงก์โฟลเดอร์ครับ")
        st.markdown('</div>', unsafe_allow_html=True)

    # 🔲 กรอบปิดท้าย: ส่วนสรุปงานหลังการแก้ไข (AFTER)
    st.markdown('<div class="login-card" style="border-top: 4px solid #10b981;">', unsafe_allow_html=True)
    st.markdown(f"<b style='color:#10b981; font-size:14px; display:block; margin-bottom:5px;'>✨ ส่วนอัปเดตงาน After ({defect_title})</b>", unsafe_allow_html=True)
    st.text_area("พิมพ์ข้อความสรุปรายละเอียดผลงาน After:", value="", key=f"ta_af_{defect}")
    st.camera_input("ถ่ายภาพยืนยันผลงาน After ชิ้นงานจริง", key=f"c_af_{defect}_final")
    st.markdown('</div>', unsafe_allow_html=True)
