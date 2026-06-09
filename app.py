import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import pytz
import base64
# ดึงระบบกล้องสแกน QR มาทำงานร่วมกับหน้าเว็บ
from streamlit_qrcode_scanner import qrcode_scanner

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="TOG Asset Audit", page_icon="🕵️‍♂️", layout="centered")

# --- โหลดข้อมูลพนักงานและทรัพย์สิน (CSV) ---
@st.cache_data(ttl=60)
def load_data():
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
if "emp_position" not in st.session_state:
    st.session_state.emp_position = ""
if "scanned_asset" not in st.session_state:
    st.session_state.scanned_asset = ""

# รับค่าจาก URL ทางคิวอาร์พนักงานตัวแรก (ถ้ามี)
query_params = st.query_params
if "emp_id" in query_params and st.session_state.page == 1:
    st.session_state.emp_id = query_params["emp_id"]

# ==========================================
# 🛑 หน้าที่ 1: ยืนยันตัวตนผู้ตรวจสอบ (+ โชว์รูปน้องแมว/พนักงาน)
# ==========================================
if st.session_state.page == 1:
    st.markdown("## 📱 ยืนยันตัวตนผู้ตรวจสอบ")
    emp_input = st.text_input("กรอกหรือสแกนรหัสพนักงาน:", value=st.session_state.emp_id)
    
    if emp_input:
        user_data = df_emp[df_emp['ID'].astype(str).str.strip() == str(emp_input).strip()]
        if not user_data.empty:
            st.session_state.emp_id = str(user_data.iloc[0]['ID'])
            st.session_state.emp_name = str(user_data.iloc[0]['Name'])
            st.session_state.emp_position = str(user_data.iloc[0]['Position']) if 'Position' in user_data.columns else "GL"
            
            st.success(f"✅ ตรวจพบข้อมูล: {st.session_state.emp_name}")
            
            if 'Picture GL' in user_data.columns and pd.notna(user_data.iloc[0]['Picture GL']):
                st.image(user_data.iloc[0]['Picture GL'], caption=f"รูปโปรไฟล์: {st.session_state.emp_name}", width=200)
            
            if st.button("เข้าสู่หน้าตรวจเช็คทรัพย์สิน ➡️", use_container_width=True):
                st.session_state.page = 2
                st.rerun()
        else:
            st.error("❌ ไม่พบข้อมูลพนักงานรายนี้ในระบบ (ตรวจสอบชื่อคอลัมน์ ID ใน Sheet)")

# ==========================================
# 🛑 หน้าที่ 2: กดเปิดกล้องสแกน Asset หน้างานจริง (+ บันทึกข้อมูลส่งชีท)
# ==========================================
elif st.session_state.page == 2:
    st.markdown("## 🕵️‍♂️ ตรวจสอบสภาพทรัพย์สินหน้างาน")
    
    # 🛠️ แก้ไขบรรทัดนี้ใหม่ให้สั้น กระชับ แข็งแรง ไม่ขาด ไม่หลุดปีกกาแน่นอนครับพี่!
    info_text = f"👤 **ผู้บันทึก:** {st.session_state.emp_name} ({st.session_state.emp_id}) | 🛠️ **ตำแหน่ง:** {st.session_state.emp_position}"
    st.write(info_text)
    st.markdown("---")
    
    if not st.session_state.scanned_asset:
        st.markdown("#### 📸 เปิดกล้องยิงคิวอาร์โค้ดล้อผ้าตรงนี้")
        camera_code = qrcode_scanner(key="asset_qrcode_scanner")
        
        if camera_code:
            actual_code = str(camera_code).strip()
            if "asset=" in actual_code:
                st.session_state.scanned_asset = actual_code.split("asset=")[-1]
            else:
                st.session_state.scanned_asset = actual_code
            st.rerun()
            
    asset_input = st.text_input("รหัสล้อผ้าที่ระบบจับได้ (หรือพิมพ์มือ):", value=st.session_state.scanned_asset)
    
    if asset_input:
        st.session_state.scanned_asset = asset_input
        
        df_asset['Asset_ID_Str'] = df_asset['Asset_ID'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
        search_value = str(asset_input).strip().split('.')[0]
        
        asset_data = df_asset[df_asset['Asset_ID_Str'] == search_value]
        
        if not asset_data.empty:
            asset_name = asset_data.iloc[0]['Asset_Name']
            asset_location = asset_data.iloc[0]['Location'] if 'Location' in asset_data.columns else "ไม่ระบุตำแหน่ง"
            
            st.info(f"🔎 **ตรวจพบข้อมูล:** {asset_name} (รหัส: {asset_input})")
            st.caption(f"📍 **พิกัดคลัง:** {asset_location}")
            
            st.markdown("##### 🖼️ รูปล้อผ้าอ้างอิงในคลังปัจจุบัน:")
            col1, col2, col3 = st.columns(3)
            with col1:
                if 'Picture 1' in asset_data.columns and pd.notna(asset_data.iloc[0]['Picture 1']) and str(asset_data.iloc[0]['Picture 1']).strip() != "":
                    st.image(asset_data.iloc[0]['Picture 1'], caption="รูปอ้างอิงที่ 1", use_container_width=True)
            with col2:
                if 'Picture 2' in asset_data.columns and pd.notna(asset_data.iloc[0]['Picture 2']) and str(asset_data.iloc[0]['Picture 2']).strip() != "":
                    st.image(asset_data.iloc[0]['Picture 2'], caption="รูปอ้างอิงที่ 2", use_container_width=True)
            with col3:
                if 'Picture 3' in asset_data.columns and pd.notna(asset_data.iloc[0]['Picture 3']) and str(asset_data.iloc[0]['Picture 3']).strip() != "":
                    st.image(asset_data.iloc[0]['Picture 3'], caption="รูปอ้างอิงที่ 3", use_container_width=True)
            
            if st.button("🔄 เคลียร์ค่าเพื่อเปิดกล้องสแกนชิ้นใหม่"):
                st.session_state.scanned_asset = ""
                st.rerun()
                
            st.markdown("---")
            st.markdown("#### 📸 ถ่ายภาพคอนเฟิร์มสภาพจริง (อย่างน้อย 3 รูป, ไม่เกิน 5 รูป)")
            
            img1 = st.camera_input("รูปภาพที่ 1 (จำเป็น)", key="img1")
            img2 = st.camera_input("รูปภาพที่ 2 (จำเป็น)", key="img2")
            img3 = st.camera_input("รูปภาพที่ 3 (จำเป็น)", key="img3")
            img4 = st.camera_input("รูปภาพที่ 4 (ไม่บังคับ)", key="img4")
            img5 = st.camera_input("รูปภาพที่ 5 (ไม่บังคับ)", key="img5")
            
            captured_images = [img1, img2, img3, img4, img5]
            valid_imgs = [img for img in captured_images if img is not None]
            st.write(f"📊 ถ่ายแล้ว: {len(valid_imgs)} / 5 รูป")
            
            if len(valid_imgs) >= 3:
                if st.button("ยอมรับ และบันทึกข้อมูลผลการตรวจสอบ 🚀", type="primary", use_container_width=True):
                    with st.spinner("⏳ กำลังบันทึกเวลาปัจจุบันและยิงรูปเข้าคลังไฟล์ระบบ..."):
                        
                        # 1. 🕒 สร้างค่าเวลาบันทึกปัจจุบันแบบโซนประเทศไทย (GMT+7)
                        tz_thai = pytz.timezone('Asia/Bangkok')
                        current_time = datetime.now(tz_thai).strftime('%Y-%m-%d %H:%M:%S')
                        
                        # 2. 📦 แพ็คข้อมูลข้อความตามที่พี่กำหนด
                        payload = {
                            "timestamp": current_time,
                            "emp_id": st.session_state.emp_id,
                            "emp_name": st.session_state.emp_name,
                            "emp_position": st.session_state.emp_position,
                            "asset_id": str(asset_input)
                        }
                        
                        # 3. 🖼️ แปลงไฟล์รูปภาพเป็น Base64 ส่งเข้าไปพร้อมข้อมูลข้อความ
                        for idx, img in enumerate(captured_images, start=1):
                            if img is not None:
                                img_bytes = img.getvalue()
                                base64_str = "data:image/jpeg;base64," + base64.b64encode(img_bytes).decode('utf-8')
                                payload[f"img{idx}"] = base64_str
                        
                        # 4. 🚀 ลิงก์ Google Apps Script ตัวจริงที่เซฟไว้ของพี่ครับ
                        webhook_url = "https://script.google.com/macros/s/AKfycbzpuNGfuWL5YvfsL0a3YrDkdDR2wVGtCl8GF7gtQmbjmiJubeucJQ3p7Dsrh-KRZLptIA/exec"
                        
                        try:
                            response = requests.post(webhook_url, data=payload)
                            
                            if response.status_code == 200:
                                st.success(f"🎉 บันทึกสำเร็จ ณ เวลา: {current_time} ลิงก์รูปและประวัติพุ่งตรงเข้าชีทแผ่น Audit_Log แล้ว!")
                                st.session_state.scanned_asset = ""
                                st.rerun()
                            else:
                                st.error(f"❌ ระบบส่งข้อมูลล้มเหลว (เกิดข้อผิดพลาดจากฝั่งเซอร์เวอร์: {response.status_code})")
                        except Exception as ex:
                            st.error(f"❌ ไม่สามารถติดต่อคลังชีทได้ กรุณาตรวจสอบลิงก์ Apps Script: {ex}")
            else:
                st.warning("⚠️ กรุณาถ่ายรูปให้ครบอย่างน้อย 3 รูปก่อน จึงจะกดปุ่มบันทึกได้ครับ")
                st.button("ยอมรับ และบันทึกข้อมูลผลการตรวจสอบ 🚀", disabled=True, use_container_width=True)
                
    if st.button("⬅️ เปลี่ยนตัวผู้ตรวจสอบ (กลับหน้าแรก)"):
        st.session_state.page = 1
        st.session_state.emp_id = ""
        st.session_state.emp_name = ""
        st.session_state.scanned_asset = ""
        st.rerun()
