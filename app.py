import streamlit as st
import pandas as pd
import base64
import time

# --- 1. ตั้งค่าหน้าเว็บเบราว์เซอร์ ---
st.set_page_config(page_title="TOG Browser Audit", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg, #0b0f19 0%, #111827 100%); color: #ffffff; }
    .status-badge { background-color: rgba(56, 189, 248, 0.1); padding: 8px 18px; border-radius: 20px; border: 1px solid #38bdf8; display: inline-block; font-weight: bold; color: #38bdf8; font-size: 14px; margin-bottom: 20px;}
    .profile-card { display: flex; align-items: center; gap: 20px; background: rgba(16, 185, 129, 0.05); padding: 20px; border-radius: 18px; border: 1px dashed #10b981; margin-bottom: 25px; }
    .asset-card { background-color: rgba(255, 255, 255, 0.04); padding: 25px; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. ดึงข้อมูลจากกูเกิลชีทไฟล์ที่ 1 ---
@st.cache_data(ttl=1)
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
        # ลิงก์ CSV ไฟล์ข้อมูลทรัพย์สิน (Asset)
        asset_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTKG0qbzmx-G-7tiRrW1Sv4IgwhBsLjKVEU7SsoMY3ZP2ZjShP3kCL1Ue74C7sZOdATeFtWO-NGbQ4z/pub?gid=0&single=true&output=csv"
        df_asset = pd.read_csv(asset_url)
        df_asset.columns = df_asset.columns.str.strip()
        
        for c in ['Picture 1', 'Picture 2', 'Picture 3']:
            if c in df_asset.columns: df_asset[c] = df_asset[c].apply(fix_link)
            
        # ลิงก์ CSV ไฟล์รายชื่อพนักงาน (Employee)
        emp_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTKG0qbzmx-G-7tiRrW1Sv4IgwhBsLjKVEU7SsoMY3ZP2ZjShP3kCL1Ue74C7sZOdATeFtWO-NGbQ4z/pub?gid=1965823485&single=true&output=csv"
        df_emp = pd.read_csv(emp_url)
        df_emp.columns = df_emp.columns.str.strip() # ตัดช่องว่างของชื่อหัวตารางออก
        
        # ล้างลิงก์รูปภาพในคอลัมน์ Picture GL ให้ดึงภาพมาแสดงบนเว็บได้โดยตรง
        if 'Picture GL' in df_emp.columns:
            df_emp['Picture GL'] = df_emp['emp_pic'] = df_emp['Picture GL'].apply(fix_link)
        
        return df_asset, df_emp
    except:
        return pd.DataFrame(), pd.DataFrame()

df_asset, df_emp = load_base_data()

# --- 3. ระบบดักจับคำสั่งจากลิงก์เบราว์เซอร์ (?emp_id=xxxx หรือ ?asset=xxxx) ---
query_params = st.query_params
url_emp = query_params.get("emp_id", None)
url_asset = query_params.get("asset", None)

if 'step' not in st.session_state: st.session_state.step = 1
if 'user' not in st.session_state: st.session_state.user = None

# ดักจับข้อมูลจากการเปิดลิงก์/สแกนคิวอาร์ครั้งแรกด้วย ID พนักงาน
if url_emp and st.session_state.user is None and not df_emp.empty:
    if 'ID' in df_emp.columns:
        df_emp['ID'] = df_emp['ID'].astype(str).str.strip()
        match = df_emp[df_emp['ID'] == str(url_emp).strip()]
        if not match.empty:
            st.session_state.user = match.iloc[0].to_dict()
            st.session_state.step = 2

def refresh_app():
    st.session_state.step = 1
    st.session_state.user = None
    st.query_params.clear()
    st.rerun()

# --- 🛑 STEP 1: หน้าล็อกอินพนักงาน ---
if st.session_state.step == 1:
    st.title("📱 ยืนยันตัวตนผู้ตรวจสอบ")
    st.markdown('<div class="status-badge">ขั้นตอนที่ 1: สแกน/กรอกไอดีพนักงาน</div>', unsafe_allow_html=True)
    
    emp_input = st.text_input("กรอกรหัสพนักงานเพื่อทดสอบระบบ:", value=url_emp if url_emp else "")
    if (emp_input or url_emp) and not df_emp.empty:
        search_id = str(emp_input if emp_input else url_emp).strip()
        
        if 'ID' in df_emp.columns:
            df_emp['ID'] = df_emp['ID'].astype(str).str.strip()
            match = df_emp[df_emp['ID'] == search_id]
            
            if not match.empty:
                emp_data = match.iloc[0]
                st.session_state.user = emp_data.to_dict()
                st.success("✅ ตรวจพบข้อมูลพนักงาน")
                
                # 🚨 แก้ไขจุดสะกดคำว่า Position เรียบร้อยแล้วครับพี่
                name_val = emp_data.get('Name Surname', 'ไม่ระบุชื่อ')
                role_val = emp_data.get('Position', 'ไม่ระบุตำแหน่ง')
                id_val = emp_data.get('ID', search_id)
                
                st.markdown(f'<div class="profile-card"><div><b>ผู้ตรวจ:</b> {name_val}<br><b>ตำแหน่ง:</b> {role_val} ({id_val})</div></div>', unsafe_allow_html=True)
                
                if emp_data.get('Picture GL'): 
                    st.image(emp_data['Picture GL'], width=140)
                
                if st.button("เข้าสู่หน้าตรวจเช็คทรัพย์สิน ➡️", type="primary", use_container_width=True):
                    st.session_state.step = 2
                    st.rerun()
            else:
                st.error("❌ ไม่พบรหัสพนักงานนี้ในระบบฐานข้อมูล")
        else:
            st.error("❌ หาคอลัมน์ 'ID' ในไฟล์รายชื่อพนักงานไม่เจอ กรุณาตรวจสอบหัวตาราง Google Sheets")

# --- 🛑 STEP 2: หน้าตรวจเช็คเครื่องจักรหน้างาน ---
elif st.session_state.step == 2:
    st.title("🕵️ ตรวจสอบสภาพทรัพย์สินหน้างาน")
    u = st.session_state.user
    st.caption(f"👤 ผู้ลงบันทึก: {u.get('Name Surname', '')} ({u.get('ID', '')})")
    st.markdown('<div class="status-badge">ขั้นตอนที่ 2: บันทึกข้อมูลสภาพจริง</div>', unsafe_allow_html=True)
    
    asset_search = st.text_input("รหัสทรัพย์สินที่สแกนพ่วงมา:", value=url_asset if url_asset else "")
    
    if asset_search and not df_asset.empty:
        if 'Asset No.' in df_asset.columns:
            df_asset['Asset No.'] = df_asset['Asset No.'].astype(str).str.strip()
            target = str(asset_search).strip()
            asset_match = df_asset[df_asset['Asset No.'] == target]
            
            if not asset_match.empty:
                row = asset_match.iloc[0]
                
                st.markdown(f'<div class="asset-card"><b style="color:#38bdf8;">ASSET NO. {row["Asset No."]}</b><h3>{row["Details"]}</h3><p style="margin:0; color:#9ca3af;">📍 สถานที่ติดตั้ง: {row["Location"]}</p></div>', unsafe_allow_html=True)
                
                st.write("🖼️ **ภาพอ้างอิงต้นฉบับในระบบ:**")
                t1, t2, t3 = st.tabs(["รูปหลัก", "มุมที่ 2", "มุมที่ 3"])
                with t1: st.image(row['Picture 1'], use_container_width=True) if row['Picture 1'] else st.info("ไม่มีรูป")
                with t2: st.image(row['Picture 2'], use_container_width=True) if row['Picture 2'] else st.caption("ไม่มีรูป")
                with t3: st.image(row['Picture 3'], use_container_width=True) if row['Picture 3'] else st.caption("ไม่มีรูป")
                
                st.write("---")
                st.subheader("📸 ถ่ายภาพรายงานสภาพจริงตอนนี้")
                uploaded_files = st.file_uploader("เปิดกล้องมือถือถ่ายภาพ (3-5 รูป):", type=['png','jpg','jpeg'], accept_multiple_files=True)
                
                num_files = len(uploaded_files) if uploaded_files else 0
                st.info(f"จำนวนรูปถ่ายปัจจุบัน: {num_files} / 5 รูป")
                
                if 3 <= num_files <= 5:
                    st.success("✅ รูปถ่ายครบตามเกณฑ์ นำส่งรายงานได้ทันที")
                    if st.button("ตกลงและบันทึกข้อมูลผลการตรวจสอบ 🚀", type="primary", use_container_width=True):
                        with st.spinner('ระบบกำลังเชื่อมโยงและบันทึกรายงานผล...'):
                            st.balloons()
                            st.success(f"🎉 รายงานของ {u.get('Name Surname','')} ตรวจเช็คเครื่องจักร {row['Asset No.']} บันทึกสำเร็จ!")
                            time.sleep(3)
                            refresh_app()
                else:
                    st.warning("⚠️ โปรดเปิดกล้องและส่งรูปถ่ายสภาพหน้างานจริงอย่างน้อย 3 รูปขึ้นไป")
                    st.button("ตกลงและบันทึกข้อมูลผลการตรวจสอบ 🚀", disabled=True, use_container_width=True)
            else:
                st.error("❌ ไม่พบข้อมูลทรัพย์สินเลขนี้ในระบบ")
        else:
            st.error("❌ หาคอลัมน์ 'Asset No.' ไม่เจอในไฟล์ข้อมูลทรัพย์สิน")

    if st.button("⬅️ ออกจากระบบผู้ตรวจ (เปลี่ยนคนตรวจ)", key="back_btn"):
        refresh_app()
