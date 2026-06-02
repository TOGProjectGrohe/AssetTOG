import streamlit as st
import pandas as pd

# --- 1. ตั้งค่าหน้าตาแอปให้โมเดิร์น (เข้ากับมือถือ iPhone/Android) ---
st.set_page_config(
    page_title="Asset TOG Scanner",
    page_icon="🔍",
    layout="centered"
)

# --- 2. แต่งหน้าตาด้วย CSS (Dark Mode สุดหรู ไม่โบราณ) ---
st.markdown("""
    <style>
    /* พื้นหลังไล่เฉดสีน้ำเงินเข้ม-ดำ */
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
    }
    /* การ์ดมนกระจกฝ้าแสดงข้อมูลทรัพย์สิน */
    .asset-card {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .asset-id {
        color: #38bdf8;
        font-size: 14px;
        font-weight: bold;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    .asset-name {
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 15px;
    }
    /* สไตล์รูปภาพให้ขอบมนและดูเด่น */
    img {
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. ดึงข้อมูลจริงจากตารางของคุณ ---
@st.cache_data
def load_data():
    # 📌 เคล็ดลับเด็ด: ฟังก์ชันแปลงลิงก์รูปภาพ Google Drive อัตโนมัติให้ Python แสดงผลได้
    def fix_google_drive_link(url):
        if pd.isna(url) or not isinstance(url, str):
            return ""
        if "drive.google.com" in url:
            # ดึง ID ของไฟล์ออกมาจากลิงก์
            parts = url.split('/')
            for i, part in enumerate(parts):
                if part == 'd' and i + 1 < len(parts):
                    file_id = parts[i+1].split('?')[0]
                    return f"http://googleusercontent.com/profile/picture/3"
        return url

    # โหลดข้อมูลจาก Google Sheets (ใส่ลิงก์ของคุณแทนที่ด้านล่างนี้ได้เลย)
    try:
        # ⚠️ ถ้ารันครั้งแรกเพื่อทดสอบ ให้ใส่ลิงก์ Google Sheets CSV ของคุณตรงนี้
        # แต่เพื่อความง่ายในการทดสอบรอบแรก โค้ดนี้จะจำลองข้อมูลจากภาพของคุณให้ก่อนครับ
        data = {
            'Asset No.': ['11450345'],
            'Details': ['ล้อผ้า'],
            'Location': ['TOG ใกล้ห้อง Safety'],
            'Picture 1': ['https://lh3.googleusercontent.com/d/12fQyueVerMwwqwWUZlYtiVeM7_8lttK4'],
            'Picture 2': [''],
            'Picture 3': ['']
        }
        df = pd.DataFrame(data)
        
        # ปรับปรุงลิงก์รูปภาพอัตโนมัติ
        df['Picture 1'] = df['Picture 1'].apply(fix_google_drive_link)
        df['Picture 2'] = df['Picture 2'].apply(fix_google_drive_link)
        df['Picture 3'] = df['Picture 3'].apply(fix_google_drive_link)
        
        return df
    except:
        return pd.DataFrame()

df = load_data()

# --- 4. ตรวจสอบค่าจากกล้องมือถือที่สแกน QR Code เข้ามา ---
query_params = st.query_params
asset_input = query_params.get("asset", None)

# --- 5. การแสดงผลบนหน้าจอมือถือ ---
if asset_input:
    # ค้นหาข้อมูลจาก Asset No. (ล้างค่าว่างเพื่อความแม่นยำ)
    df['Asset No.'] = df['Asset No.'].astype(str).str.strip()
    result = df[df['Asset No.'] == str(asset_input).strip()]
    
    if not result.empty:
        row = result.iloc[0]
        
        st.write("### 📦 ข้อมูลทรัพย์สินอุปกรณ์ (TOG)")
        
        # การ์ดแสดงรายละเอียด
        st.markdown(f"""
            <div class="asset-card">
                <div class="asset-id">ASSET NO. {row['Asset No.']}</div>
                <div class="asset-name">{row['Details']}</div>
                <hr style="opacity: 0.1; margin: 15px 0;">
                <p style="font-size: 16px; margin: 0;">📍 <b>สถานที่ติดตั้ง:</b> {row['Location']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # แสดงรูปภาพแบบ Tabs เผื่อมีรูปเพิ่มในอนาคต
        st.write("🖼️ **รูปภาพอุปกรณ์:**")
        tab1, tab2, tab3 = st.tabs(["รูปหลัก", "รูปมุมที่ 2", "รูปมุมที่ 3"])
        
        with tab1:
            if row['Picture 1']:
                st.image(row['Picture 1'], use_container_width=True)
            else:
                st.info("ไม่มีรูปภาพหลักในระบบ")
        with tab2:
            if row['Picture 2']:
                st.image(row['Picture 2'], use_container_width=True)
            else:
                st.caption("ไม่ได้ระบุรูปภาพมุมที่ 2")
        with tab3:
            if row['Picture 3']:
                st.image(row['Picture 3'], use_container_width=True)
            else:
                st.caption("ไม่ได้ระบุรูปภาพมุมที่ 3")
                
    else:
        st.error(f"❌ ไม่พบข้อมูลรหัสทรัพย์สิน: {asset_input}")
        if st.button("กลับหน้าหลัก"):
            st.query_params.clear()
            st.rerun()
else:
    # หน้าแรกกรณีที่เปิดแอปธรรมดาโดยไม่ได้สแกนคิวอาร์โค้ด
    st.markdown("<div style='text-align: center; padding-top: 30px;'>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2530/2530010.png", width=90)
    st.title("Asset TOG Scanner")
    st.write("สแกน QR Code ประจำอุปกรณ์เพื่อตรวจสอบข้อมูลทรัพย์สิน")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ช่องค้นหาเผื่อพิมพ์เองด้วยมือ
    manual_id = st.text_input("หรือพิมพ์เลข Asset No. เองที่นี่:", placeholder="เช่น 11450345")
    if st.button("🔍 ค้นหาข้อมูล"):
        if manual_id:
            st.query_params.asset = manual_id
            st.rerun()
