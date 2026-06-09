import streamlit as st
import pandas as pd
import requests
from streamlit_qrcode_scanner import qrcode_scanner

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="TOG Asset Audit", page_icon="🕵️‍♂️", layout="centered")

# --- โหลดข้อมูลพนักงานและทรัพย์สิน (CSV) ---
@st.cache_data(ttl=60)
def load_data():
    # ⚠️ ให้พี่เปลี่ยน URL สองลิงก์นี้เป็นลิงก์ CSV ตัวจริงของพี่นะครับ
    emp_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRL_hlhh4MYI3wmq0UserMHRiD7DWID5LsLtWqLCv7aA-N8bSOOvjOy2fSYWXMAzh5BxqfntPqop9Jv/pub?gid=0&single=true&output=csv"
    asset_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTKG0qbzmx-G-7tiRrW1Sv4IgwhBsLjKVEU7SsoMY3ZP2ZjShP3kCL1Ue74C7sZOdATeFtWO-NGbQ4z/pub?gid=0&single=true&output=csv"
    
    df_emp = pd.read_csv(emp_url)
    df_asset = pd.read_csv(asset_url)
    return df_emp, df_asset

try:
    df_emp, df_asset = load_data()
except Exception as e:
    st.error("ไม่สามารถโหลดข้อมูลจาก Google Sheets ได้ กรุณาตรวจสอบลิงก์ CSV")
    st.stop()

# --- บริหารจัดการหน้าจอ (Session State) ---
if "page" not in st.session_state:
    st.session_state.page = 1
if "emp_id" not in st.session_state:
    st.session_state.emp_id = ""
if "emp_name" not in st.session_state:
    st.session_state.emp_name = ""

# รับค่าจาก QR Code ทาง URL (ถ้ามี)
query_params = st.query_params
if "emp_id" in query_params and st.session_state.page == 1:
    st.session_state.emp_id = query_params["emp_id"]

# ==========================================
# 🛑 หน้าที่ 1: สแกนพนักงาน / ยืนยันตัวตน
# ==========================================
if st.session_state.page == 1:
    st.markdown("## 📱 ยืนยันตัวตนผู้ตรวจสอบ")
    
    emp_input = st.text_input("กรอกหรือสแกนรหัสพนักงาน:", value=st.session_state.emp_id)
    
    if emp_input:
        # ค้นหาข้อมูลพนักงาน (สมมติว่าหัวตารางชื่อ ID และ Name)
        user_data = df_emp[df_emp['ID'].astype(str) == str(emp_input)]
        if not user_data.empty:
            st.session_state.emp_id = str(user_data.iloc[0]['ID'])
            st.session_state.emp_name = str(user_data.iloc[0]['Name'])
            
            st.success(f"✅ ตรวจพบข้อมูล: {st.session_state.emp_name}")
            
            if st.button("เข้าสู่หน้าตรวจเช็คทรัพย์สิน ➡️", use_container_width=True):
                st.session_state.page = 2
                st.rerun()
        else:
            st.error("❌ ไม่พบข้อมูลพนักงานรายนี้ในระบบ")

# ==========================================
# 🛑 หน้าที่ 2: สแกน Asset และ ถ่ายรูปคอนเฟิร์ม
# ==========================================
elif st.session_state.page == 2:
    st.markdown("## 🕵️‍♂️ ตรวจสอบสภาพทรัพย์สินหน้างาน")
    st.write(f"👤 **ผู้บันทึก:** {st.session_state.emp_name} ({st.session_state.emp_id})")
    
    st.markdown("---")
    
    # 2. ปุ่มเปิดกล้องสแกน QR Code ของ Asset บนหน้าเว็บทันที ไม่ต้องย่อแอป
    st.markdown("#### 📸 กดปุ่มด้านล่างเพื่อเปิดกล้องสแกน QR ล้อผ้า/Asset")
    scanned_asset_code = qrcode_scanner(key="asset_qrcode_scanner")
    
    # มีช่องพิมพ์แมนนวลเผื่อไว้ให้ด้วย
    asset_input = st.text_input("รหัสทรัพย์สิน (สแกนจากกล้องด้านบน หรือพิมพ์มือ):", value=scanned_asset_code if scanned_asset_code else "")
    
    if asset_input:
        # ค้นหาข้อมูลทรัพย์สิน (สมมติว่าหัวตารางชื่อ Asset_ID และ Asset_Name)
        asset_data = df_asset[df_asset['Asset_ID'].astype(str) == str(asset_input)]
        
        if not asset_data.empty:
            asset_name = asset_data.iloc[0]['Asset_Name']
            st.info(f"📦 **กำลังตรวจสอบ:** {asset_name} (รหัส: {asset_input})")
            
            st.markdown("---")
            st.markdown("#### 📸 ถ่ายภาพคอนเฟิร์มสภาพจริง (อย่างน้อย 3 รูป, ไม่เกิน 5 รูป)")
            
            # สร้างช่องเปิดกล้องถ่ายรูป 5 ช่อง
            img1 = st.camera_input("รูปภาพที่ 1 (จำเป็น)", key="img1")
            img2 = st.camera_input("รูปภาพที่ 2 (จำเป็น)", key="img2")
            img3 = st.camera_input("รูปภาพที่ 3 (จำเป็น)", key="img3")
            img4 = st.camera_input("รูปภาพที่ 4 (ไม่บังคับ)", key="img4")
            img5 = st.camera_input("รูปภาพที่ 5 (ไม่บังคับ)", key="img5")
            
            # นับจำนวนรูปที่ถ่ายจริง
            captured_images = [img for img in [img1, img2, img3, img4, img5] if img is not None]
            st.write(f"📊 ถ่ายแล้ว: {len(captured_images)} / 5 รูป")
            
            # 3 & 4. เงื่อนไขการกดบันทึกข้อมูล (ต้องได้อย่างน้อย 3 รูป ปุ่มถึงจะยอมให้กดได้)
            if len(captured_images) >= 3:
                if st.button("ยอมรับ และบันทึกข้อมูลผลการตรวจสอบ 🚀", type="primary", use_container_width=True):
                    
                    # ⚠️ บันทึกข้อมูล (ส่งค่าไป Google Sheets หรือ Webhook ของพี่ตรงนี้)
                    # ตัวอย่างเช่นส่งหา Google Form หรือชีทแผ่นที่ 2
                    
                    st.success("🎉 บันทึกข้อมูลสำเร็จเรียบร้อย!")
                    
                    # รีเซ็ตค่ากลับมาสแตนบายรอสแกน Asset ชิ้นถัดไปต่อทันที
                    st.rerun()
            else:
                st.warning("⚠️ กรุณาถ่ายรูปให้ครบอย่างน้อย 3 รูปก่อน จึงจะกดปุ่มยอมรับบันทึกข้อมูลได้ครับ")
                st.button("ยอมรับ และบันทึกข้อมูลผลการตรวจสอบ 🚀", disabled=True, use_container_width=True)
        else:
            st.error("❌ ไม่พบรหัสทรัพย์สินนี้ในระบบคลังข้อมูล")
            
    # ปุ่มย้อนกลับไปหน้าแรกเผื่อเปลี่ยนตัวคนตรวจสอบ
    if st.button("⬅️ เปลี่ยนตัวผู้ตรวจสอบ (กลับหน้าแรก)", code="back_btn"):
        st.session_state.page = 1
        st.session_state.emp_id = ""
        st.session_state.emp_name = ""
        st.rerun()
