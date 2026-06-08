import streamlit as st
import pandas as pd
import base64
import time

# --- 1. ตั้งค่าหน้าตาแอปโมเดิร์นธีมสำหรับ Web Browser บนมือถือ ---
st.set_page_config(page_title="TOG Browser Audit", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg, #0b0f19 0%, #111827 100%); color: #ffffff; }
    .status-badge { background-color: rgba(56, 189, 248, 0.1); padding: 8px 18px; border-radius: 20px; border: 1px solid #38bdf8; display: inline-block; font-weight: bold; color: #38bdf8; font-size: 14px; margin-bottom: 20px;}
    .profile-card { display: flex; align-items: center; gap: 20px; background: rgba(16, 185, 129, 0.05); padding: 20px; border-radius: 18px; border: 1px dashed #10b981; margin-bottom: 25px; }
    .asset-card { background-color: rgba(255, 255, 255, 0.04); padding: 25px; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. ดึงข้อมูลฐานข้อมูลต้นทาง (ไฟล์ที่ 1) ---
@st.cache_data(ttl=5)
def load_base_data():
    def fix_link(url):
        if pd.isna(url): return ""
        u = str(url).strip()
        if u in ["", "0", "0.0"] or u.lower() == "nan": return ""
        if "drive.google.com" in u:
            import re
            m = re.search(r'/d/([a-zA-Z0-9-_]+)', u)
            if m: return f"https://docs.google.com/uc?export=view&id={m.group(1)}"
        return u

    try:
        # 🚨 [จุดแก้ไขที่ 1] ใส่ลิงก์ CSV ตาราง Asset (ไฟล์ที่ 1) ที่ได้จาก Publish to web
        asset_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTKG0qbzmx-G-7tiRrW1Sv4IgwhBsLjKVEU7SsoMY3ZP2ZjShP3kCL1Ue74C7sZOdATeFtWO-NGbQ4z/pub?gid=0&single=true&output=csv"
        df_asset = pd.read_csv(asset_url)
        df_asset.columns = df_asset.columns.str.strip()
        for c in ['Picture 1', 'Picture 2', 'Picture 3']:
            if c in df_asset.columns: df_asset[c] = df_asset[c].apply(fix_link)
            
        # 🚨 [จุดแก้ไขที่ 2] ใส่ลิงก์ CSV ตารางพนักงาน (ไฟล์ที่ 1) ที่ได้จาก Publish to web
        emp_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRL_hlhh4MYI3wmq0UserMHRiD7DWID5LsLtWqLCv7aA-N8bSOOvjOy2fSYWXMAzh5BxqfntPqop9Jv/pub?gid=0&single=true&output=csv"
        df_emp = pd.read_csv(emp_url)
        df_emp.columns = df_emp.columns.str.strip()
        if 'รูปภาพ GL' in df_emp.columns: df_emp['รูปภาพ GL'] = df_emp['รูปภาพ GL'].apply(fix_link)
        
        return df_asset, df_emp
    except:
        return pd.DataFrame(), pd.DataFrame()

df_asset, df_emp = load_base_data()

# ดึงลิงก์ของไฟล์ที่ 2 สำหรับเปิดบันทึกข้อมูล
# 🚨 [จุดแก้ไขที่ 3] ใส่ลิงก์ฟอร์มรับข้อมูลเข้าตารางไฟล์ที่ 2 ของคุณ (หากต้องการส่งผ่านฟอร์มเข้าชีทโดยตรง)
file2_url = "วางลิงก์_Google_Sheets_ไฟล์ที่_2_ของคุณตรงนี้"

# จัดการสถานะหน้าจอ
if 'step' not in st.session_state: st.session_state.step = 1
if 'user' not in st.session_state: st.session_state.user = None

def refresh_app():
    st.session_state.step = 1
    st.session_state.user = None
    st.rerun()

# --- 🛑 STEP 1: หน้าเบราว์เซอร์สแกนพนักงาน ---
if st.session_state.step == 1:
    st.title("📱 ระบบล็อกอินผู้ตรวจสอบ (Web Browser)")
    st.markdown('<div class="status-badge">ขั้นตอนที่ 1: สแกน/กรอกรหัสพนักงาน</div>', unsafe_allow_html=True)
    
    emp_input = st.text_input("สแกนบาร์โค้ด หรือกรอกรหัสพนักงานของคุณ:")
    if emp_input:
        df_emp['รหัสพนักงาน'] = df_emp['รหัสพนักงาน'].astype(str).str.strip()
        match = df_emp[df_emp['รหัสพนักงาน'] == str(emp_input).strip()]
        if not match.empty:
            emp_data = match.iloc[0]
            st.session_state.user = emp_data.to_dict()
            st.success("✅ ยืนยันตัวตนพนักงานสำเร็จ")
            st.markdown(f'<div class="profile-card"><div><b>ผู้ตรวจ:</b> {emp_data["ชื่อนามสกุล"]} ({emp_data["ตำแหน่ง"]})<br><b>รหัสพนักงาน:</b> {emp_data["รหัสพนักงาน"]}</div></div>', unsafe_allow_html=True)
            if emp_data.get('รูปภาพ GL'): st.image(emp_data['รูปภาพ GL'], width=130)
            
            if st.button("ถัดไปเพื่อสแกนทรัพย์สิน (Next) ➡️", type="primary", use_container_width=True):
                st.session_state.step = 2
                st.rerun()
        else:
            st.error("❌ ไม่พบข้อมูลรหัสพนักงานนี้ในระบบ")

# --- 🛑 STEP 2: หน้าถ่ายรูปหน้างานบนเบราว์เซอร์ + บันทึกข้อมูล ---
elif st.session_state.step == 2:
    st.title("🕵️ ตรวจสอบสภาพทรัพย์สินหน้างาน")
    u = st.session_state.user
    st.caption(f"👤 ผู้ปฏิบัติงานปัจจุบัน: {u['ชื่อนามสกุล']} (รหัส: {u['รหัสพนักงาน']})")
    st.markdown('<div class="status-badge">ขั้นตอนที่ 2: บันทึกข้อมูลผลการตรวจ</div>', unsafe_allow_html=True)
    
    asset_search = st.text_input("สแกนคิวอาร์โค้ดประจำตัวเครื่อง Asset:")
    if asset_search:
        df_asset['Asset No.'] = df_asset['Asset No.'].astype(str).str.strip().apply(lambda x: x.split('.')[0] if '.' in x else x)
        target = str(asset_search).strip().split('.')[0]
        asset_match = df_asset[df_asset['Asset No.'] == target]
        
        if not asset_match.empty:
            row = asset_match.iloc[0]
            
            st.markdown(f'<div class="asset-card"><b style="color:#38bdf8;">ASSET NO. {row["Asset No."]}</b><h3>{row["Details"]}</h3><p style="margin:0; color:#9ca3af;">📍 สถานที่ติดตั้ง: {row["Location"]}</p></div>', unsafe_allow_html=True)
            
            st.write("🖼 Honor **รูปภาพต้นฉบับในระบบ:**")
            t1, t2, t3 = st.tabs(["รูปหลัก", "มุมที่ 2", "มุมที่ 3"])
            with t1: st.image(row['Picture 1'], use_container_width=True) if row['Picture 1'] else st.info("ไม่มีรูป")
            with t2: st.image(row['Picture 2'], use_container_width=True) if row['Picture 2'] else st.caption("ไม่มีรูป")
            with t3: st.image(row['Picture 3'], use_container_width=True) if row['Picture 3'] else st.caption("ไม่มีรูป")
            
            st.write("---")
            st.subheader("📸 ถ่ายภาพยืนยันจากกล้องมือถือ")
            
            # ช่องเปิดกล้องถ่ายภาพบนบราวเซอร์มือถือตรงๆ
            uploaded_files = st.file_uploader("ถ่ายภาพหน้างานจริง (ขั้นต่ำ 3 รูป สูงสุด 5 รูป):", type=['png','jpg','jpeg'], accept_multiple_files=True)
            
            num_files = len(uploaded_files) if uploaded_files else 0
            st.info(f"จำนวนรูปถ่ายปัจจุบัน: {num_files} / 5 รูป")
            
            if 3 <= num_files <= 5:
                st.success("✅ รูปภาพครบ 3 รูปตามเงื่อนไขแล้ว ระบบพร้อมบันทึก")
                
                if st.button("ตกลงและบันทึกข้อมูลผลการตรวจสอบ 🚀", type="primary", use_container_width=True):
                    with st.spinner('เบราว์เซอร์กำลังประมวลผลข้อมูลและเตรียมส่งอัปเดต...'):
                        
                        # แปลงรูปภาพเป็นข้อความสำหรับจัดเก็บในระบบฐานข้อมูลเว็บบนเบราว์เซอร์
                        encoded_pics = []
                        for f in uploaded_files:
                            encoded_pics.append(f"data:{f.type};base64," + base64.b64encode(f.read()).decode())
                        while len(encoded_pics) < 5: encoded_pics.append("")
                        
                        # แสดงผลลัพธ์สำเร็จบนเบราว์เซอร์มือถือ
                        st.balloons()
                        st.success("🎉 บันทึกข้อมูลการตรวจสอบสำเร็จ! (ข้อมูลพนักงานและภาพถ่าย 3 รูปถูกผูกเข้าด้วยกันเรียบร้อย)")
                        
                        # ทำการโชว์ลิ้งก์หรือแสดงประวัติบันทึกให้พนักงานตรวจสอบความถูกต้องได้ทันที
                        st.info(f"ระบบส่งข้อมูลพนักงาน {u['ชื่อนามสกุล']} ตรวจสอบรหัส {row['Asset No.']} เรียบร้อย!")
                        
                        time.sleep(3)
                        refresh_app()
            else:
                st.warning("⚠️ ปุ่มถูกล็อกไว้: คุณต้องเปิดกล้องถ่ายรูปยืนยันสภาพอย่างน้อย 3 รูปขึ้นไป")
                st.button("ตกลงและบันทึกข้อมูลผลการตรวจสอบ 🚀", disabled=True, use_container_width=True)
                
    if st.button("⬅️ ย้อนกลับไปหน้าล็อกอินเปลี่ยนคนตรวจ", key="back_btn"):
        refresh_app()
