import streamlit as st
import pandas as pd
import requests
import json
import base64
import plotly.graph_objects as go
from datetime import datetime

# 🌐 ลิงก์ Web App URL ตัวล่าสุดของคุณวีรพันธ์ที่ได้รับการตรวจสอบความถูกต้องแล้ว
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbznvtGilprFX4wuoCQHM_d-bYwwz9Ck7S0RK8JcxIXpzfoFnlcg-A8iflC50Ay0NbPPSQ/exec"

# 1. ตั้งค่าหน้าเว็บสไตล์สมาร์ทโฟน
st.set_page_config(page_title="TOG App", layout="centered", initial_sidebar_state="collapsed")

# 2. 🎨 CSS ตกแต่งหน้าจอโทรศัพท์ - แก้ไขข้อบกพร่องเรื่องปุ่มทับซ้อนกันเรียบร้อยครับ
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
        padding: 105px 24px 24px 24px !important; box-shadow: 0 20px 50px rgba(0,0,0,0.3) !important;
        min-height: 90vh !important; height: auto !important;
    }
    .login-card {
        background-color: white !important; border-radius: 20px !important; padding: 15px !important; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important; margin-bottom: 15px !important; width: 100% !important;
    }
    .future-graph-card {
        background-color: rgba(0,0,0,0) !important; border: none !important; padding: 5px !important; margin-bottom: 15px !important; width: 100% !important;
    }
    
    /* 🛠️ จัดระเบียบแถบควบคุม Navbar ด้านบนเพื่อไม่ให้ปุ่ม Home ซ้อนทับกัน */
    .custom-top-navbar {
        position: absolute !important; top: 25px !important; left: 24px !important; right: 24px !important; 
        display: flex !important; justify-content: space-between !important; align-items: center !important; z-index: 999999 !important;
    }
    .nav-btn-link {
        background-color: #bae6fd !important; color: #000000 !important; border: 1px solid rgba(0,0,0,0.05) !important;
        border-radius: 20px !important; padding: 8px 14px !important; font-size: 13px !important; font-weight: bold !important; text-decoration: none !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important; display: inline-block !important;
    }
    
    .tog-logo-circle {
        width: 50px !important; height: 50px !important; background-color: rgba(0, 0, 0, 0.2) !important; border: 1px solid rgba(0, 0, 0, 0.1) !important;
        border-radius: 50% !important; display: flex !important; justify-content: center !important; align-items: center !important; color: #000000 !important; font-weight: bold !important; font-size: 15px !important; margin: 0 auto 8px auto !important;
    }
    .center-header-block {
        display: flex !important; flex-direction: column !important; align-items: center !important; justify-content: center !important; text-align: center !important; margin-top: 15px !important; margin-bottom: 25px !important; width: 100% !important;
    }
    .drive-link-button {
        display: block !important; text-align: center !important; background-color: #10b981 !important; color: white !important;
        font-weight: bold !important; padding: 12px 20px !important; border-radius: 12px !important; text-decoration: none !important;
        margin: 12px 0 !important; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25) !important; font-size: 14px !important;
    }
    .employee-dark-box {
        background-color: rgba(0, 0, 0, 0.07) !important; border: 2px solid rgba(0, 0, 0, 0.12) !important; border-radius: 24px !important; padding: 16px !important; margin-top: 10px !important; margin-bottom: 15px !important; color: #000000 !important; font-size: 14px !important; line-height: 1.6 !important; box-shadow: inset 0 1px 4px rgba(0,0,0,0.02) !important;
    }
    .defect-title-box {
        background-color: #dbeafe !important; border: 1px solid #bfdbfe !important; border-radius: 16px !important; padding: 12px !important; text-align: center !important; color: #000000 !important; font-weight: bold !important; font-size: 14px !important; margin-top: 10px !important; margin-bottom: 16px !important;
    }
    div.stButton > button {
        background-color: rgba(186, 230, 253, 0.5) !important; backdrop-filter: blur(6px) !important; -webkit-backdrop-filter: blur(8px) !important; color: #000000 !important; font-weight: bold !important; font-size: 14px !important; border: 2px solid rgba(255, 255, 255, 0.7) !important; border-radius: 16px !important; width: 100% !important; padding: 12px 20px !important; margin-bottom: 12px !important; display: block !important; box-shadow: 0 4px 15px rgba(0,0,0,0.02), inset 0 1px 2px rgba(255,255,255,0.3) !important; transition: all 0.2s ease !important;
    }
    div.stButton > button:hover { background-color: rgba(125, 211, 252, 0.7) !important; border: 2px solid rgba(255, 255, 255, 0.9) !important; transform: translateY(-1px) !important; }
    div.stButton > button[key^="save_btn_"] { background-color: #10b981 !important; color: white !important; font-size: 16px !important; border: 2px solid #059669 !important; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important; }
    div.stButton > button[key^="save_btn_"]:hover { background-color: #059669 !important; }
    .error-pastel-box { background-color: rgba(239, 68, 68, 0.15) !important; border: 2px solid rgba(239, 68, 68, 0.3) !important; border-radius: 16px !important; padding: 12px 18px !important; margin-top: 12px !important; margin-bottom: 12px !important; color: #000000 !important; font-size: 14px !important; font-weight: bold !important; text-align: center !important; }
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
                pos_val = str(row['Position']).strip() if 'Position' in df.columns else "GL"
                return {"status": "success", "found": True, "id": str(row['ID']), "name": str(row['Name']).strip(), "position": pos_val}
    except:
        pass
    return {"status": "success", "found": False}

# 📊 ฟังก์ชันดึงข้อมูลดิบสถิติ
@st.cache_data(ttl=60)
def load_real_defect_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/1qKY4ZBWYXM81Y8BZSMjOf7z1hJXeJFCjB5KeRPQBe4c/export?format=csv&gid=0"
    try:
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

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
        261: {"main_url": "https://drive.google.com/drive/folders/1slgqqMbiRttmRd70hbPkV_DAKoiqGbht", "main_title": "C_261", "slave_url": "https://drive.google.com/drive/folders/1FzfsI-xDgUQPnB_6kDrQ8iGxI5_N075P", "slave_title": "SC_261"},
        380: {"main_url": "https://drive.google.com/drive/folders/14jkMpOZG-bIN6h0EYbZ3UrqiFAYUQ7A1", "main_title": "C_380", "slave_url": "https://drive.google.com/drive/folders/11OR4QaWPaLcM6EPaSPrMkQTQrpfqMMJT", "slave_title": "SC_380"}
    }
}

if 'page' not in st.session_state: st.session_state.page = "login"
if 'user_info' not in st.session_state: st.session_state.user_info = None
if 'current_defect' not in st.session_state: st.session_state.current_defect = None
if 'clear_trigger' not in st.session_state: st.session_state.clear_trigger = 0

current_page = st.session_state.page

st.markdown('<div class="custom-top-navbar"><a href="?nav=reset" target="_self" class="nav-btn-link">🏠 Home</a><a href="?nav=reset" target="_self" class="nav-btn-link">🚪 Logout</a></div>', unsafe_allow_html=True)
if st.query_params.get("nav") == "reset":
    st.session_state.page = "login"; st.session_state.user_info = None; st.session_state.current_defect = None
    st.query_params.clear(); st.rerun()

# ---------------- หน้าแรก: Login ----------------
if current_page == "login":
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='font-size:16px; margin-top:0; color:#2c3e50; text-align:center;'>🪪 ป้อนรหัสพนักงานเพื่อเข้าระบบ</h4>", unsafe_allow_html=True)
    input_id = st.text_input("กรอกรหัส ID พนักงานของคุณ:", value="", placeholder="พิมพ์ตัวเลขรหัส เช่น 20", label_visibility="collapsed")
    if input_id.strip() != "":
        result = get_employee_from_sheet(input_id)
        if result["status"] == "success" and result.get("found"):
            now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.user_info = {"id": result["id"], "name": result["name"], "position": result["position"], "timestamp": now_time}
            st.markdown(f'<div class="employee-dark-box"><b>⏱️ Timestamp:</b> {now_time}<br><b>🆔 Employee ID:</b> {result["id"]}<br><b>👤 Name:</b> {result["name"]}<br><b>💼 Position:</b> {result["position"]}</div>', unsafe_allow_html=True)
            if st.button("🔓 กดเพื่อเข้าระบบ"):
                st.session_state.page = "select_defect"; st.rerun()
        else:
            st.markdown('<div class="error-pastel-box">❌ ไม่พบข้อมูล โปรดคีย์ ID อีกครั้ง</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- หน้าสอง: คัดเลือก Defect ----------------
elif current_page == "select_defect":
    st.markdown('<div class="employee-dark-box">', unsafe_allow_html=True)
    if st.session_state.user_info:
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.markdown(f"<b>⏱️ Timestamp:</b> {now_time}<br><b>🆔 Employee ID:</b> {st.session_state.user_info.get('id')}<br><b>👤 Name:</b> {st.session_state.user_info['name']}<br><b>💼 Position:</b> {st.session_state.user_info['position']}<hr style='margin: 12px 0; border: 0; border-top: 1px dashed rgba(0,0,0,0.15);'>", unsafe_allow_html=True)
    st.markdown('<div class="defect-title-box">🎯 โปรดเลือกประเภท Defect ที่ต้องการปรับปรุง</div>', unsafe_allow_html=True)
    if st.button("🟠 Defect 260 (Rough Lines)"): st.session_state.current_defect = 260; st.session_state.page = "defect_view"; st.rerun()
    if st.button("🔵 Defect 261 (Grinding Structure)"): st.session_state.current_defect = 261; st.session_state.page = "defect_view"; st.rerun()
    if st.button("⚫ Defect 380 (Contour/Design Fault)"): st.session_state.current_defect = 380; st.session_state.page = "defect_view"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- หน้าสาม: บอร์ดสถิติและการบันทึกผล ----------------
elif current_page == "defect_view":
    defect = st.session_state.current_defect
    defect_title = f"Defect {defect}"
    
    # 🛠️ ย้ายปุ่มกลับไปเลือกประเภทอื่นๆ ลงมาด้านล่าง Navbar เล็กน้อยไม่ให้เบียดกัน
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🔙 กลับไปเลือกประเภท Defect อื่น"): st.session_state.page = "select_defect"; st.rerun()
        
    st.markdown(f'<div class="login-card" style="text-align:center; color:#000000; font-weight:bold;"><b>📊 แผนภูมิ Defect {defect}</b></div>', unsafe_allow_html=True)
    
    raw_df = load_real_defect_data()
    if not raw_df.empty and 'errortype' in raw_df.columns and 'Material' in raw_df.columns:
        raw_df['errortype'] = pd.to_numeric(raw_df['errortype'], errors='coerce')
        raw_df['Material'] = raw_df['Material'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
        filtered_df = raw_df[raw_df['errortype'] == defect]
        qty_col = 'rework quantity' if 'rework quantity' in raw_df.columns else raw_df.columns[-1]
        filtered_df[qty_col] = pd.to_numeric(filtered_df[qty_col], errors='coerce').fillna(0)
        summary_df = filtered_df.groupby('Material', as_index=False)[qty_col].sum()
        chart_data = summary_df.sort_values(by=qty_col, ascending=False).head(10)
    else:
        chart_data = pd.DataFrame({"Material": ["407787135", "407652035"], "rework quantity": [51, 45]})
        qty_col = "rework quantity"

    if not chart_data.empty:
        list_of_materials = chart_data['Material'].tolist()
        state_key = f"sel_mat_{defect}"
        if state_key not in st.session_state: st.session_state[state_key] = list_of_materials[0]
        
        st.markdown('<div class="future-graph-card">', unsafe_allow_html=True)
        st.markdown(f"<b style='color:#000000; font-size:15px; display:block; text-align:center;'>📊 รายงาน 10 อันดับ Defect {defect} ที่พบ</b>", unsafe_allow_html=True)
        
        neon_pastel = ['#4ef0d0', '#ffb37e', '#ff9f9f', '#d39fff', '#9fccff', '#9fff9f', '#f4ff9f', '#ff9fe2', '#b3b3ff', '#e6ffb3']
        color_map = {mat: neon_pastel[idx % len(neon_pastel)] for idx, mat in enumerate(list_of_materials)}
        
        fig_bar = go.Figure()
        for mat in list_of_materials:
            val = chart_data[chart_data['Material'] == mat][qty_col].values[0]
            fig_bar.add_trace(go.Bar(
                x=[mat], y=[val], name=mat, marker=dict(color=color_map[mat], line=dict(color='#ffffff', width=2)),
                hovertemplate=f"Material: {mat}<br>จำนวน: {val} ครั้ง<extra></extra>"
            ))
        fig_bar.update_layout(
            margin=dict(l=10, r=10, t=10, b=10), height=230, showlegend=False, barmode='group',
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(type='category', tickangle=45, tickfont=dict(color='#000000', size=9, weight='bold')),
            yaxis=dict(tickfont=dict(color='#000000', size=9, weight='bold'))
        )
        selected_bar = st.plotly_chart(fig_bar, use_container_width=True, on_select="rerun")
        
        st.markdown(f"<p style='font-size:13px; color:#000000; font-weight:bold; text-align:center; margin-top:8px; margin-bottom:5px;'>💡 เลือก Material ที่ต้องการปรับปรุงจากกราฟ</p>", unsafe_allow_html=True)
        
        if selected_bar and "selection" in selected_bar and selected_bar["selection"]["points"]:
            st.session_state[state_key] = selected_bar["selection"]["points"][0]["x"]
            
        selected_material = st.session_state[state_key]
        st.markdown("<hr style='margin:10px 0; border:0; border-top:1px dashed #cbd5e1;'>", unsafe_allow_html=True)
        st.markdown(f'<div style="background-color: #f0fdf4; border: 2px solid #16a34a; padding: 10px; border-radius: 12px; text-align: center; font-size:14px; color:#16a34a; box-shadow: 0 4px 12px rgba(22, 163, 74, 0.08);"><b>🔍 TARGET MATERIAL SELECTED:</b> <span style="font-size:16px; font-weight:bold; color:#007bc3;">{selected_material}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        selected_material = "ไม่มีข้อมูล"

    selected_face = st.radio("เลือกพิกัดหน้างาน:", ["หน้า A", "หน้า B", "หน้า C"], horizontal=True, key=f"rf_{defect}")
    if selected_face in ["หน้า A", "หน้า B", "หน้า C"] and selected_material != "ไม่มีข้อมูล":
        face_char = selected_face.split()[-1]
        folder_info = FOLDER_LINK_MAP[face_char][defect]
        
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown(f"<b style='color:#005aab; font-size:14px;'>📁 1. คลังภาพหลักชิ้นงาน ({folder_info['main_title']}) ของ {selected_material}</b>", unsafe_allow_html=True)
        st.markdown(f'<a href="{folder_info["main_url"]}" target="_blank" class="drive-link-button">🖼️ กดเปิดคลังภาพใหญ่ {folder_info["main_title"]} ↗️</a>', unsafe_allow_html=True)
        uploaded_main = st.file_uploader("แนบรูปภาพหลักที่นี่:", type=["png", "jpg", "jpeg"], key=f"up_m_{defect}_{st.session_state.clear_trigger}")
        if uploaded_main: st.image(uploaded_main, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown(f"<b style='color:#007bc3; font-size:14px;'>📁 2. คลังรูปรายละเอียดจุดย่อย ({folder_info['slave_title']})</b>", unsafe_allow_html=True)
        st.markdown(f'<a href="{folder_info["slave_url"]}" target="_blank" class="drive-link-button">🖼️ กดเปิดคลังภาพย่อย {folder_info["slave_title"]} ↗️</a>', unsafe_allow_html=True)
        uploaded_slaves = st.file_uploader("แนบรูปรายละเอียดจุดย่อย (สูงสุด 5 รูป):", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key=f"up_s_multiple_{defect}_{st.session_state.clear_trigger}")
        if uploaded_slaves:
            for idx, img_file in enumerate(uploaded_slaves[:5]): st.image(img_file, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 🔲 ส่วนสรุปรายละเอียดงาน AFTER
    st.markdown('<div class="login-card" style="border-top: 4px solid #10b981;">', unsafe_allow_html=True)
    st.markdown(f"<b style='color:#10b981; font-size:14px; display:block; margin-bottom:5px;'>✨ ส่วนอัปเดตงาน After ({defect_title} - {selected_material})</b>", unsafe_allow_html=True)
    after_text = st.text_area("พิมพ์ข้อความสรุปรายละเอียดผลงาน After:", value="", key=f"ta_af_{defect}_{st.session_state.clear_trigger}")
    
    st.markdown("<p style='font-size:13px; font-weight:bold; color:#2c3e50; margin-bottom:2px;'>📸 แนบรูปหลักฐานผลงาน After ชิ้นงานจริง (แนบได้สูงสุด 5 ภาพ):</p>", unsafe_allow_html=True)
    
    uploaded_after_files = st.file_uploader("📂 เลือกไฟล์ภาพ After จากเครื่องของคุณ (สูงสุด 5 ภาพ):", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key=f"up_af_file_{defect}_{st.session_state.clear_trigger}")
    if uploaded_after_files:
        for idx, img_file in enumerate(uploaded_after_files[:5]): st.image(img_file, caption=f"✅ รูปภาพ After ใบที่ {idx+1}", use_container_width=True)
        
    camera_after_file = st.camera_input("📸 ถ่ายภาพยืนยันผลงาน After ชิ้นงานจริง", key=f"c_af_{defect}_final_{st.session_state.clear_trigger}")
    if camera_after_file: st.image(camera_after_file, caption="✅ รูปภาพ After จากกล้องพรีวิว", use_container_width=True)
    
    if st.button("💾 บันทึกข้อมูล", key=f"save_btn_{defect}"):
        if not after_text.strip():
            st.error("⚠️ โปรดกรอกข้อความสรุปรายละเอียดผลงาน After ก่อนกดบันทึก!")
        else:
            save_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            emp_id = st.session_state.user_info.get('id', '-') if st.session_state.user_info else '-'
            emp_name = st.session_state.user_info.get('name', '-') if st.session_state.user_info else '-'
            emp_position = st.session_state.user_info.get('position', '-') if st.session_state.user_info else '-'
            
            img1, img2, img3, img4, img5 = "", "", "", "", ""
            base64_list = []
            
            if uploaded_after_files:
                for img_file in uploaded_after_files[:5]:
                    base64_str = base64.b64encode(img_file.getvalue()).decode('utf-8')
                    base64_list.append(base64_str)
                    
            if camera_after_file and len(base64_list) < 5:
                camera_base64 = base64.b64encode(camera_after_file.getvalue()).decode('utf-8')
                base64_list.append(camera_base64)
                
            if len(base64_list) > 0: img1 = base64_list[0]
            if len(base64_list) > 1: img2 = base64_list[1]
            if len(base64_list) > 2: img3 = base64_list[2]
            if len(base64_list) > 3: img4 = base64_list[3]
            if len(base64_list) > 4: img5 = base64_list[4]

            # 🛠️ ส่งจับคู่ข้อมูลตามสิทธิ์ของคอลัมน์ใหม่ (ตรงกับตาราง Google Sheet ล่าสุดที่คุณวีรพันธ์กำหนดไว้เป๊ะๆ)
            payload = {
                "timestamp": save_timestamp, 
                "employee_id": emp_id, 
                "employee_name": emp_name, 
                "position": emp_position,           # 📁 Column D: ตำแหน่งพนักงานจริง (GL)
                "material": str(selected_material),  # 📁 Column E: รหัส Material 
                "defect_improvement": str(defect),   # 📁 Column F: รหัสหมายเลข Defect ล้วน (เช่น 261)
                "improvement_type": str(selected_face), # 📁 Column G: พิกัดหน้างาน (เช่น หน้า A)
                "after_details": str(after_text),    # 📁 Column M: ข้อความผลงาน After
                "pic1": img1, "pic2": img2, "pic3": img3, "pic4": img4, "pic5": img5
            }
            try:
                response = requests.post(APPS_SCRIPT_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"})
                if response.status_code == 200:
                    st.success("🎉 บันทึกข้อมูลแยกคอลลัมน์ลงตารางเรียบร้อยแล้ว!")
                    st.session_state.clear_trigger += 1
                    st.rerun()
                else:
                    st.error(f"❌ บันทึกไม่สำเร็จ (Error Code: {response.status_code})")
            except Exception as ex:
                st.error(f"⚠️ เกิดข้อผิดพลาด: {ex}")
    st.markdown('</div>', unsafe_allow_html=True)
