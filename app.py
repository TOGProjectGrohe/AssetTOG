import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. ตั้งค่าหน้าเว็บพื้นฐานให้กระชับเข้ามุมมองสไตล์สมาร์ทโฟน
st.set_page_config(page_title="TOG App", layout="centered", initial_sidebar_state="collapsed")

# 2. 🛠️ CSS ฉบับสมบูรณ์ คุมหน้าจอมือถือ จัดกลาง และตีกรอบปุ่มสวยงาม
st.markdown("""
    <style>
    .stDeployButton, [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], header, footer, #MainMenu {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }
    [data-testid="stStatusWidget"], #stConnectionStatus, div[class*="viewerBadge"], div[class*="st-emotion-cache-"] button[title="Manage app"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }
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
    [data-testid="stMainBlockContainer"], [data-testid="stVerticalBlock"], [data-testid="stVerticalBlockRoot"], div[data-testid="element-container"], .stColumn {
        width: 100% !important; max-width: 100% !important; background-color: transparent !important; border: none !important; box-shadow: none !important; padding: 0px !important; margin: 0px !important;
    }
    .login-card {
        background-color: white !important; border-radius: 20px !important; padding: 15px !important; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important; margin-bottom: 15px !important; width: 100% !important;
    }
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
    div.stButton {
        width: 100% !important; display: flex !important; justify-content: center !important; align-items: center !important; margin-top: 10px !important;
    }
    div.stButton > button {
        background-color: #007bc3 !important; color: white !important; border-radius: 30px !important; padding: 12px 0px !important; font-weight: bold !important; font-size: 15px !important; border: none !important; width: 100% !important; max-width: 340px !important; display: flex !important; justify-content: center !important; align-items: center !important; margin: 0 auto !important; box-shadow: 0 4px 12px rgba(0, 123, 195, 0.25) !important;
    }
    div.stButton > button * {
        display: flex !important; justify-content: center !important; align-items: center !important; text-align: center !important; width: auto !important; margin: 0 auto !important;
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

# 3. 📊 ฐานข้อมูลลิงก์โฟลเดอร์ตามเงื่อนไขที่คุณให้มา
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

# 4. จัดการหน้าเพจและบันทึก State การเลือกกลุ่มข้อมูล
if 'page' not in st.session_state: st.session_state.page = "login"
if 'user_info' not in st.session_state: st.session_state.user_info = None

current_page = st.session_state.page

# --- แถบนำทางด้านบนสุด ---
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

# ---------------- หน้าแรก: Login ----------------
if current_page == "login":
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:18px; margin-top:0; color:#2c3e50; text-align:center;'>🪪 ส่วนพนักงานเข้าใช้งาน</h3>", unsafe_allow_html=True)
    
    enable_camera = st.checkbox("เปิดสิทธิ์ใช้งานกล้องถ่ายรูป", value=True)
    if enable_camera:
        picture = st.camera_input("", label_visibility="collapsed")
        if picture:
            st.session_state.user_info = {
                "id": "EMP-94821", "name": "สมชาย", "surname": "สายลมเย็น",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.page = "dashboard"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("📊 ดูภาพรวม Dashboard", key="btn_login_dash"):
        st.session_state.user_info = {
            "id": "GUEST-001", "name": "ผู้เยี่ยมชม", "surname": "(ทั่วไป)",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.page = "dashboard"
        st.rerun()

# ---------------- หน้าสอง: Dashboard (ครบถ้วนตามเงื่อนไขใหม่) ----------------
elif current_page == "dashboard":
    
    # โชว์ ID, ชื่อ นามสกุล และเวลา
    if st.session_state.user_info:
        info = st.session_state.user_info
        st.markdown(f"""
        <div class="user-profile-box">
            <div style="font-size: 14px; font-weight: bold; color: #1e293b;">👤 พนักงาน: {info['name']} {info['surname']}</div>
            <div style="font-size: 12px; color: #64748b; margin-top: 2px;">รหัสพนักงาน: {info['id']} | เวลาแสกนเข้า: {info['time']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="text-align:center; font-size:17px; font-weight:bold; color:#2c3e50; margin-bottom:15px;">📊 กราฟสรุปผล 3 ประเภท</div>', unsafe_allow_html=True)

    # กราฟประเภทที่ 1: Defect 260
    st.markdown('<div class="login-card" style="padding:8px 15px; margin-bottom:5px;"><b>🔥 Defect 260 (Rough Lines)</b></div>', unsafe_allow_html=True)
    df_260 = get_graph_data(260)
    if not df_260.empty:
        st.markdown('<div class="scrollable-graph-container"><div class="inner-graph-box">', unsafe_allow_html=True)
        fig_260 = px.bar(df_260, x='Material', y='rework quantity', text='rework quantity')
        fig_260.update_traces(textposition='outside', marker_color='#ff7f0e')
        fig_260.update_layout(xaxis=dict(type='category', tickangle=45), yaxis=dict(tickformat='d'), margin=dict(l=10, r=10, t=25, b=50), height=200, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_260, use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    # กราฟประเภทที่ 2: Defect 261
    st.markdown('<div class="login-card" style="padding:8px 15px; margin-bottom:5px;"><b>⚡ Defect 261 (Grinding Structure Visible)</b></div>', unsafe_allow_html=True)
    df_261 = get_graph_data(261)
    if not df_261.empty:
        st.markdown('<div class="scrollable-graph-container"><div class="inner-graph-box">', unsafe_allow_html=True)
        fig_261 = px.bar(df_261, x='Material', y='rework quantity', text='rework quantity')
        fig_261.update_traces(textposition='outside', marker_color='#002060')
        fig_261.update_layout(xaxis=dict(type='category', tickangle=45), yaxis=dict(tickformat='d'), margin=dict(l=10, r=10, t=25, b=50), height=200, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_261, use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    # กราฟประเภทที่ 3: Defect 380
    st.markdown('<div class="login-card" style="padding:8px 15px; margin-bottom:5px;"><b>💥 Defect 380 (Contour/Design Fault)</b></div>', unsafe_allow_html=True)
    df_380 = get_graph_data(380)
    if not df_380.empty:
        st.markdown('<div class="scrollable-graph-container"><div class="inner-graph-box">', unsafe_allow_html=True)
        fig_380 = px.bar(df_380, x='Material', y='rework quantity', text='rework quantity')
        fig_380.update_traces(textposition='outside', marker_color='#000000')
        fig_380.update_layout(xaxis=dict(type='category', tickangle=45), yaxis=dict(tickformat='d'), margin=dict(l=10, r=10, t=25, b=50), height=200, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_380, use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    # --- ส่วนที่สั่งปรับแต่งเพิ่มใหม่: ระบบเลือกรูปภาพ ก่อน/หลัง ---
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown("<b style='color:#1e293b; font-size:14px; display:block; margin-bottom:5px;'>กรอบที่ 1 defect 380 เลือกภาพ Before</b>", unsafe_allow_html=True)
    
    # 1. กล่องวิทยุเลือก หน้า A, B, C หรือ อื่นๆ
    selected_face = st.radio(
        "เลือกตำแหน่งชิ้นงาน:",
        ["หน้า A", "หน้า B", "หน้า C", "อื่นๆ"],
        horizontal=True
    )
    
    # กรณีเลือกหน้าหลัก (A, B, C)
    if selected_face in ["หน้า A", "หน้า B", "หน้า C"]:
        face_key = selected_face.split()[-1] # ดึงเฉพาะตัวอักษร A, B, C
        
        # คัดกรองรหัส Defect ที่ต้องการเจาะลึกดูรูปภาพย่อย
        target_defect = st.selectbox("เลือกรหัส Defect เพื่อเข้าคลังรูปย่อย:", [380, 260, 261])
        
        # ดึงข้อมูลชุดลิงก์ตรงตามที่กำหนดไว้
        folder_info = DRIVE_MAP[face_key][target_defect]
        
        st.markdown(f"""
        <div style="background-color:#f1f5f9; padding:10px; border-radius:10px; font-size:12px; margin: 10px 0;">
            <b>📁 ระบบล็อกพิกัดคลังภาพอัตโนมัติ:</b><br>
            • โฟลเดอร์หลัก ({face_key}_{target_defect}): <a href="{folder_info['main']}" target="_blank">คลิกเปิดดู</a><br>
            • โฟลเดอร์ย่อย ชั้น Slave ({folder_info['slave_name']}): <a href="{folder_info['slave']}" target="_blank">คลิกเปิดดูย่อย</a>
        </div>
        """, unsafe_allow_html=True)
        
        # ตัวเลือกรูปภาพย่อย 5 รายละเอียดภายในกลุ่ม
        sub_img = st.selectbox(
            f"เลือกรายละเอียดภาพย่อยของ {face_key}_{target_defect} (มี 5 ภาพ):",
            ["ภาพรายละเอียดย่อยที่ 1", "ภาพรายละเอียดย่อยที่ 2", "ภาพรายละเอียดย่อยที่ 3", "ภาพรายละเอียดย่อยที่ 4", "ภาพรายละเอียดย่อยที่ 5"]
        )
        st.info(f"📸 กำลังแสดงพรีวิวซอร์สของ: {sub_img}")
        
    # กรณีเลือก "อื่นๆ" -> ระบบเปิดสิทธิ์ให้ถ่ายรูปลงได้เองทันที
    elif selected_face == "อื่นๆ":
        st.markdown("<p style='color:#64748b; font-size:13px;'>📷 โหมดเลือกกำหนดเอง: โปรดกดปุ่มกล้องเพื่อถ่ายภาพชิ้นงาน Before</p>", unsafe_allow_html=True)
        other_pic = st.camera_input("ถ่ายภาพชิ้นงานอื่นๆ", key="cam_before_other")
        if other_pic:
            st.success("บันทึกรูปภาพ Before เรียบร้อย")

    st.markdown('</div>', unsafe_allow_html=True)

    # --- ส่วนด้านล่างสุด: โซน AFTER ---
    st.markdown('<div class="login-card" style="border-top: 4px solid #10b981;">', unsafe_allow_html=True)
    st.markdown("<b style='color:#10b981; font-size:14px; display:block; margin-bottom:5px;'>✨ ส่วนอัปเดตข้อมูลผลลัพธ์ After</b>", unsafe_allow_html=True)
    
    # ช่องพิมพ์ข้อความในส่วน After
    after_text = st.text_area("พิมพ์ข้อความรายละเอียด / สรุปงาน After:", placeholder="กรอกรายละเอียดผลการแก้ไขที่นี่...")
    
    # ถ่ายภาพแนบได้สูงสุด 5 ภาพในส่วน After
    st.markdown("<p style='font-size:12px; color:#475569; margin-bottom:2px;'>📸 แนบรูปถ่าย After (ส่งได้สูงสุด 5 ภาพ):</p>", unsafe_allow_html=True)
    
    after_pics = []
    # ใช้ loop สร้างช่องเปิดกล้องขึ้นมา 5 ช่องเรียงกัน
    for i in range(1, 6):
        pic_captured = st.camera_input(f"ถ่ายภาพ After ชิ้นที่ {i}", key=f"cam_after_{i}")
        if pic_captured:
            after_pics.append(pic_captured)
            
    if after_pics:
        st.toast(f"บันทึกรูปภาพ After สำเร็จแล้ว {len(after_pics)} ภาพ")
        
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
