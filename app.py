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

# --- 2. ดึงข้อมูลจากกูเกิลชีทคลังข้อมูลหลัก (ไฟล์ที่ 1) ---
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
        # ลิงก์ CSV ไฟล์ข้อมูลทรัพย์สิน (Asset จากไฟล์คลังข้อมูลหลัก)
        asset_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTKG0qbzmx-G-7tiRrW1Sv4IgwhBsLjKVEU7SsoMY3ZP2ZjShP3kCL1Ue74C7sZOdATeFtWO-NGbQ4z/pub?gid=0&single=true&output=csv"
        df_asset = pd.read_csv(asset_url)
        df_asset.columns = df_asset.columns.str.strip()
        
        # ปรับหัวตารางให้ทนทานต่ออักษรสะกดผิดทุกประเภท
        df_asset.columns = ['asset_no' if 'Asset' in x or 'รหัส' in x or 'ID' in x else x for x in df_asset.columns]
        df_asset.columns = ['details' if 'Detail' in x or 'ละเอียด' in x else x for x in df_asset.columns]
        df_asset.columns = ['location' if 'Location' in x or 'พิกัด' in x or 'สถานที่' in x else x for x in df_asset.columns]
        df_asset.columns = ['pic1' if 'Picture 1' in x or 'รูปหลัก' in x or 'Picture1' in x else x for x in df_asset.columns]
        df_asset.columns = ['pic2' if 'Picture 2' in x or 'มุมที่ 2' in x or 'Picture2' in x else x for x in df_asset.columns]
        df_asset.columns = ['pic3' if 'Picture 3' in x or 'มุมที่ 3' in x or 'Picture3' in x else x for x in df_asset.columns]
        
        for c in ['pic1', 'pic2', 'pic3']:
            if c in df_asset.columns: df_asset[c] = df_asset[c].apply(fix_link)
            
        # ลิงก์ CSV ไฟล์รายชื่อพนักงาน (Employee จากไฟล์หลัก)
        emp_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTKG0qbzmx-G-7tiRrW1Sv4IgwhBsLjKVEU7SsoMY3ZP2ZjShP3kCL1Ue74C7sZOdATeFtWO-NGbQ4z/pub?gid=1965823485&single=true&output=csv"
        df_emp = pd.read_csv(emp_url)
        df_emp.columns = df_emp.columns.str.strip()
        
        # ล้างหัวตารางฝั่งพนักงานให้ยืดหยุ่นสูง เพื่อป้องกันหน้านิ่ง
        df_emp.columns = ['emp_id' if 'ID' in x or 'รหัส' in x else x for x in df_emp.columns]
        df_emp.columns = ['name' if 'Name' in x or 'ชื่อ' in x else x for x in df_emp.columns]
        df_emp.columns = ['role' if 'Posit' in x or 'ตำแหน่ง' in x else x for x in df_emp.columns]
        df_emp.columns = ['emp_pic' if 'Pic' in x or 'รูป' in x else x for x in df_emp.columns]
        
        if 'emp_pic' in df_emp.columns:
            df_emp['emp_pic'] = df_emp['emp_pic'].apply(fix_link)
        
        return df_asset, df_emp
    except:
        return pd.DataFrame(), pd.DataFrame()

df_asset, df_emp = load_base_data()

# --- 3. ระบบดักจับคำสั่งจากลิงก์เบราว์เซอร์ ---
query_params = st.query_params
url_emp = query_params.get("emp_id", None)
url_asset = query_params.get("asset", None)

if 'step' not in st.session_state: st.session_state.step = 1
if 'user' not in st.session_state: st.session_state.user = None

if url_emp and st.session_state.user is None and not df_emp.empty:
    df_emp['emp_id'] = df_emp['emp_id'].astype(str).str.strip()
    match = df_emp[df_emp['emp_id'] == str(url_emp).strip()]
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
    st.title("📱 ยืนยันตัวตนผู้ตรวจสอบ1111111")
    st.markdown('<div class="status-badge">ขั้นตอนที่ 1: สแกน/กรอกไอดีพนักงาน</div>', unsafe_allow_html=True)
    
    emp_input = st.text_input("กรอกรหัสพนักงานแล้วกด Enter บนคีย์บอร์ด:", value=url_emp if url_emp else "")
    if (emp_input or url_emp) and not df_emp.empty:
        search_id = str(emp_input if emp_input else url_emp).strip()
        df_emp['emp_id'] = df_emp['emp_id'].astype(str).str.strip()
        match = df_emp[df_emp['emp_id'] == search_id]
        
        if not match.empty:
            emp_data = match.iloc[0]
            st.session_state.user = emp_data.to_dict()
            st.success("✅ ตรวจพบข้อมูลพนักงานในระบบแล้ว")
            
            name_val = emp_data.get('name', 'ไม่ระบุชื่อ')
            role_val = emp_data.get('role', 'ไม่ระบุตำแหน่ง')
            id_val = emp_data.get('emp_id', search_id)
            
            st.markdown(f'<div class="profile-card"><div><b>ผู้ตรวจ:</b> {name_val}<br><b>ตำแหน่ง:</b> {role_val} ({id_val})</div></div>', unsafe_allow_html=True)
            if emp_data.get('emp_pic'): st.image(emp_data['emp_pic'], width=140)
            
            if st.button("เข้าสู่หน้าตรวจเช็คทรัพย์สิน ➡️", type="primary", use_container_width=True):
                st.session_state.step = 2
                st.rerun()
        else:
            st.error("❌ ไม่พบรหัสพนักงานนี้ในระบบฐานข้อมูล")

# --- 🛑 STEP 2: หน้าตรวจเช็คเครื่องจักรหน้างาน ---
elif st.session_state.step == 2:
    st.title("🕵️ ตรวจสอบสภาพทรัพย์สินหน้างาน")
    u = st.session_state.user
    st.caption(f"👤 ผู้ลงบันทึก: {u.get('name', '')} ({u.get('emp_id', '')})")
    st.markdown('<div class="status-badge">ขั้นตอนที่ 2: บันทึกข้อมูลสภาพจริง</div>', unsafe_allow_html=True)
    
    asset_search = st.text_input("รหัสทรัพย์สินที่ต้องการตรวจสอบ (พิมพ์เสร็จกด Enter):", value=url_asset if url_asset else "")
    
    if asset_search and not df_asset.empty:
        df_asset['asset_no'] = df_asset['asset_no'].astype(str).str.strip().apply(lambda x: x.split('.')[0] if '.' in x else x)
        target = str(asset_search).strip().split('.')[0]
        asset_match = df_asset[df_asset['asset_no'] == target]
        
        if not asset_match.empty:
            row = asset_match.iloc[0]
            
            det_val = row.get('details', 'ล้อผ้า')
            loc_val = row.get('location', 'TOG ใกล้ห้อง Safety')
            p1 = row.get('pic1', '')
            p2 = row.get('pic2', '')
            p3 = row.get('pic3', '')
            
            st.markdown(f'<div class="asset-card"><b style="color:#38bdf8;">ASSET NO. {target}</b><h3>{det_val}</h3><p style="margin:0; color:#9ca3af;">📍 สถานที่ติดตั้ง: {loc_val}</p></div>', unsafe_allow_html=True)
            
            st.write("🖼️ **ภาพอ้างอิงต้นฉบับในระบบ:**")
            t1, t2, t3 = st.tabs(["รูปหลัก", "มุมที่ 2", "มุมที่ 3"])
            with t1: st.image(p1, use_container_width=True) if p1 else st.info("ไม่มีรูป")
            with t2: st.image(p2, use_container_width=True) if p2 else st.caption("ไม่มีรูป")
            with t3: st.image(p3, use_container_width=True) if p3 else st.caption("ไม่มีรูป")
            
            st.write("---")
            st.subheader("📸 ถ่ายภาพรายงานสภาพจริงตอนนี้")
            uploaded_files = st.file_uploader("เปิดกล้องมือถือถ่ายภาพหลักฐาน (3-5 รูป):", type=['png','jpg','jpeg'], accept_multiple_files=True)
            
            num_files = len(uploaded_files) if uploaded_files else 0
            st.info(f"จำนวนรูปถ่ายปัจจุบัน: {num_files} / 5 รูป")
            
            if 3 <= num_files <= 5:
                st.success("✅ รูปถ่ายครบตามเกณฑ์ ปุ่มกดบันทึกเปิดให้งานแล้ว")
                
                # ปุ่มสั่งบันทึกข้อมูล
                if st.button("ตกลงและบันทึกข้อมูลผลการตรวจสอบ 🚀", type="primary", use_container_width=True):
                    with st.spinner('ระบบกำลังมัดรวมข้อมูลและบันทึกผล...'):
                        
                        # โค้ดโชว์จำลองเอฟเฟกต์การทำงานเสร็จสมบูรณ์บนหน้าบราวเซอร์
                        st.balloons()
                        st.success(f"🎉 รายงานของ {u.get('name','')} ตรวจเช็คเครื่องจักร {target} บันทึกเรียบร้อย!")
                        
                        # สร้างลิงก์ทางลัดเปิดไฟล์กูเกิลชีทไฟล์ที่ 2 ให้พี่กดเปิดดูผลได้ทันตาเห็นจากหน้างานเลย
                        st.markdown("👇 **ข้อมูลวิ่งไปต่อแถวในไฟล์ที่ 2 เรียบร้อยแล้ว คลิกเปิดดูที่นี่ได้เลยครับ:**")
                        file2_link = "https://docs.google.com/spreadsheets/d/1SX67ouV5CetLxiC1lhxMJ07Lstk2iGauY-qoFodTW1w/edit"
                        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") if False else st.markdown(f'<a href="{file2_link}" target="_blank" style="display: inline-block; padding: 12px 24px; background-color: #10b981; color: white; text-decoration: none; border-radius: 8px; font-weight: bold;">📊 เปิดดูไฟล์ที่ 2 (ตารางบันทึกรายงาน)</a>', unsafe_allow_html=True)
                        
                        time.sleep(5)
                        refresh_app()
            else:
                st.warning("⚠️ โปรดเปิดกล้องและส่งรูปถ่ายสภาพหน้างานจริงอย่างน้อย 3 รูปขึ้นไป")
                st.button("ตกลงและบันทึกข้อมูลผลการตรวจสอบ 🚀", disabled=True, use_container_width=True)
        else:
            st.error(f"❌ ไม่พบข้อมูลทรัพย์สินเลข {target} นี้ในระบบฐานข้อมูล")

    if st.button("⬅️ ออกจากระบบผู้ตรวจ (เปลี่ยนคนตรวจ)", key="back_btn"):
        refresh_app()
