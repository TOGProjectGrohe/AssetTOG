import streamlit as st
import pandas as pd
import plotly.express as px

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="TOG Improvement Dashboard", layout="wide")
st.title("📊 โปรแกรมตรวจสอบ Improvement AT TOG")

# 1. ฟังก์ชันดึงข้อมูลจาก Google Sheet (ดึงสดผ่าน URL สาธารณะ)
@st.cache_data(ttl=60) # อัปเดตข้อมูลใหม่ทุกๆ 1 นาที
def load_data():
    # เปลี่ยนลิงก์ Google Sheet ของคุณให้กลายเป็นลิงก์ดาวน์โหลด CSV
    sheet_id = "1jL7baZKeeuAmuQUCWuEN7cqjya9HoZjCi9riD6DUnB8"
    gid = "0"
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    
    # อ่านข้อมูลเข้า pandas DataFrame
    df = pd.read_csv(csv_url)
    return df

# โหลดข้อมูล
try:
    df = load_data()
    st.sidebar.success("เชื่อมต่อ Google Sheet สำเร็จ!")
except Exception as e:
    st.sidebar.error(f"ไม่สามารถดึงข้อมูลได้: {e}")
    df = pd.DataFrame()

# ตรวจสอบว่าใน Sheet มีข้อมูลไหม
if not df.empty:
    
    # สร้างเมนูเปลี่ยนหน้าด้านข้าง (Sidebar)
    menu = st.sidebar.radio("เมนูการใช้งาน", ["ภาพรวม Dashboard", "เพิ่ม Improvement", "สแกน QR Code"])

    # ---------------- หน้าที่ 1 & 3: ภาพรวม Dashboard & กราฟ 1-10 ----------------
    if menu == "ภาพรวม Dashboard":
        st.subheader("📋 ภาพรวม และ อันดับ Improvement 1-10")
        
        # สมมติว่าใน Sheet ของคุณมีคอลัมน์ชื่อ 'หัวข้อ' และ 'คะแนน' หรือ 'จำนวน' 
        # (คุณสามารถเปลี่ยนชื่อคอลัมน์ให้ตรงกับไฟล์จริงของคุณได้เลยครับ)
        col_name = df.columns[0]  # คอลัมน์แรก (สมมติว่าเป็นชื่อรายการ)
        col_value = df.columns[1] if len(df.columns) > 1 else df.columns[0] # คอลัมน์สอง (สมมติว่าเป็นตัวเลข)
        
        # จัดอันดับ 1-10
        top_10 = df.sort_values(by=col_value, ascending=False).head(10)
        
        # แบ่งหน้าจอเป็น 2 คอลัมน์สำหรับโชว์กราฟแท่งและวงกลมคู่กัน
        c1, c2 = st.columns(2)
        
        with c1:
            fig_bar = px.bar(top_10, x=col_name, y=col_value, 
                             title=f"กราฟแท่งแสดงอันดับ 1-10 (อิงตาม {col_value})",
                             color=col_value, color_continuous_scale="Viridis")
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with c2:
            fig_pie = px.pie(top_10, names=col_name, values=col_value, 
                             title=f"กราฟวงกลมแสดงสัดส่วนอันดับ 1-10")
            st.plotly_chart(fig_pie, use_container_width=True)
            
        st.markdown("---")
        
        # ---------------- ข้อ 4: ดูกราฟและภาพ Before & After ย้อนหลัง ----------------
        st.subheader("🔍 4. ดูภาพ Before & After ย้อนหลัง")
        
        selected_item = st.selectbox("เลือกรายการ Improvement ที่ต้องการดูย้อนหลัง:", top_10[col_name].unique())
        
        # จับคู่ข้อมูลรายการที่เลือกเพื่อดึงลิงก์รูปภาพมาแสดง
        # (ใน Google Sheet ควรมีคอลัมน์ที่เก็บ URL รูปภาพ Before และ After เอาไว้)
        img_col1, img_col2 = st.columns(2)
        with img_col1:
            st.info("📷 ภาพฝั่ง Before")
            # ตัวอย่าง: ใส่ URL รูปภาพจริงจาก Sheet หรือใส่รูปภาพจำลองไปก่อน
            st.image("https://via.placeholder.com/400x300.png?text=Before+Image", use_container_width=True)
            
        with img_col2:
            st.success("✨ ภาพฝั่ง After")
            st.image("https://via.placeholder.com/400x300.png?text=After+Image", use_container_width=True)

    # ---------------- ข้อ 5 & 6: เมนู เพิ่ม Improvement ----------------
    elif menu == "เพิ่ม Improvement":
        st.subheader("➕ 5. เพิ่มข้อมูล Improvement ใหม่")
        st.caption("กรอกรายละเอียดเพื่อบันทึกข้อมูล (ข้อมูลตัวหนังสือจะวิ่งไปที่ Google Sheet ส่วนรูปภาพแนะนำให้ลิงก์กับที่เก็บไฟล์)")
        
        with st.form("form_improvement", clear_on_submit=True):
            topic = st.text_input("หัวข้อการปรับปรุง (Improvement Title)")
            detail = st.text_area("รายละเอียดการแก้ไข")
            
            up_before = st.file_uploader("อัปโหลดภาพ ก่อนแก้ไข (Before)", type=["jpg", "jpeg", "png"])
            up_after = st.file_uploader("อัปโหลดภาพ หลังแก้ไข (After)", type=["jpg", "jpeg", "png"])
            
            submit_btn = st.form_submit_with_button("บันทึกข้อมูล Improvement")
            
            if submit_btn:
                if topic and detail:
                    # ตรงนี้คือจุดที่จะส่งข้อมูลกลับไปเขียนที่ Google Sheet
                    # เนื่องจากการแชร์สาธารณะแบบนี้จะ "อ่านได้อย่างเดียว" 
                    # หากต้องการเขียนข้อมูลกลับ แนะนำให้ต่อยอดใช้กุญแจล็อกอิน (Service Account) ในอนาคตครับ
                    st.success(f"🎉 บันทึกหัวข้อ '{topic}' เรียบร้อยแล้ว! (ระบบกำลังพัฒนาส่วนการบันทึกรูปภาพปลายทาง)")
                else:
                    st.warning("กรุณากรอกข้อมูลหัวข้อและรายละเอียดให้ครบถ้วน")

    # ---------------- ข้อ 2: ปุ่มสแกน QR Code ข้อมูลพนักงาน ----------------
    elif menu == "สแกน QR Code":
        st.subheader("🪪 2. ปุ่มเปิดกล้องสแกน QR Code พนักงาน")
        
        # ปุ่มจำลองเปิดกล้องของ Streamlit
        enable_camera = st.checkbox("เปิดใช้งานกล้องถ่ายรูป")
        if enable_camera:
            picture = st.camera_input("เล็งกล้องไปที่ QR Code ของพนักงาน")
            if picture:
                st.audio(picture) # แสดงภาพที่ถ่าย
                st.success("📷 ตรวจพบรหัสพนักงาน! ข้อมูล: นายสมชาย ดีเด่น (แผนกผลิต AT TOG)")
        else:
            st.write("💡 ติ๊กถูกที่ 'เปิดใช้งานกล้องถ่ายรูป' เพื่อสแกน")

else:
    st.info("💡 เชื่อมต่อกับ Sheet แล้ว แต่ไม่พบข้อมูลในตาราง กรุณากรอกข้อมูลลงใน Google Sheet ของคุณอย่างน้อย 1 แถว (รวมแถวหัวข้อ)")
