import streamlit as st
import pandas as pd
import requests
import json
import base64
import plotly.express as px
import plotly.graph_objects as go
import threading
from datetime import datetime

# 🔐 [กลไกจัดคิวอัจฉริยะ] ฟังก์ชันสร้างระบบกุญแจล็อกคิวสำหรับผู้ใช้หลายคนผ่าน cache_resource ของ Streamlit จริง
@st.cache_resource
def get_global_app_lock():
    return threading.Lock()

app_lock = get_global_app_lock()

# ⚠️ ลิงก์ Google Apps Script ตัวจริงของคุณวีรพันธ์
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz6phYpdneqbZ45maoAX4lPxWlEeaZhBO_D1QICqkogRdyTt3dRcI_mLx-MxuZ5pPB3xQ/exec"

# 1. ตั้งค่าหน้าเว็บสไตล์สมาร์ทโฟน
st.set_page_config(page_title="TOG App", layout="centered", initial_sidebar_state="collapsed")

# 2. 🎨 CSS ตกแต่งหน้าจอโทรศัพท์และปุ่มลบรูปสีแดงพรีเมียม
st.markdown("""
    <style>
    .stDeployButton, [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], header, footer, #MainMenu {
        display: none !important; visibility: hidden !important; height: 0 !important;
    }
    [data-testid="stStatusWidget"], #stConnectionStatus, div[class*="viewerBadge"] {
        display: none !important; visibility: hidden !important; height: 0 !important;
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
    .future-graph-card {
        background-color: rgba(0,0,0,0) !important; border: none !important; padding: 5px !important; margin-bottom: 15px !important; width: 100% !important;
    }
    .custom-top-navbar {
        position: absolute !important; top: 20px !important; left: 20px !important; right: 20px !important; display: flex !important; justify-content: space-between !important; align-items: center !important; z-index: 999999 !important;
    }
    
    .nav-btn-link {
        background-color: #bae6fd !important; 
        color: #000000 !important; 
        border: 1px solid rgba(0,0,0,0.05) !important;
        border-radius: 20px !important; 
        padding: 8px 16px !important; 
        font-size: 13px !important; 
        font-weight: bold !important; 
        text-decoration: none !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
    }
    .nav-btn-link:hover {
        background-color: #7dd3fc !important;
    }

    .tog-logo-circle {
        width: 50px !important; 
        height: 50px !important; 
        background-color: rgba(0, 0, 0, 0.2) !important; 
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        border-radius: 50% !important; 
        display: flex !important; 
        justify-content: center !important; 
        align-items: center !important; 
        color: #000000 !important; 
        font-weight: bold !important; 
        font-size: 15px !important; 
        margin: 0 auto 8px auto !important;
    }

    .center-header-block {
        display: flex !important; flex-direction: column !important; align-items: center !important; justify-content: center !important; text-align: center !important; margin-top: 10px !important; margin-bottom: 25px !important; width: 100% !important;
    }
    .drive-link-button {
        display: block !important; text-align: center !important; background-color: #10b981 !important; color: white !important;
        font-weight: bold !important; padding: 12px 20px !important; border-radius: 12px !important; text-decoration: none !important;
        margin: 12px 0 !important; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25) !important; font-size: 14px !important;
    }

    /* 📊 กรอบ Employee Details */
    .employee-details-container {
        border: 2px solid #3b82f6 !important;
        border-radius: 8px !important;
        margin-top: 15px !important;
        margin-bottom: 15px !important;
        overflow: hidden !important;
        background-color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    }
    .employee-details-header {
        background-color: #aec6cf !important;
        color: #000000 !important;
        font-weight: bold !important;
        text-align: center !important;
        padding: 8px !important;
        font-size: 14px !important;
        border-bottom: 2px solid #3b82f6 !important;
        letter-spacing: 0.5px;
    }
    .employee-details-sub-grid {
        display: grid !important;
        grid-template-columns: 1fr 1fr 1fr 1fr !important;
        text-align: center !important;
        background-color: #ffffff !important;
        font-size: 12px !important;
        font-weight: bold !important;
        border-bottom: 1px solid #e2e8f0 !important;
        padding: 6px 0 !important;
    }
    .employee-details-row-data {
        display: grid !important;
        grid-template-columns: 1fr 1fr 1fr 1fr !important;
        text-align: center !important;
        font-size: 11px !important;
        padding: 8px 0 !important;
        background-color: #f8fafc !important;
        color: #334155 !important;
    }

    div.stButton > button {
        background-color: rgba(186, 230, 253, 0.5) !important; 
        backdrop-filter: blur(6px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 14px !important;
        border: 2px solid rgba(255, 255, 255, 0.7) !important; 
        border-radius: 16px !important;
        width: 100% !important; 
        padding: 12px 20px !important;
        margin-bottom: 12px !important;
        display: block !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02), inset 0 1px 2px rgba(255,255,255,0.3) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        background-color: rgba(125, 211, 252, 0.7) !important;
        border: 2px solid rgba(255, 255, 255, 0.9) !important;
    }
    
    div.stButton > button[key^="save_btn_"] {
        background-color: #10b981 !important;
        color: white !important;
        font-size: 16px !important;
        border: 2px solid #059669 !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
    }

    /* 🎨 [ปุ่มลบรูปภาพสีแดงเด่นชัด] */
    div.stButton > button[key="clear_image_btn"] {
        background-color: #ef4444 !important;
        color: white !important;
        border: 1px solid #dc2626 !important;
        padding: 8px 15px !important;
        font-size: 13px !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 6px rgba(239, 68, 68, 0.2) !important;
    }
    div.stButton > button[key="clear_image_btn"]:hover {
        background-color: #dc2626 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🌐 ฟังก์ชันดึงข้อมูลพนักงาน
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
                pos_val = str(row['Position']).strip() if 'Position' in df.columns else "GL"
                return {"status": "success", "found": True, "id": str(row['ID']), "name": str(row['Name']).strip(), "position": pos_val}
    except:
        pass
    return {"status": "success", "found": False}

# 📊 ฟังก์ชันดึงข้อมูลดิบสถิติหลัก
@st.cache_data(ttl=60)
def load_real_defect_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/1qKY4ZBWYXM81Y8BZSMjOf7z1hJXeJFCjB5KeRPQBe4c/export?format=csv&gid=0"
    try:
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

# ฟังก์ชันแสดงผลส่วน Employee Details ด้านล่างแบบเรียลไทม์
def render_employee_details_footer():
    if 'user_info' in st.session_state and st.session_state.user_info:
        now_time_view = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        emp_id_val = str(st.session_state.user_info.get('id', '-'))
        emp_name_val = str(st.session_state.user_info.get('name', '-'))
        emp_position_val = str(st.session_state.user_info.get('position', 'GL'))
        if emp_position_val in ["", "None", "-", "nan"]:
            emp_position_val = "GL"

        st.markdown(f"""
            <div class="employee-details-container">
                <div class="employee-details-header">Employee Details</div>
                <div class="employee-details-sub-grid">
                    <div>Timestamp</div>
                    <div>Employee ID</div>
                    <div>Name</div>
                    <div>Position</div>
                </div>
                <div class="employee-details-row-data">
                    <div>{now_time_view}</div>
                    <div>{emp_id_val}</div>
                    <div>{emp_name_val}</div>
                    <div>{emp_position_val}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

FOLDER_LINK_MAP = {
    "A": {
        260: {"main_url": "https://drive.google.com/drive/folders/1QTQuQR8e7DUAYQF0yyYreCi9_bGcX6z0", "main_title": "A_260", "slave_url": "https://drive.google.com/drive/folders/1DQWgtMsVcPbpNGRH8WQX65VKfJkCxlp5", "slave_title": "SA_260"},
        261: {"main_url": "https://drive.google.com/drive/folders/1phKW7eXcijB4U6P95JHnJm6BgG2bcKyQ", "main_title": "A_261", "slave_url": "https://drive.google.com/drive/folders/1n5KGFnub6z3urE09taiJh4TaUJXqElCF", "slave_title": "SA_261"},
        380: {"main_url": "https://drive.google.com/drive/folders/1-77ViPZrWhRXiYMvpa2gTp63CDjxIcHu", "main_title": "A_380", "slave_url": "https://drive.google.com/drive/folders/1DlKAZot6QPHXdvuVu8ro_TIk26NsznDz", "slave_title": "SA_380"}
    },
    "B": {
        260: {"main_url": "https://drive.google.com/drive/folders/1NVgoWHj_WTOU7PDdKyozBYJKL7Ap-s4J", "main_title": "B_260", "slave_url": "https://drive.google.com/drive/folders/1mFPvOUYkuH57QSwkw0nOmFUNsQKhl3Tf", "slave_title": "SB_260"},
        261: {"main_url": "https://drive.google.com/drive/folders/1q3Kb3ClsvnfulRCug33FoBYlyUvhKz-o", "main_title": "B_261", "slave_url": "https://drive.google.com/drive/folders/1Kf7jjhN1RIcaQG60uIs6bkDs2aafK8OQ", "slave_title": "SB_261"},
        380: {"main_url": "https://drive.google.com/drive/folders/1b8jDU2ZJwWuFGihYFVqzbpIVgkH61bhK", "main_title": "B_380", "slave_url": "https://drive.google.com/drive/folders/179CQ6uNpDen5hao1a949EXpmYLOCu4LQ", "slave_title": "SB_380"}
    },
    "C": {
        260: {"main_url": "https://drive.google.com/drive/folders/13k1E0lDkRw4BQWKXCz637gHxo5ou7z3V", "main_title": "C_260", "slave_url": "https://drive.google.com/drive/folders/1P3qw10mB6zs4yC4w3Jd2rOXN6KnmuzNr", "slave_title": "SC_260"},
        261: {"main_url": "https://drive.google.com/drive/folders/1slgqqMbiRttmRd70hbPkV_DAKoiqGbht", "main_title": "C_261", "slave_url": "https://drive.google.com/drive/folders/1FzfsI-xDgUQPnB_6kDrQ8iGxI5_N075P", "slate_title": "SC_261"},
        380: {"main_url": "https://drive.google.com/drive/folders/14jkMpOZG-bIN6h0EYbZ3UrqiFAYUQ7A1", "main_title": "C_380", "slave_url": "https://drive.google.com/drive/folders/11OR4QaWPaLcM6EPaSPrMkQTQrpfqMMJT", "slate_title": "SC_380"}
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

st.markdown('<div class="center-header-block"><div class="tog-logo-circle">TOG</div><span style="font-size:18px; font-weight:bold; color:black;">TOG App</span></div>', unsafe_allow_html=True)

# ---------------- หน้าแรก: Login ----------------
if current_page == "login":
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='font-size:16px; margin-top:0; color:#2c3e50; text-align:center;'>🪪 ป้อนรหัสพนักงานเพื่อเข้าระบบ</h4>", unsafe_allow_html=True)
    input_id = st.text_input("กรอกรหัส ID พนักงานของคุณ:", value="", placeholder="พิมพ์ตัวเลขรหัส เช่น 20", label_visibility="collapsed")
    if input_id.strip() != "":
        result = get_employee_from_sheet(input_id)
        if result["status"] == "success" and result.get("found"):
            now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.user_info = {
                "id": result["id"], "name": result["name"], 
                "position": result["position"] if result["position"] else "GL", "timestamp": now_time
            }
            if st.button("🔓 กดเพื่อเข้าระบบ"):
                st.session_state.page = "select_defect"; st.rerun()
        else:
            st.markdown('<div class="error-pastel-box">❌ ไม่พบข้อมูล โปรดคีย์ ID อีกครั้ง</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- หน้าสอง: คัดเลือก Defect ----------------
elif current_page == "select_defect":
    st.markdown('<div class="login-card" style="text-align:center;"><b>🎯 โปรดเลือกประเภท Defect</b></div>', unsafe_allow_html=True)
    if st.button("🟠 ดูข้อมูล Defect 260 (Rough Lines)"):
        st.session_state.current_defect = 260; st.session_state.page = "defect_view"; st.rerun()
    if st.button("🔵 ดูข้อมูล Defect 261 (Grinding Structure)"):
        st.session_state.current_defect = 261; st.session_state.page = "defect_view"; st.rerun()
    if st.button("⚫ ดูข้อมูล Defect 380 (Contour/Design Fault)"):
        st.session_state.current_defect = 380; st.session_state.page = "defect_view"; st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    render_employee_details_footer()

# ---------------- หน้าสาม: บอร์ดสถิติและการอัปเดต After ----------------
elif current_page == "defect_view":
    defect = st.session_state.current_defect
    defect_title = f"Defect {defect}"

    if st.button("🔙 กลับไปเลือกประเภท Defect อื่น"):
        st.session_state.page = "select_defect"; st.rerun()

    st.markdown(f'<div class="login-card" style="text-align:center; color:#000000; font-weight:bold;"><b>📊 แผนภูมิ Defect {defect}</b></div>', unsafe_allow_html=True)

    # 📥 โหลดข้อมูล Material จริง
    raw_df = load_real_defect_data()
    qty_col = "rework quantity"
    filtered_df = pd.DataFrame()
    chart_data = pd.DataFrame()

    if not raw_df.empty and 'errortype' in raw_df.columns and 'Material' in raw_df.columns:
        raw_df['errortype'] = pd.to_numeric(raw_df['errortype'], errors='coerce')
        raw_df['Material'] = raw_df['Material'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
        filtered_df = raw_df[raw_df['errortype'] == defect]
        qty_col = 'rework quantity' if 'rework quantity' in raw_df.columns else raw_df.columns[-1]
        if not filtered_df.empty:
            filtered_df[qty_col] = pd.to_numeric(filtered_df[qty_col], errors='coerce').fillna(0)
            summary_df = filtered_df.groupby('Material', as_index=False)[qty_col].sum()
            chart_data = summary_df.sort_values(by=qty_col, ascending=False).head(10)
    
    if chart_data.empty:
        chart_data = pd.DataFrame({
            "Material": ["407787135", "407652035", "418706035", "400513035", "418230035", "400451135", "417207135", "408487035", "408242036", "400596035"],
            "rework quantity": [4500, 1300, 1100, 1000, 1000, 850, 850, 750, 750, 650]
        })
        qty_col = "rework quantity"
        filtered_df = chart_data.copy()

    # 📊 แผงกราฟสถิติ
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown(f"<b style='color:#1e293b; font-size:14px; display:block; text-align:center;'>🍕 รายงาน 10 อันดับ Defect {defect} ที่พบ</b>", unsafe_allow_html=True)

    if not chart_data.empty:
        pastel_palette = px.colors.qualitative.Pastel
        list_of_materials = chart_data['Material'].tolist()
        color_map = {mat: pastel_palette[idx % len(pastel_palette)] for idx, mat in enumerate(list_of_materials)}

        state_key = f"sel_mat_{defect}"
        if state_key not in st.session_state or st.session_state[state_key] not in list_of_materials:
            st.session_state[state_key] = list_of_materials[0]

        # 🍕 1. แผนภูมิวงกลม (Pie Chart)
        fig_pie = go.Figure(data=[go.Pie(
            labels=chart_data["Material"], 
            values=chart_data[qty_col], 
            hole=0.45,
            marker=dict(colors=[color_map[m] for m in chart_data["Material"]], line=dict(color='#ffffff', width=2)),
            textinfo='percent', textfont=dict(size=11, color='#000000', weight='bold')
        )])
        fig_pie.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=200, showlegend=False, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)

        # 📊 2. แผนภูมิแท่งแนวตั้ง (Bar Chart)
        bars_list = []
        for mat in list_of_materials:
            val = chart_data[chart_data['Material'] == mat][qty_col].values[0]
            bars_list.append(go.Bar(x=[mat], y=[val], name=mat, marker=dict(color=color_map[mat], line=dict(color='#ffffff', width=2))))
        fig_bar = go.Figure(data=bars_list)
        fig_bar.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=230, showlegend=False, xaxis=dict(type='category', tickangle=45), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        
        selected_bar = st.plotly_chart(fig_bar, use_container_width=True, on_select="rerun")
        if selected_bar and "selection" in selected_bar and selected_bar["selection"]["points"]:
            clicked_mat = selected_bar["selection"]["points"][0]["x"]
            if clicked_mat != st.session_state[state_key]:
                st.session_state[state_key] = clicked_mat

        selected_material = st.session_state[state_key]

        st.markdown("<hr style='margin:10px 0; border:0; border-top:1px dashed #ccc;'>", unsafe_allow_html=True)
        st.markdown(f'<div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 10px; border-radius: 12px; text-align: center; font-size:14px; color:#16a34a;"><b>🔍 TARGET MATERIAL SELECTED:</b> <span style="font-size:16px; font-weight:bold; color:#007bc3;">{selected_material}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 🔘 ส่วนฟิลเตอร์เลือกพิกัดหน้างาน
    selected_face = st.radio("เลือกพิกัดหน้างาน:", ["หน้า A", "หน้า B", "หน้า C"], horizontal=True, key=f"rf_{defect}")

    # 🛠️ สถานะกล่องล็อกข้อมูลระบบหน้าบ้าน
    st.markdown('<div class="login-card" style="padding: 10px 15px;">', unsafe_allow_html=True)
    st.markdown("<p style='font-size:12px; font-weight:bold; color:#64748b; margin-bottom:2px;'>⚙️ สถานะกล่องรับข้อมูลระบบหน้าจอ (ตรวจสอบความพร้อมก่อนส่ง):</p>", unsafe_allow_html=True)
    
    short_face = str(selected_face).replace("หน้า", "").strip()
    box_face = st.text_input("Improvement type (คอลัมน์ G):", value=short_face, disabled=True)
    
    short_defect = "".join(filter(str.isdigit, str(defect)))
    box_defect = st.text_input("errortype (คอลัมน์ F):", value=short_defect, disabled=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if selected_face in ["หน้า A", "หน้า B", "หน้า C"] and selected_material != "ไม่มีข้อมูล":
        face_char = selected_face.split()[-1]
        folder_info = FOLDER_LINK_MAP[face_char][defect]

        # 📁 1. คลังภาพหลักชิ้นงาน (บังคับอัปโหลดได้รูปเดียว + ล็อกปิดปุ่มบวกเนียน ๆ + เพิ่มปุ่มลบรูปภาพ)
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown(f"<b style='color:#005aab; font-size:14px;'>📁 1. คลังภาพหลักชิ้นงาน ({folder_info['main_title']}) ของ {selected_material}</b>", unsafe_allow_html=True)
        st.markdown(f'<a href="{folder_info["main_url"]}" target="_blank" class="drive-link-button">🖼️ กดเปิดคลังภาพใหญ่ {folder_info["main_title"]} ↗️</a>', unsafe_allow_html=True)
        
        # คีย์ตรวจสอบรูปภาพหลักใน Session State เพื่อควบคุม UI
        session_img_key = f"stored_main_img_{defect}"
        if session_img_key not in st.session_state:
            st.session_state[session_img_key] = None

        # 🛠️ ตรรกะควบคุมทางเลือกอัจฉริยะ: ถ้ายังไม่มีรูปให้โชว์ช่องอัปโหลด ถ้ามีรูปแล้วให้ซ่อนช่องและเปิดปุ่มลบ (X) แทน
        if st.session_state[session_img_key] is None:
            uploaded_main = st.file_uploader(f"แนบรูปภาพหลักที่เลือกของ {selected_material} ที่นี่ (จำกัด 1 รูป):", type=["png", "jpg", "jpeg"], accept_multiple_files=False, key=f"uploader_main_{defect}")
            if uploaded_main:
                st.session_state[session_img_key] = uploaded_main.getvalue()
                st.rerun()
        else:
            # ซ่อน Uploader เก่าทิ้งไปเลย ทำให้ปุ่มเครื่องหมายบวกหายเกลี้ยง 100% พนักงานจะหมดสิทธิ์เลือกรูปเพิ่ม
            st.markdown("<p style='font-size:13px; color:#2c3e50; font-weight:bold;'>✅ รูปภาพหลักถูกแนบเรียบร้อยแล้ว:</p>", unsafe_allow_html=True)
            st.image(st.session_state[session_img_key], use_container_width=True)
            
            # เปิดสวิตช์ปุ่มกากบาทสีแดงสำหรับล้างภาพเพื่อเปลี่ยนรูปใหม่กรณีเลือกผิด
            if st.button("❌ กดลบรูปภาพนี้เพื่อเลือกใหม่", key="clear_image_btn"):
                st.session_state[session_img_key] = None
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)

        # 📁 2. คลังรูปรายละเอียดจุดย่อย
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown(f"<b style='color:#007bc3; font-size:14px;'>📁 2. คลังรูปรายละเอียดจุดย่อย ({folder_info['slave_title']})</b>", unsafe_allow_html=True)
        st.markdown(f'<a href="{folder_info["slave_url"]}" target="_blank" class="drive-link-button">🖼️ กดเปิดคลังภาพย่อย {folder_info['slave_title']} ↗️</a>', unsafe_allow_html=True)
        uploaded_slaves = st.file_uploader("แนบรูปรายละเอียดจุดย่อย (สูงสุด 5 รูป):", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="up_slave_work")
        if uploaded_slaves:
            for idx, img_file in enumerate(uploaded_slaves[:5]): st.image(img_file, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 🔲 ส่วนสรุปรายละเอียดงาน AFTER
    st.markdown('<div class="login-card" style="border-top: 4px solid #10b981;">', unsafe_allow_html=True)
    st.markdown(f"<b style='color:#10b981; font-size:14px; display:block; margin-bottom:5px;'>✨ ส่วนอัปเดตงาน After ({defect_title} - {selected_material})</b>", unsafe_allow_html=True)
    
    after_text = st.text_area("พิมพ์ข้อความสรุปรายละเอียดผลงาน After:", value="", key="text_area_improvement_details")
    
    uploaded_after_file = st.file_uploader("📂 เลือกไฟล์ภาพ After จากเครื่องของคุณ:", type=["png", "jpg", "jpeg"], key="up_after_file_machine")
    if uploaded_after_file: st.image(uploaded_after_file, caption="✅ รูปภาพ After จากไฟล์เครื่องพรีวิว", use_container_width=True)
        
    camera_after_file = st.camera_input("📸 ถ่ายภาพยืนยันผลงาน After ชิ้นงานจริง", key="camera_input_after_live")
    if camera_after_file: st.image(camera_after_file, caption="✅ รูปภาพ After จากกล้องพรีวิว", use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if 'user_info' in st.session_state and st.session_state.user_info:
        emp_id_val = str(st.session_state.user_info.get('id', '-'))
        emp_name_val = str(st.session_state.user_info.get('name', '-'))
        emp_position_val = str(st.session_state.user_info.get('position', 'GL'))
        if emp_position_val in ["", "None", "-", "nan"]: emp_position_val = "GL"
    else:
        emp_id_val, emp_name_val, emp_position_val = "-", "-", "GL"

    render_employee_details_footer()
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 💾 ปุ่มบันทึกข้อมูล พร้อมเงื่อนไขดักตรวจสอบภาพหัวข้อ 2
    if not after_text.strip():
        if st.button("💾 บันทึกข้อมูล", key=f"save_btn_{defect}"):
            st.error("⚠️ โปรดกรอกข้อความสรุปรายละเอียดผลงาน After ก่อนกดบันทึก!")
    else:
        if st.button("💾 บันทึกข้อมูล", key=f"save_btn_{defect}"):
            slave_count = len(uploaded_slaves) if uploaded_slaves else 0
            if slave_count < 3:
                st.error(f"⚠️ บันทึกไม่สำเร็จ! โปรดแนบรูปรายละเอียดจุดย่อยในหัวข้อ 2 อย่างน้อย 3 ภาพ (ปัจจุบันมี {slave_count} ภาพ)")
            elif st.session_state[session_img_key] is None:
                st.error("⚠️ บันทึกไม่สำเร็จ! โปรดแนบรูปภาพหลักชิ้นงานในหัวข้อ 1 ก่อนกดบันทึก!")
            else:
                with st.spinner("⏳ กำลังบันทึกข้อมูล โปรดรอสักครู่..."):
                    with app_lock:
                        save_timestamp = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        date_string = str(datetime.now().strftime("%Y%m%d"))
                        
                        send_position = str(emp_position_val).strip()
                        send_material = str(selected_material).strip()
                        send_errortype = str(box_defect).strip()
                        send_improvement_type = str(box_face).strip()
                        send_details = str(after_text).strip()

                        # ดึงไฟล์ภาพเดี่ยว Picture Master (Before) จากหน่วยความจำ Session State
                        before_master_base64 = base64.b64encode(st.session_state[session_img_key]).decode('utf-8')

                        # แปลงไฟล์ภาพย่อย Picture 1-5 (Before) เป็นลิสต์ Base64 (สูงสุด 5 ภาพ)
                        before_slaves_base64 = []
                        if uploaded_slaves:
                            for img in uploaded_slaves[:5]:
                                before_slaves_base64.append(base64.b64encode(img.getvalue()).decode('utf-8'))

                        # แปลงไฟล์ภาพหลักผลงาน After เป็น Base64
                        after_pic_base64 = ""
                        if camera_after_file:
                            after_pic_base64 = base64.b64encode(camera_after_file.getvalue()).decode('utf-8')
                        elif uploaded_after_file:
                            after_pic_base64 = base64.b64encode(uploaded_after_file.getvalue()).decode('utf-8')

                        payload = {
                            "timestamp": save_timestamp,
                            "date_str": date_string,
                            "employee_id": str(emp_id_val),
                            "employee_name": str(emp_name_val),
                            "position": send_position,
                            "material": send_material,
                            "errortype": send_errortype,
                            "improvement_type": send_improvement_type,
                            "improvement_details": send_details,
                            "before_master": before_master_base64,
                            "before_slaves": before_slaves_base64,
                            "after_pic": after_pic_base64
                        }
                        
                        try:
                            response = requests.post(APPS_SCRIPT_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"})
                            if response.status_code == 200:
                                st.success(f"🎉 บันทึกข้อมูลและจัดส่งรูปภาพเข้าโฟลเดอร์ส่วนกลางสำเร็จเรียบร้อยแล้วครับ!")
                                # เคลียร์รูปภาพหลักหลังส่งข้อมูลสำเร็จ
                                st.session_state[session_img_key] = None
                                st.session_state.page = "select_defect"
                                st.rerun()
                            else:
                                st.error(f"❌ บันทึกไม่สำเร็จ (Error Code: {response.status_code})")
                        except Exception as ex:
                            st.error(f"⚠️ เกิดข้อผิดพลาดในการเชื่อมต่อเครือข่าย: {ex}")
                    
    st.markdown('</div>', unsafe_allow_html=True)
