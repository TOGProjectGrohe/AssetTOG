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
            # ดึงคอลัมน์ Position มาเก็บไว้ ถ้าไม่มีจะใส่ค่าตั้งต้นเป็น "GL" ตามรูปชีทของพี่
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
    st.write(f"👤 **ผู้บันทึก:** {st.session_state.emp_name} ({st.session_
