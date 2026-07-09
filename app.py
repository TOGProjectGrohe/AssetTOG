import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. ตั้งค่าหน้าเว็บพื้นฐานให้กระชับเข้ามุมมองสไตล์สมาร์ทโฟน
st.set_page_config(page_title="TOG App", layout="centered", initial_sidebar_state="collapsed")

# 2. 🛠️ ชุดคำสั่ง CSS จัดโครงสร้างแผงหน้าจอมือถือส้มพาสเทล ปุ่มลิงก์ทางด่วน และบล็อกย่อยให้สมดุล
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
    
    /* เคลียร์ระยะห่างบล็อกหลัก */
    [data-testid="stMainBlockContainer"], [data-testid="stVerticalBlock"], [data-testid="stVerticalBlockRoot"], div[data-testid="element-container"], .stColumn {
        width: 100% !important; max-width: 100% !important; background-color: transparent !important; border: none !important; box-shadow: none !important; padding: 0px !important; margin: 0px !important;
    }

    /* กล่องพื้นหลังขาวสำหรับ Content */
    .login-card {
        background-color: white !important; border-radius: 20px !important; padding: 15px !important; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important; margin-bottom: 15px !important; width: 100% !important;
    }

    /* แถบนำทางปุ่มกด Home / Logout ฟิกซ์ล็อกชิดขอบบนสุดขนานสองฝั่ง */
    .custom-top-navbar {
        position: absolute !important; 
        top: 20px !important; 
        left: 20px !important; 
        right: 20px !important; 
        display: flex !important; 
        justify-content: space-between !important; 
        align-items: center !important; 
        z-index: 999999 !important;
    }
    
    .nav-btn-link {
        background-color: #007bc3 !important; 
        color: white !important; 
        border-radius: 20px !important; 
        padding: 8px 16px !important; 
        font-size: 13px !important; 
        font-weight: bold !important; 
        text-decoration: none !important;
        box-shadow: 0 4px 10px rgba(0, 123, 195, 0.25) !important;
        white-space: nowrap !important;
    }

    /* จัดบล็อกโลโก้ TOG และข้อความต้อนรับให้อยู่ตรงกึ่งกลางหน้าจอแบบ 100% */
    .center-header-block {
        display: flex !important; flex-direction: column !important; align-items: center !important; justify-content: center !important; text-align: center !important; margin-top: 10px !important; margin-bottom: 25px !important; width: 100% !important;
    }
    .tog-center-logo {
        width: 50px; height: 50px; background-color: #000000; border-radius: 50%; display: flex; justify-content: center; align-items: center; color: #ffffff; font-weight: bold; font-size: 15px; margin-bottom: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    /* เจาะลึกช่องกรอกข้อความ TextInput ให้เนื้อหาอยู่เซ็นเตอร์ */
    div[data-testid="stTextInput"] input {
        text-align: center !important;
        font-size: 18px !important;
        font-weight: bold !important;
        color: #1e293b !important;
        border-radius: 15px !important;
        border: 2px solid #cbd5e1 !important;
    }
    
    /* บังคับปุ่มทั่วไปให้ตีกรอบยาวสีฟ้า */
    div.stButton {
        width: 100% !important; display: flex !important; justify-content: center !important; align-items: center !important; margin-top: 15px !important;
    }
    div.stButton > button {
        background-color: #007bc3 !important; color: white !important; border-radius: 30px !important; padding: 13px 0px !important; font-weight: bold !important; font-size: 15px !important; border: none !important; width: 100% !important; max-width: 340px !important; display: flex !important; justify-content: center !important; align-items: center !important; margin: 0 auto !important; box-shadow: 0 4px 12px rgba(0, 123, 195, 0.25) !important;
    }
    
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
    
    /* สไตล์คุมกล่องบล็อกย่อยรูปภาพ */
    .sub-image-block {
        border: 1px solid #cbd5e1 !important; 
        background-color: #f8fafc !important; 
        border-radius: 15px !important; 
        padding: 12px !important; 
        margin-top: 10px !important; 
        margin-bottom: 5px !important; 
        text-align: center !important;
    }
    .main-image-block {
        border: 2px solid #007bc3 !important; 
        background-color: #f0f9ff !important; 
        border-radius: 15px !important; 
        padding: 14px !important; 
        margin-top: 10px !important; 
        margin-bottom: 15px !important; 
        text-align: center !important;
    }
    .drive-picker-btn {
        display: block !important;
        background-color: #007bc3 !important;
        color: white !important;
        text-align: center !important;
        padding: 10px 12px !important;
        border-radius: 10px !important;
        font-size: 13px !important;
        font-weight: bold !important;
        text-decoration: none !important;
        margin-top: 5px !important;
        box-shadow: 0 4px 10px rgba(0, 123, 195, 0.2) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 🌐 ฟังก์ชันดึงข้อมูลรายชื่อพนักงาน
def get_employee_from_sheet(input_id):
    sheet_id = "1sRher870S-P1w_kUVfryy-OqM67WjGpwek9y9wm29Ps"
    gid = "0"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        if 'ID' in df.columns:
            df['ID'] = df['ID'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
            target_id = str(input_id).strip().replace('.0', '')
            match = df[df['ID'] == target_id]
            if not match.empty:
                row = match.iloc[0]
                return {
                    "status": "success", "found": True, "id": str(row['ID']),
                    "name": str(row['Name']).strip(), "position": str(row['Position']).strip() if 'Position' in df.columns else "พนักงาน"
                }
            return {"status": "success", "found": False, "id": target_id}
    except Exception as e:
        return {"status": "error", "error_msg": str(e), "id": str(input_id)}
    return {"status": "success", "found": False, "id": str(input_id)}

# 🔗 🔗 🔗 ฐานข้อมูลคลังลิงก์โฟลเดอร์ Google Drive (อัปเดตชุดใหม่แยกกลุ่มหลัก-กลุ่มย่อย 5 ภาพ ตามที่คุณส่งมาล่าสุด)
DRIVE_MAP = {
    "A": {
        260: {
            "main_url": "https://drive.google.com/drive/folders/1QTQuQR8e7DUAYQF0yyYreCi9_bGcX6z0", "main_name": "A_260",
            "slave_url": "https://drive.google.com/drive/folders/1QTQuQR8e7DUAYQF0yyYreCi9_bGcX6z0", "slave_name": "SA_260"
        },
        261: {
            "main_url": "https://drive.google.com/drive/folders/1phKW7eXcijB4U6P95JHnJm6BgG2bcKyQ", "main_name": "A_261",
            "slave_url": "https://drive.google.com/drive/folders/1n5KGFnub6z3urE09taiJh4TaUJXqElCF", "slave_name": "SA_261"
        },
        380: {
            "main_url": "https://drive.google.com/drive/folders/1-77ViPZrWhRXiYMvpa2gTp63CDjxIcHu", "main_name": "A_380",
            "slave_url": "https://drive.google.com/drive/folders/1DlKAZot6QPHXdvuVu8ro_TIk26NsznDz", "slave_name": "SA_380"
        }
    },
    "B": {
        260: {
            "main_url": "https://drive.google.com/drive/folders/1NVgoWHj_WTOU7PDdKyozBYJKL7Ap-s4J", "main_name": "B_260",
            "slave_url": "https://drive.google.com/drive/folders/1mFPvOUYkuH57QSwkw0nOmFUNsQKhl3Tf", "slave_name": "SB_260"
        },
        261: {
            "main_url": "https://drive.google.com/drive/folders/1q3Kb3ClsvnfulRCug33FoBYlyUvhKz-o", "main_name": "B_261",
            "slave_url": "https://drive.google.com/drive/folders/1Kf7jjhN1RIcaQG60uIs6bkDs2aafK8OQ", "slave_name": "SB_261"
        },
        380: {
            "main_url": "https://drive.google.com/drive/folders/1b8jDU2ZJwWuFGihYFVqzbpIVgkH61bhK", "main_name": "B_380",
            "slave_url": "https://drive.google.com/drive/folders/179CQ6uNpDen5hao1a949EXpmYLOCu4LQ", "slave_name": "SB_380"
        }
    },
    "C": {
        260: {
            "main_url": "https://drive.google.com/drive/folders/13k1E0lDkRw4BQWKXCz637gHxo5ou7z3V", "main_name": "C_260",
            "slave_url": "https://drive.google.com/drive/folders/1P3qw10mB6zs4yC4w3Jd2rOXN6KnmuzNr", "slave_name": "SC_260"
        },
        261: {
            "main_url": "https://drive.google.com/drive/folders/1slgqqMbiRttmRd70hbPkV_DAKoiqGbht", "main_name": "C_261",
            "slave_url": "https://drive.google.com/drive/folders/1FzfsI-xDgUQPnB_6kDrQ8iGxI5_N075P", "slave_name": "SC_261"
        },
        380: {
            "main_url": "https://drive.google.com/drive/folders/14jkMpOZG-bIN6h0EYbZ3UrqiFAYUQ7A1", "main_name": "C_380",
            "slave_url": "https://drive.google.com/drive/folders/11OR4QaWPaLcM6EPaSPrMkQTQrpfqMMJT", "slave_name": "SC_380"
        }
    }
}

# 📊 ฟังก์ชันดึงชุดข้อมูลกราฟหลัก
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

if 'page' not in st.session_state: st.session_state.page = "login"
if 'user_info' not in st.session_state: st.session_state.user_info = None
if 'current_defect' not in st.session_state: st.session_state.current_defect = None

current_page = st.session_state.page

# --- แถบนำทางด้านบนสุด ---
st.markdown("""
<div class="custom-top-navbar">
    <a href="?nav=reset" target="_self" class="nav-btn-link">🏠 Home</a>
    <a href="?nav=reset" target="_self" class="nav-btn-link">🚪 Logout</a>
</div>
""", unsafe_allow_html=True)

if st.query_params.get("nav") == "reset":
    st.session_state.page = "login"
    st.session_state.user_info = None
    st.session_state.current_defect = None
    st.query_params.clear()
    st.rerun()

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

# ---------------- หน้าแรก: Login ----------------
if current_page == "login":
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='font-size:16px; margin-top:0; color:#2c3e50; text-align:center;'>🪪 ป้อนรหัสพนักงานเพื่อเข้าระบบ</h4>", unsafe_allow_html=True)
    input_id = st.text_input("กรอกรหัส ID พนักงานของคุณ:", value="", placeholder="พิมพ์ตัวเลขรหัส เช่น 20, 198, 222", label_visibility="collapsed")
    
    if input_id.strip() != "":
        result = get_employee_from_sheet(input_id)
        if result["status"] == "success" and result.get("found"):
            st.markdown(f"""
            <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 15px; border-radius: 15px; margin-top: 15px; text-align: center;">
                <span style="color: #16a34a; font-weight: bold; font-size: 15px;">✅ ตรวจพบข้อมูลพนักงานถูกต้อง:</span><br>
                <div style="font-size: 14px; margin-top: 5px; color: #1e293b; text-align: left; padding-left: 10px;">
                    • <b>ชื่อพนักงาน:</b> {result['name']}<br>
                    • <b>รหัสพนักงาน (ID):</b> {result['id']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔓 ยืนยันข้อมูลถูกต้อง กดเพื่อเข้าระบบ", key="btn_confirm_login"):
                st.session_state.user_info = {"id": result["id"], "name": result["name"], "position": result["position"], "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
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

# ---------------- หน้าสาม: แสดงกราฟ และระบบเลือกภาพใหญ่พ่วง 5 ภาพย่อย ----------------
elif current_page == "defect_view":
    defect = st.session_state.current_defect
    color_hex = "#ff7f0e" if defect == 260 else ("#002060" if defect == 261 else "#000000")
    defect_title = "Defect 260" if defect == 260 else ("Defect 261" if defect == 261 else "Defect 380")
    
    if st.button("🔙 กลับไปเลือกประเภท Defect อื่น", key="btn_back_select"):
        st.session_state.page = "select_defect"; st.rerun()
        
    st.markdown(f'<div class="login-card" style="text-align:center; border-left: 6px solid {color_hex};"><b>📊 สรุปข้อมูลของ {defect_title}</b></div>', unsafe_allow_html=True)
    
    df_current = get_graph_data(defect)
    selected_material_from_chart = ""
    
    if not df_current.empty:
        st.markdown('<div class="scrollable-graph-container"><div class="inner-graph-box">', unsafe_allow_html=True)
        fig = px.bar(df_current, x='Material', y='rework quantity', text='rework quantity')
        fig.update_traces(textposition='outside', marker_color=color_hex)
        fig.update_layout(xaxis=dict(type='category', tickangle=45), yaxis=dict(tickformat='d'), margin=dict(l=10, r=10, t=25, b=50), height=200, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', clickmode='event+select')
        chart_data = st.plotly_chart(fig, use_container_width=True, on_select="rerun")
        st.markdown('</div></div>', unsafe_allow_html=True)
        
        if chart_data and "selection" in chart_data and "points" in chart_data["selection"]:
            points = chart_data["selection"]["points"]
            if len(points) > 0: selected_material_from_chart = points[0].get("x", "")

    # 🔲 กรอบย่อยที่ 1: คลังรูปภาพ BEFORE (ระบบเพิ่มกล่องภาพใหญ่คู่ 5 ภาพย่อยแยกขาดกันชัดเจน)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown(f"<b style='color:#007bc3; font-size:14px; display:block; margin-bottom:5px;'>🖼️ กรอบที่ 1: {defect_title} ส่วนเลือกภาพ Before</b>", unsafe_allow_html=True)
    
    if selected_material_from_chart:
        st.success(f"🎯 ล็อกรหัสชิ้นงาน Material: **{selected_material_from_chart}**")

    # ขั้นตอนที่ 1: ให้พนักงานระบุหัวข้อพิกัดหน้างาน
    selected_face = st.radio("เลือกพิกัดหน้างาน:", ["หน้า A", "หน้า B", "หน้า C", "อื่นๆ"], horizontal=True, key=f"rf_{defect}")
    
    if selected_face in ["หน้า A", "หน้า B", "หน้า C"]:
        face_char = selected_face.split()[-1]
        folder_info = DRIVE_MAP[face_char][defect]
        
        st.markdown("<p style='font-size:13px; font-weight:bold; color:#1e293b; margin-top:10px; margin-bottom:2px;'>🎯 ขั้นตอนที่ 1: เลือกภาพใหญ่ชิ้นงานต้นทาง (Main)</p>", unsafe_allow_html=True)
        
        # 🟢 1. บล็อกเพิ่มรูปภาพใหญ่ (คลังต้นทาง เช่น A_260, B_380)
        st.markdown(f"""
        <div class="main-image-block">
            <span style="font-size:13px; font-weight:bold; color:#005aab; display:block; margin-bottom:4px;">🖼️ เลือกรูปภาพชิ้นงานใหญ่ ({folder_info['main_name']})</span>
            <a href="{folder_info['main_url']}" target="_blank" class="drive-picker-btn" style="background-color:#005aab;">
                📂 เปิดคลังภาพใหญ่ใน Google Drive
            </a>
        </div>
        """, unsafe_allow_html=True)
        uploaded_main = st.file_uploader(f"แนบภาพใหญ่ {folder_info['main_name']}", type=["png", "jpg", "jpeg"], key=f"uf_main_{defect}", label_visibility="collapsed")
        if uploaded_main is not None:
            st.image(uploaded_main, use_container_width=True, caption=f"✅ แนบภาพใหญ่ {folder_info['main_name']} สำเร็จ")

        st.markdown("<hr style='margin: 15px 0; border: 0; border-top: 2px dashed #cbd5e1;'>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:13px; font-weight:bold; color:#1e293b; margin-bottom:2px;'>📥 ขั้นตอนที่ 2: เลือกภาพรายละเอียดจุดย่อย 5 ภาพ (Slave)</p>", unsafe_allow_html=True)
        
        # 🔵 2. แผงกางบล็อกเพิ่มรูปภาพย่อย 5 บล็อกอิสระแยกจากกัน (คลังย่อย เช่น SA_260, SB_380)
        for i in range(1, 6):
            st.markdown(f"""
            <div class="sub-image-block">
                <span style="font-size:13px; font-weight:bold; color:#007bc3; display:block; margin-bottom:4px;">📸 เพิ่มรูปรายละเอียดย่อยจุดที่ {i} ({folder_info['slave_name']})</span>
                <a href="{folder_info['slave_url']}" target="_blank" class="drive-picker-btn">
                    📎 เปิดเลือกไฟล์รูปภาพจาก Folder {folder_info['slave_name']}
                </a>
            </div>
            """, unsafe_allow_html=True)
            
            uploaded_preview = st.file_uploader(f"แนบภาพย่อยจุดที่ {i}", type=["png", "jpg", "jpeg"], key=f"uf_bef_{defect}_{i}", label_visibility="collapsed")
            if uploaded_preview is not None:
                st.image(uploaded_preview, use_container_width=True)
            else:
                st.caption(f"ช่องจุดที่ {i} ว่างอยู่ (กดเปิดลิงก์ด้านบนเพื่อหาภาพ)")
            st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)

    elif selected_face == "อื่นๆ":
        st.markdown("<p style='color:#64748b; font-size:12px;'>📸 โหมดหน้างานเสริม: กดบันทึกรูปภาพชิ้นงาน Before ได้ด้วยตนเอง</p>", unsafe_allow_html=True)
        st.camera_input("ถ่ายภาพ Before (กำหนดเอง)", key=f"c_bef_{defect}")
    st.markdown('</div>', unsafe_allow_html=True)

    # 🔲 กรอบย่อยที่ 2: ส่วนอัปเดตงาน AFTER
    st.markdown('<div class="login-card" style="border-top: 4px solid #10b981;">', unsafe_allow_html=True)
    st.markdown(f"<b style='color:#10b981; font-size:14px; display:block; margin-bottom:5px;'>✨ กรอบที่ 2: ส่วนอัปเดตงาน After ({defect_title})</b>", unsafe_allow_html=True)
    default_text = f"รายงานผลชิ้นงาน Material รหัส: {selected_material_from_chart}\n" if selected_material_from_chart else ""
    st.text_area("พิมพ์ข้อความสรุปรายละเอียดผลงาน After:", value=default_text, key=f"ta_af_{defect}")
    for i in range(1, 3):
        st.camera_input(f"ถ่ายภาพ After ลำดับที่ {i}", key=f"c_af_{defect}_{i}")
    st.markdown('</div>', unsafe_allow_html=True)
