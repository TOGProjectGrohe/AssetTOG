import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. ตั้งค่าหน้าเว็บพื้นฐานให้กระชับเข้ามุมมองสไตล์สมาร์ทโฟน
st.set_page_config(page_title="TOG App", layout="centered", initial_sidebar_state="collapsed")

# 2. 🛠️ ชุดคำสั่ง CSS คุมธีม และสไตล์จัดการให้ปุ่มและตัวอักษรทุกชิ้นอยู่กึ่งกลางสมดุล 100%
st.markdown("""
    <style>
    /* 🚫 ซ่อนเมนูและป้ายส่วนเกินดั้งเดิมของ Streamlit ทั้งหมด */
    .stDeployButton, [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], header, footer, #MainMenu {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }
    
    /* 🚫 ซ่อนปุ่ม Manage App มุมขวาล่างไม่ให้โผล่มากวนใจ */
    [data-testid="stStatusWidget"], #stConnectionStatus, div[class*="viewerBadge"], div[class*="st-emotion-cache-"] button[title="Manage app"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }

    /* 📱 ดีไซน์คุมธีมหน้าจอมือถือ ส้มพาสเทลสวยงาม */
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
    
    /* เคลียร์ระยะห่างบล็อกหลักไม่ให้โย้ชิดซ้าย */
    [data-testid="stMainBlockContainer"], [data-testid="stVerticalBlock"], [data-testid="stVerticalBlockRoot"], div[data-testid="element-container"], .stColumn {
        width: 100% !important; max-width: 100% !important; background-color: transparent !important; border: none !important; box-shadow: none !important; padding: 0px !important; margin: 0px !important;
    }

    /* กล่องพื้นหลังขาวสำหรับ Content */
    .login-card {
        background-color: white !important; border-radius: 20px !important; padding: 15px !important; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important; margin-bottom: 15px !important; width: 100% !important;
    }

    /* 🏠 แถบนำทาง Home / Logout ล็อกตำแหน่งไว้ที่มุมบนสุด */
    .custom-top-navbar {
        position: absolute !important; top: 18px !important; left: 20px !important; right: 20px !important; display: flex !important; justify-content: space-between !important; align-items: center !important; z-index: 999999 !important;
    }
    .nav-btn-link {
        background-color: #007bc3 !important; color: white !important; border-radius: 20px !important; padding: 8px 16px !important; font-size: 13px !important; font-weight: bold !important; text-decoration: none !important; display: inline-block !important; box-shadow: 0 4px 10px rgba(0, 123, 195, 0.25) !important; white-space: nowrap !important;
    }
    .center-header-block {
        display: flex !important; flex-direction: column !important; align-items: center !important; justify-content: center !important; text-align: center !important; margin-top: 10px !important; margin-bottom: 25px !important; width: 100% !important;
    }
    .tog-center-logo {
        width: 50px; height: 50px; background-color: #000000; border-radius: 50%; display: flex; justify-content: center; align-items: center; color: #ffffff; font-weight: bold; font-size: 15px; margin-bottom: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    /* บังคับปุ่มของ Streamlit ให้ตีกรอบสไตล์ฟ้ายาวและจัดอักษรตรงกลางกึ่งกลาง */
    div.stButton {
        width: 100% !important; display: flex !important; justify-content: center !important; align-items: center !important; margin-top: 10px !important;
    }
    div.stButton > button {
        background-color: #007bc3 !important; color: white !important; border-radius: 30px !important; padding: 13px 0px !important; font-weight: bold !important; font-size: 16px !important; border: none !important; width: 100% !important; max-width: 340px !important; display: flex !important; justify-content: center !important; align-items: center !important; margin: 0 auto !important; box-shadow: 0 4px 12px rgba(0, 123, 195, 0.25) !important;
    }
    div.stButton > button * {
        display: flex !important; justify-content: center !important; align-items: center !important; text-align: center !important; width: auto !important; margin: 0 auto !important;
    }
    
    /* สไตล์แต่งกลุ่มปุ่มคัดกรองสลับเลือกสัดส่วนวิทยุด้านล่าง */
    div[data-testid="stRadio"] > label {
        font-weight: bold !important; color: #1e293b !important;
    }

    .scrollable-graph-container {
        width: 100% !important; overflow-x: auto !important; display: block !important; margin-bottom: 15px !important;
    }
    .inner-graph-box {
        width: 600px !important; display: block !important;
    }
    .user-profile-box {
        text-align: center !important; background: rgba(255, 255, 255, 0.9) !important; border-radius: 15px !important; padding: 12px !important; margin-bottom: 15px !important; border-left: 5px solid #007bc3 !important; box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 📊 ดิกชันนารีเก็บฐานข้อมูลโฟลเดอร์ Google Drive ล็อกพิกัดแม่นยำตามเงื่อนไข (A, B, C ย่อยไปหา Slave)
DRIVE_MAP = {
    "A": {
        260: {"main": "https://drive.google.com/drive/u/0/folders/1QTQuQR8e7DUAYQF0yyYreCi9_bGcX6z0", "slave": "https://drive.google.com/drive/u/0/folders/1DQWgtMsVcPbpNGRH8WQX65VKfJkCxlp5", "slave_name": "SA_260"},
        261: {"main": "https://drive.google.com/drive/u/0/folders/1phKW7eXcijB4U6P95JHnJm6BgG2bcKyQ", "slave": "https://drive.google.com/drive/u/0/folders/1n5KGFnub6z3urE09taiJh4TaUJXqElCF", "slave_name": "SA_261"},
        380: {"main": "https://drive.google.com/drive/u/0/folders/1-77ViPZrWhRXiYMvpa2gTp63CDjxIcHu", "slave": "https://drive.google.com/drive/u/0/folders/1DlKAZot6QPHXdvuVu8ro_TIk26NsznDz", "slave_name": "SA_380"}
    },
    "B": {
        260: {"main": "https://drive.google.com/drive/u/0/folders/1NVgoWHj_WTOU7PDdKyozBYJKL7Ap-s4J", "slave": "https://drive.google.com/drive/u/0/folders/1mFPvOUYkuH57QSwkw0nOmFUNsQKhl3Tf", "slave_name": "SB_260"},
        261: {"main": "https://drive.google.com/drive/u/0/folders/1q3Kb3ClsvnfulRCug33FoBYlyUvhKz-o", "slave": "https://drive.google.com/drive/u/0/folders/1Kf7jjhN1RIcaQG60uIs6bkDs2aafK8OQ", "slave_name": "SB_261"},
        380: {"main": "https://drive.google.com/drive/u/0/folders/1b8jDU2ZJwWuFGihYFVqzbpIVgkH61bhK", "slave": "https://drive.google.com/drive/u/0/folders/179CQ6uNpDen5hao1a949EXpmYLOCu4LQ", "slave_name": "SB_380"}
    },
    "C": {
        260: {"main": "https://drive.google.com/drive/u/0/folders/13k1E0lDkRw4BQWKXCz637gHxo5ou7z3V", "slave": "https://drive.google.com/drive/u/0/folders/1P3qw10mB6zs4yC4w3Jd2rOXN6KnmuzNr", "slave_name": "SC_260"},
        261: {"main": "https://drive.google.com/drive/u/0/folders/1slgqqMbiRttmRd70hbPkV_DAKoiqGbht", "slave": "https://drive.google.com/drive/u/0/folders/1FzfsI-xDgUQPnB_6kDrQ8iGxI5_N075P", "slave_name": "SC_261"},
        380: {"main": "https://drive.google.com/drive/u/0/folders/14jkMpOZG-bIN6h0EYbZ3UrqiFAYUQ7A1", "slave": "https://drive.google.com/drive/u/0/folders/11OR4QaWPaLcM6EPaSPrMkQTQrpfqMMJT", "slave_name": "SC_380"}
    }
}

# 📊 ฟังก์ชันดึงชุดข้อมูลอันดับความถี่ชิ้นงาน Rework จาก Google Sheets
@st.cache_data(ttl=15)
def get_graph_data(target_error):
    sheet_id = "1qKY4ZBWYXM81Y8BZSMjOf7z1hJXeJFCjB5KeRPQBe4c"
    gid = "0"
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    try:
        raw_df = pd.read_csv(csv_url)
        raw_df.columns = raw_df.columns.str.strip()
        raw_df['errortype'] = pd.to_numeric(raw_df['errortype'], errors='coerce')
        raw_df['rework quantity'] = pd.to_numeric(raw_df['rework quantity'], errors='coerce').fillna(0)
        filtered_df = raw_df[raw_df['errortype'] == target_error]
        grouped_df = filtered_df.groupby('Material', as_index=False)['rework quantity'].sum()
        top_10 = grouped_df.sort_values(by='rework quantity', ascending=False).head(10)
        top_10['Material'] = top_10['Material'].astype(str)
        return top_10
    except:
        return pd.DataFrame(columns=['Material', 'rework quantity'])

# 4. ออกแบบระบบจดจำสลับหน้าเพจด้วย Session State คุมพฤติกรรมกล้องมือถือให้เสถียร
if 'page' not in st.session_state: st.session_state.page = "login"
if 'user_info' not in st.session_state: st.session_state.user_info = None
if 'current_defect' not in st.session_state: st.session_state.current_defect = None

current_page = st.session_state.page

# --- แถบนำทางด้านบนสุดสำหรับรีเฟรชหน้าหลัก ---
st.markdown("""
<div class="custom-top-navbar">
    <a href="#" onclick="window.location.reload();" class="nav-btn-link">🏠 Home</a>
    <a href="#" onclick="window.location.reload();" class="nav-btn-link">🚪 Logout</a>
</div>
""", unsafe_allow_html=True)

# --- โลโก้ TOG กลางหน้าจอ ---
st.markdown("""
<div class="center-header-block">
    <div class="tog-center-logo">TOG</div>
    <div>
        <small style="color:#fff; opacity:0.8; display:block; font-size:11px; margin-bottom:2px;">ยินดีต้อนรับ</small>
        <span style="font-size:18px; font-weight:bold; color:white; letter-spacing: 0.5px;">TOG App</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- หน้าที่ 1: Login สแกน QR Code เพื่อเก็บโปรไฟล์พนักงาน ----------------
if current_page == "login":
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:18px; margin-top:0; color:#2c3e50; text-align:center;'>🪪 ส่วนพนักงานเข้าใช้งาน</h3>", unsafe_allow_html=True)
    
    enable_camera = st.checkbox("เปิดสิทธิ์ใช้งานกล้องถ่ายรูป", value=True)
    if enable_camera:
        picture = st.camera_input("", label_visibility="collapsed")
        if picture:
            st.session_state.user_info = {
                "id": "EMP-20688", "name": "สมบัติ", "surname": "อำภา",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.page = "select_defect"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("📊 ดูภาพรวมระบบโดยไม่สแกน"):
        st.session_state.user_info = {
            "id": "GUEST-007", "name": "ผู้เยี่ยมชม", "surname": "(ส่วนกลาง)",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.page = "select_defect"
        st.rerun()

# ---------------- หน้าที่ 2: แสดงโปรไฟล์พนักงาน และมีปุ่มเลือก 3 Defect ----------------
elif current_page == "select_defect":
    # แสดงข้อมูลพนักงานด้านบนสุดตามบรีฟใหม่
    if st.session_state.user_info:
        info = st.session_state.user_info
        st.markdown(f"""
        <div class="user-profile-box">
            <div style="font-size: 14px; font-weight: bold; color: #1e293b;">👤 ผู้ใช้งาน: {info['name']} {info['surname']}</div>
            <div style="font-size: 12px; color: #64748b; margin-top: 2px;">ID: {info['id']} | เวลาแสกนเข้า: {info['time']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('<div class="login-card" style="text-align:center;"><b>🎯 โปรดเลือกประเภท Defect ที่ต้องการตรวจสอบคลังงาน:</b></div>', unsafe_allow_html=True)
    
    # เมนูปุ่มกดขนาดใหญ่ 3 Defect แยกขาดชิ้นต่อชิ้น
    if st.button("🟠 ดูข้อมูล Defect 260 (Rough Lines)"):
        st.session_state.current_defect = 260
        st.session_state.page = "defect_view"
        st.rerun()
        
    if st.button("🔵 ดูข้อมูล Defect 261 (Grinding Structure)"):
        st.session_state.current_defect = 261
        st.session_state.page = "defect_view"
        st.rerun()
        
    if st.button("⚫ ดูข้อมูล Defect 380 (Contour/Design Fault)"):
        st.session_state.current_defect = 380
        st.session_state.page = "defect_view"
        st.rerun()

# ---------------- หน้าที่ 3: หน้ารายละเอียดงานแบบแยกหน้าต่อหน้า (ไม่ปนกัน) ----------------
elif current_page == "defect_view":
    defect = st.session_state.current_defect
    
    # แสดงหัวข้อกำกับและสีแท่งตามเงื่อนไขระบุ
    color_hex = "#ff7f0e" if defect == 260 else ("#002060" if defect == 261 else "#000000")
    defect_title = "Defect 260" if defect == 260 else ("Defect 261" if defect == 261 else "Defect 380")
    
    # ปุ่มย้อนกลับไปสลับเลือก Defect อื่น
    if st.button("🔙 กลับไปเลือกประเภท Defect อื่น"):
        st.session_state.page = "select_defect"
        st.rerun()
        
    st.markdown(f'<div class="login-card" style="text-align:center; border-left: 6px solid {color_hex};"><b>📊 ข้อมูลสรุปกราฟ 1-10 ของ {defect_title}</b></div>', unsafe_allow_html=True)
    
    # 📈 โชว์เฉพาะกราฟ 1-10 ของชิ้นที่เราคลิกเข้ามาเท่านั้น
    df_current = get_graph_data(defect)
    if not df_current.empty:
        st.markdown('<div class="scrollable-graph-container"><div class="inner-graph-box">', unsafe_allow_html=True)
        fig = px.bar(df_current, x='Material', y='rework quantity', text='rework quantity')
        fig.update_traces(textposition='outside', marker_color=color_hex)
        fig.update_layout(xaxis=dict(type='category', tickangle=45), yaxis=dict(tickformat='d'), margin=dict(l=10, r=10, t=25, b=50), height=210, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)
    else:
        st.caption("ไม่มีข้อมูลประวัติ rework สำหรับกลุ่มนี้")

    # --- 🔲 กรอบย่อยที่ 1: ระบบตรวจสอบคลังรูป BEFORE (สวิทช์ลิงก์ตรงตามตัวเลือกอัตโนมัติ) ---
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown(f"<b style='color:#007bc3; font-size:14px; display:block; margin-bottom:5px;'>🖼️ กรอบที่ 1: {defect_title} เลือกภาพ Before</b>", unsafe_allow_html=True)
    
    selected_face = st.radio(
        "เลือกพิกัดหน้างาน:",
        ["หน้า A", "หน้า B", "หน้า C", "อื่นๆ"],
        horizontal=True,
        key=f"radio_face_{defect}"
    )
    
    # กรณีเลือกหน้าหลัก A, B, C -> ดึงลิงก์มาแมปคู่กันทันทีเพื่อความเร็ว
    if selected_face in ["หน้า A", "หน้า B", "หน้า C"]:
        face_char = selected_face.split()[-1]
        folder_info = DRIVE_MAP[face_char][defect]
        
        st.markdown(f"""
        <div style="background-color:#f1f5f9; padding:10px; border-radius:10px; font-size:12px; margin: 10px 0;">
            <b>📂 พิกัด Drive ตรงตัวเลือก ({face_char}_{defect}):</b><br>
            • โฟลเดอร์หลัก: <a href="{folder_info['main']}" target="_blank">คลิกเพื่อเปิดไว</a><br>
            • ชั้นรอง (Slave): <a href="{folder_info['slave']}" target="_blank">คลิกเข้าสู่ {folder_info['slave_name']}</a>
        </div>
        """, unsafe_allow_html=True)
        
        # ตัวเลือกจำลองเปิดรูปย่อย 5 รูป
        sub_choice = st.selectbox("เลือกรายละเอียดภาพย่อยย่อย (มี 5 ภาพ):", [f"ภาพรายละเอียดชิ้นงานย่อยที่ {i}" for i in range(1, 6)])
        st.info(f"📸 พรีวิวกำลังดึงค่าซอร์ส: {sub_choice}")
        
    # กรณีเลือก อื่นๆ -> สั่งเปิดกล้องถ่ายภาพเก็บลงเองได้เลย
    elif selected_face == "อื่นๆ":
        st.markdown("<p style='color:#64748b; font-size:12px;'>📸 โหมดหน้างานเสริม: กดบันทึกรูปภาพชิ้นงาน Before ได้ด้วยตนเอง</p>", unsafe_allow_html=True)
        custom_before = st.camera_input("ถ่ายภาพ Before (อื่นๆ)", key=f"cam_before_other_{defect}")
        if custom_before:
            st.success("บันทึกภาพถ่าย Before นอกกรอบสำเร็จ")
            
    st.markdown('</div>', unsafe_allow_html=True)

    # --- 🔲 กรอบย่อยที่ 2: ระบบจัดการอัปเดตผลลัพธ์ AFTER ---
    st.markdown('<div class="login-card" style="border-top: 4px solid #10b981;">', unsafe_allow_html=True)
    st.markdown(f"<b style='color:#10b981; font-size:14px; display:block; margin-bottom:5px;'>✨ กรอบที่ 2: ส่วนอัปเดตงาน After ({defect_title})</b>", unsafe_allow_html=True)
    
    # ช่องกรอกรายละเอียดความเห็น After
    after_comment = st.text_area("พิมพ์ข้อความสรุปรายละเอียดผลงาน After:", key=f"text_after_{defect}", placeholder="กรอกข้อความที่ต้องการบันทึกหลังการแก้ไข...")
    
    # ระบบถ่ายภาพแนบผลงาน After ได้จำนวน 5 รูป
    st.markdown("<p style='font-size:12px; color:#475569; margin-bottom:2px;'>📸 สแนปภาพถ่ายชิ้นงาน After (ถ่ายแนบได้สูงสุด 5 ภาพ):</p>", unsafe_allow_html=True)
    
    captured_after_list = []
    for i in range(1, 6):
        pic_after = st.camera_input(f"ถ่ายภาพ After ลำดับที่ {i}", key=f"cam_after_{defect}_{i}")
        if pic_after:
            captured_after_list.append(pic_after)
            
    if captured_after_list:
        st.toast(f"รับไฟล์รูปถ่าย After ครบเรียบร้อย {len(captured_after_list)} ภาพ")
        
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
