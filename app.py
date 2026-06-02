import streamlit as st
import pandas as pd

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
    .asset-id { color: #38bdf8; font-size: 14px; font-weight: bold; letter-spacing: 1px; }
    .asset-name { font-size: 28px; font-weight: 700; margin-bottom: 15px; }
    img { border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.4); border: 1px solid rgba(255, 255, 255, 0.1); }
    </style>
""", unsafe_allow_html=True)

# --- 3. ดึงข้อมูลจริงและจัดการแปลงลิงก์รูปภาพอัตโนมัติ ---
@st.cache_data(ttl=5) # ดึงข้อมูลใหม่จาก Google Sheets ทุกๆ 5 วินาที
def load_data():
    def fix_google_drive_link(url):
        if pd.isna(url):
            return ""
        
        # แปลงค่าเป็น String และล้างช่องว่างหัวท้าย
        url_str = str(url).strip()
        
        # 🚨 [ดักจับบั๊กเลข 0] ถ้าในชีทเป็นเลข 0, ค่าว่าง หรือข้อความ nan ให้ตีเป็นค่าว่างทันที
        if url_str == "" or url_str == "0" or url_str == "0.0" or url_str.lower() == "nan":
            return ""
        
        # ค้นหา ID ของรูปภาพจากลิงก์ Google Drive เพื่อแปลงเป็น Direct Link อัตโนมัติ
        if "drive.google.com" in url_str:
            import re
            match = re.search(r'/d/([a-zA-Z0-9-_]+)', url_str)
            if match:
                return f"https://docs.google.com/uc?export=view&id={match.group(1)}"
        
        # ถ้าเป็นลิงก์ทั่วไปที่ขึ้นต้นด้วย http ให้ส่งกลับไปตรงๆ
        if url_str.startswith("http"):
            return url_str
            
        return "" # ถ้าเป็นข้อความอื่นๆ ที่ไม่ใช่ลิงก์ ให้ตีเป็นค่าว่าง

    try:
        # 🚨 [สำคัญที่สุด] นำลิงก์ CSV ที่เพิ่งก๊อปปี้มาล่าสุดสดๆ ร้อนๆ มาวางแทนที่ด้านล่างนี้ครับ
        sheet_url = "นำลิงก์_CSV_ที่ลงท้ายด้วย_pub?output=csv_มาวางตรงนี้"
        
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip() # ล้างช่องว่างหัวตาราง
        
        # แปลงลิงก์รูปภาพทั้งหมดที่มีในตารางให้แสดงผลได้จริง
        for col in ['Picture 1', 'Picture 2', 'Picture 3']:
            if col in df.columns:
                df[col] = df[col].apply(fix_google_drive_link)
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

# --- 4. รับค่าเลข Asset จากกล้องมือถือ ---
query_params = st.query_params
asset_input = query_params.get("asset", None)

# --- 5. แสดงผลบนหน้าจอแอป ---
if asset_input:
    if not df.empty and 'Asset No.' in df.columns:
        # ล้างค่า Asset No. ในตารางให้เป็นข้อความและตัดจุดทศนิยมออกเผื่อ Excel แปลงเลข
        df['Asset No.'] = df['Asset No.'].astype(str).str.strip()
        df['Asset No.'] = df['Asset No.'].apply(lambda x: x.split('.')[0] if '.' in x else x)
        
        # ล้างค่าที่รับมาจากกล้องมือถือ
        target_asset = str(asset_input).strip().split('.')[0]
        result = df[df['Asset No.'] == target_asset]
        
        if not result.empty:
            row = result.iloc[0]
            st.write("### 📦 ข้อมูลทรัพย์สินอุปกรณ์ (TOG)")
            
            # การ์ดข้อมูล
            st.markdown(f"""
                <div class="asset-card">
                    <div class="asset-id">ASSET NO. {row['Asset No.']}</div>
                    <div class="asset-name">{row.get('Details', 'ไม่มีรายละเอียด')}</div>
                    <hr style="opacity: 0.1; margin: 15px 0;">
                    <p style="font-size: 16px; margin: 0;">📍 <b>สถานที่ติดตั้ง:</b> {row.get('Location', 'ไม่ได้ระบุ')}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # แสดงระบบแท็บรูปภาพ 1, 2, 3
            st.write("🖼️ **รูปภาพอุปกรณ์:**")
            tab1, tab2, tab3 = st.tabs(["รูปหลัก", "รูปมุมที่ 2", "รูปมุมที่ 3"])
            
            with tab1:
                if 'Picture 1' in row and row['Picture 1'] != "":
                    st.image(row['Picture 1'], use_container_width=True)
                else: st.info("ไม่มีรูปภาพหลักในระบบ")
            with tab2:
                if 'Picture 2' in row and row['Picture 2'] != "":
                    st.image(row['Picture 2'], use_container_width=True)
                else: st.caption("ไม่ได้ระบุรูปภาพมุมที่ 2")
            with tab3:
                if 'Picture 3' in row and row['Picture 3'] != "":
                    st.image(row['Picture 3'], use_container_width=True)
                else: st.caption("ไม่ได้ระบุรูปภาพมุมที่ 3")
        else:
            st.error(f"❌ ไม่พบข้อมูลรหัสทรัพย์สิน: {asset_input}")
    else:
        st.error("❌ กำลังเชื่อมต่อฐานข้อมูล หรือระบบชื่อคอลัมน์ไม่ถูกต้อง")
else:
    st.title("Asset TOG Scanner")
    st.write("กรุณาสแกน QR Code ประจำอุปกรณ์เพื่อเปิดข้อมูล")
