import streamlit as st
import pandas as pd
import plotly.express as px
# (รวมถึงไลบรารี gspread สำหรับเชื่อมต่อ Google Sheet)

st.title("โปรแกรมตรวจสอบ Improvement AT TOG")

# 1. ฟังก์ชันดึงข้อมูลจาก Google Sheet
def load_data():
    # โค้ดเชื่อมต่อ gspread ด้วย Service Account ตัวอย่าง:
    # gc = gspread.service_account(filename='credentials.json')
    # sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/...')
    # บันทึกข้อมูลแปลงเป็น DataFrame ของ pandas
    df = pd.read_csv("ตัวอย่างข้อมูล_improvement.csv") # สมมติฐานข้อมูล
    return df

df = load_data()

# สร้างแถบเมนูข้างๆ (Sidebar) เพื่อเปลี่ยนหน้า
menu = st.sidebar.selectbox("เมนูใช้งาน", ["ภาพรวม Dashboard", "เพิ่ม Improvement", "สแกน QR Code"])

if menu == "ภาพรวม Dashboard":
    st.subheader("1. ภาพรวมและอันดับ Improvement")
    
    # จัดอันดับ Top 10
    top_10 = df.sort_values(by="คะแนน", ascending=False).head(10)
    
    # วาดกราฟแท่ง Top 10
    fig_bar = px.bar(top_10, x="ชื่อหัวข้อ", y="คะแนน", title="กราฟแท่งแสดงอันดับ 1-10")
    st.plotly_chart(fig_bar)
    
    # วาดกราฟวงกลม Top 10
    fig_pie = px.pie(top_10, names="ชื่อหัวข้อ", values="คะแนน", title="กราฟวงกลมแสดงสัดส่วน 1-10")
    st.plotly_chart(fig_pie)
    
    st.subheader("4. ดูภาพ Before & After ย้อนหลัง")
    selected_job = st.selectbox("เลือกรายการที่ต้องการดูรูปย้อนหลัง", top_10["ชื่อหัวข้อ"])
    # ดึงรูปมาแสดงผลเปรียบเทียบ
    col1, col2 = st.columns(2)
    with col1:
        st.image("url_ภาพ_before_จาก_sheet.jpg", caption="Before")
    with col2:
        st.image("url_ภาพ_after_จาก_sheet.jpg", caption="After")

elif menu == "เพิ่ม Improvement":
    st.subheader("5. เพิ่มข้อมูล Improvement ใหม่")
    with st.form("improvement_form"):
        title = st.text_input("ชื่อหัวข้อ Improvement")
        details = st.text_area("รายละเอียดสิ่งที่แก้ไข")
        
        file_before = st.file_uploader("อัปโหลดภาพ Before", type=["png", "jpg", "jpeg"])
        file_after = st.file_uploader("อัปโหลดภาพ After", type=["png", "jpg", "jpeg"])
        
        submitted = st.form_submit_with_button("บันทึกข้อมูล")
        if submitted:
            # โค้ดส่งรูปไปเก็บ และเขียนข้อมูลลง Google Sheet ด้วย gspread.append_row()
            st.success("บันทึกข้อมูลและอัปเดตลง Google Sheet เรียบร้อยแล้ว!")

elif menu == "สแกน QR Code":
    st.subheader("2. สแกน QR โค้ดข้อมูลพนักงาน")
    img_file = st.camera_input("เปิดกล้องเพื่อสแกน QR Code")
    if img_file:
        # โค้ดใช้ pyzbar แกะรหัสพนักงานจากรูปถ่าย
        st.write("ข้อมูลพนักงาน: นายสมชาย ตั้งใจทำงาน (ID: 65001)")
