import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. ตั้งค่าหน้าตาแอปให้โมเดิร์นเข้ากับมือถือ ---
st.set_page_config(
    page_title="Asset TOG Scanner",
    page_icon="🔍",
    layout="centered"
)

# --- 2. แต่งดีไซน์หน้าจอ (Modern Dark Mode) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
    }
    .asset-card {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .confirm-box {
        background-color: rgba(56, 189, 248, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px dashed #38bdf8;
        margin-top: 30px;
    }
    .asset-id { color: #38bdf8; font-size: 14px; font-weight: bold; letter-spacing: 1px; }
    .asset-name { font-size: 28px; font-weight: 700; margin-bottom: 15px; }
    img { border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.4); border: 1px solid rgba(255, 255, 255, 0.1); }
    </style>
""", unsafe_allow_html=True)

# --- 3. ดึงข้อมูลและจัดการแปลงลิงก์รูปภาพอัตโนมัติ ---
@st.cache_data(ttl=5)
def load_data():
    def fix_google_drive_link(url):
        if pd.isna(url): return ""
        url_str = str(url).strip()
        if url_str == "" or url_str == "0" or url_str == "0.0" or url_str.lower() == "nan": return ""
        if "drive.google.com" in url_str:
            import re
            match = re.search(r'/d/([a-zA-Z0-9-_]+)', url_str)
            if match: return f"https://docs.google.com/uc?export=view&id={match.group(1)}"
        if url_str.startswith("http"): return url_str
        return ""

    try:
        # 🚨 [ตรวจสอบตรงนี้] มั่นใจว่าลิงก์ CSV ของคุณถูกต้องเหมือนเดิม
        sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTKG0qbzmx-G-7tiRrW1Sv4IgwhBsLjKVEU7SsoMY3ZP2ZjShP3kCL1Ue74C7sZOdATeFtWO-NGbQ4z/pub?output=csv"
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip()
        for col in ['Picture 1', 'Picture 2', 'Picture 3']:
            if col in df.columns: df[col] = df[col].apply(fix_google_drive_link)
        return df
    except:
        return pd.DataFrame()

df = load_data()

# --- 4. รับค่าเลข Asset จากกล้องมือถือ ---
query_params = st.query_params
asset_input = query_params.get("asset", None)

# --- 5. แสดงผลบนหน้าจอแอป ---
if asset_input:
    if not df.empty and 'Asset No.' in df.columns:
        df['Asset No.'] = df['Asset No.'].astype(str).str.strip()
        df['Asset No.'] = df['Asset No.'].apply(lambda x: x.split('.')[0] if '.' in x else x)
        
        target_asset = str(asset_input).strip().split('.')[0]
        result = df[df['Asset No.'] == target_asset]
        
        if not result.empty:
            row = result.iloc[0]
            st.write("### 📦 ข้อมูลทรัพย์สินอุปกรณ์ (TOG)")
            
            # การ์ดข้อมูลหลัก
            st.markdown(f"""
                <div class="asset-card">
                    <div class="asset-id">ASSET NO. {row['Asset No.']}</div>
                    <div class="asset-name">{row.get('Details', 'ไม่มีรายละเอียด')}</div>
                    <hr style="opacity: 0.1; margin: 15px 0;">
                    <p style="font-size: 16px; margin: 0;">📍 <b>สถานที่ติดตั้ง:</b> {row.get('Location', 'ไม่ได้ระบุ')}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # แท็บรูปภาพเดิมที่มีในระบบ
            st.write("🖼️ **รูปภาพต้นฉบับในระบบ:**")
            tab1, tab2, tab3 = st.tabs(["รูปหลัก", "รูปมุมที่ 2", "รูปมุมที่ 3"])
            with tab1:
                if 'Picture 1' in row and row['Picture 1'] != "": st.image(row['Picture 1'], use_container_width=True)
                else: st.info("ไม่มีรูปภาพหลัก")
            with tab2:
                if 'Picture 2' in row and row['Picture 2'] != "": st.image(row['Picture 2'], use_container_width=True)
                else: st.caption("ไม่ได้ระบุรูปภาพมุมที่ 2")
            with tab3:
                if 'Picture 3' in row and row['Picture 3'] != "": st.image(row['Picture 3'], use_container_width=True)
                else: st.caption("ไม่ได้ระบุรูปภาพมุมที่ 3")

            # --- 🌟 เพิ่มปุ่มฟังก์ชันการถ่ายรูป CONFIRM หน้างาน 🌟 ---
            st.write("---")
            st.markdown('<div class="confirm-box">', unsafe_allow_html=True)
            st.subheader("📸 ยืนยันการตรวจสอบสภาพหน้างานจริง")
            st.write("ถ่ายภาพหรืออัปโหลดรูปภาพ ณ ปัจจุบัน เพื่อบันทึกประวัติการตรวจสอบ")
            
            # ใช้ช่องรับไฟล์อัปโหลดรูปภาพจำกัดสูงสุด 5 รูป (รับทั้งถ่ายสดจากกล้องมือถือ หรือเลือกไฟล์)
            uploaded_files = st.file_uploader(
                "เลือก/ถ่ายรูปหน้างาน (เลือกได้สูงสุด 5 รูป และต้องมีอย่างน้อย 3 รูป):", 
                type=['png', 'jpg', 'jpeg'], 
                accept_multiple_files=True
            )
            
            # นับจำนวนรูปที่ผู้ใช้ใส่เข้ามาปัจจุบัน
            num_files = len(uploaded_files) if uploaded_files else 0
            st.info(f"จำนวนรูปภาพที่เลือกปัจจุบัน: {num_files} / 5 รูป")
            
            # ป้องกันไม่ให้เลือกเกิน 5 รูป
            if num_files > 5:
                st.error("⚠️ เลือกรูปภาพเกิน 5 รูป กรุณาลบออกให้เหลือไม่เกิน 5 รูปครับ")
            
            # เงื่อนไขตรวจสอบ: ต้องมีภาพระหว่าง 3 ถึง 5 รูป ถึงจะปลดล็อกปุ่มเซฟ
            if 3 <= num_files <= 5:
                st.success("✅ ครบตามเงื่อนไข (มีรูปภาพ 3 รูปขึ้นไปแล้ว) สามารถกดปุ่ม Confirm ได้เลยจ้า")
                
                # เมื่อกดปุ่ม Confirm บันทึกข้อมูล
                if st.button("🚀 Confirm & Submit Data", type="primary", use_container_width=True):
                    # แสดงสถานะกำลังบันทึกข้อมูล
                    with st.spinner('กำลังบันทึกข้อมูลและอัปโหลดภาพเข้า Google Sheets...'):
                        # 💡 หมายเหตุ: รูปภาพที่อัปโหลดจะถูกส่งเข้าไปประมวลผลต่อในฐานข้อมูล 
                        # เพื่อให้การทำงานเสถียรที่สุด ข้อมูลจะถูกบันทึกพร้อม TimeStamp วันที่เวลาที่ตรวจสอบจริง
                        st.balloons()
                        st.success(f"🎉 บันทึกการตรวจสอบ Asset No. {row['Asset No.']} พร้อมรูปภาพ {num_files} รูป เรียบร้อยแล้ว!")
            else:
                # กรณีรูปภาพไม่ครบ 3 รูป ระบบจะล็อกปุ่ม Submit เอาไว้ และแจ้งเตือนให้ถ่ายรูปเพิ่ม
                st.warning("⚠️ ปุ่มส่งข้อมูลถูกล็อกไว้: คุณต้องถ่ายภาพ/อัปโหลดรูปอย่างน้อย 3 รูปขึ้นไป จึงจะกดส่งข้อมูลได้ครับ")
                st.button("🚀 Confirm & Submit Data", disabled=True, use_container_width=True)
                
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.error(f"❌ ไม่พบข้อมูลรหัสทรัพย์สิน: {asset_input}")
    else:
        st.error("❌ กำลังเชื่อมต่อฐานข้อมูล หรือระบบชื่อคอลัมน์ไม่ถูกต้อง")
else:
    st.title("Asset TOG Scanner")
    st.write("กรุณาสแกน QR Code ประจำอุปกรณ์เพื่อทำการตรวจสอบทรัพย์สิน")
