import streamlit as st
import cv2
import numpy as np
from PIL import Image
from roboflow import Roboflow

# ==================================================================
# 🚨 [โน้ตหัวข้อสำคัญ] จุดที่พี่วิรัตน์ต้องเปลี่ยน WORDING ให้ตรงกับที่เทรนจริง 🚨
# ==================================================================
# 📌 จุดที่ 1 (บรรทัดที่ 34): เปลี่ยนรหัส API KEY ส่วนตัวของพี่วิรัตน์
# 📌 จุดที่ 2 (บรรทัดที่ 35): เช็กชื่อโปรเจกต์ (เช่น "test11-domtn") ให้ตรงกับบนเว็บ
# 📌 จุดที่ 3 (บรรทัดที่ 36): เลขเวอร์ชัน ต้องเป็นเลข .version(5) ล่าสุดที่พวกเราเพิ่งอบเสร็จ
# 📌 จุดที่ 4 (บรรทัดที่ 46): ตัวแปร TARGET_CLASSES ต้องเปลี่ยนจากของเดิมอุตสาหกรรม 
#                             ให้เป็นคลาสปากกาจริง คือ ["Pink", "Green"] (ห้ามสะกดผิดเด็ดขาด!)
# ==================================================================

# CONFIGURATION & INITIALIZATION
st.set_page_config(page_title="AI Smart Inspection v5", layout="wide")

# เชื่อมต่อเข้าเตาอบสมองกล Roboflow v5 ของพี่วิรัตน์
@st.cache_resource
def init_roboflow_model():
    try:
        # 🔴 [จุดเปลี่ยนที่ 1]: เอา Private API Key ลับยาวๆ ของพี่มาแปะในเครื่องหมายคำพูดแทนที่คำเดิม
        # 🔴 [จุดเปลี่ยนที่ 2]: คำว่า "test11-domtn" ต้องสะกดตรงตามชื่อโปรเจกต์บนหน้าเว็บเป๊ะๆ
        # 🔴 [จุดเปลี่ยนที่ 3]: เลขในวงเล็บ .version(5) ต้องตรงกับเวอร์ชันล่าสุดที่พี่ต้องการรันทดสอบ
        rf = Roboflow(api_key="ใส่_API_KEY_ของพี่ตรงนี้") 
        project = rf.workspace().project("test11-domtn")
        model = project.version(5).model
        return model
    except Exception as e:
        st.error(f"❌ เชื่อมต่อโมเดลไม่สำเร็จ: โปรดตรวจสอบ API Key หรืออินเทอร์เน็ตครับพี่ ({e})")
        return None

model = init_roboflow_model()

# 🔴 [จุดเปลี่ยนที่ 4]: ตัวแปรกลุ่มคลาสเป้าหมาย ต้องเปลี่ยน Wording ให้เป็นคำเดียวกับที่ตีกรอบเป๊ะๆ
# ตัวอย่าง: เดิมเป็นไอเทมอุตสาหกรรม -> ตอนนี้ต้องเป็นกลุ่มปากกา ["Pink", "Green"] เท่านั้น!
TARGET_CLASSES = ["Pink", "Green"]

if "sim_status" not in st.session_state:
    st.session_state.sim_status = "READY"
if "sim_count" not in st.session_state:
    st.session_state.sim_count = 0

# UI DESIGN: DASHBOARD
st.title("🏭 AI Smart Inspection Dashboard (v5 Real-time)")
st.write("สถานีทดสอบระบบตรวจจับวัตถุสแกนภาพสด - แยกแยะปากกา Pink / Green ชัดเจน")
st.markdown("---")

col_cam, col_result = st.columns([3, 2])

with col_cam:
    st.subheader("📸 ข้อ 4: หน้าต่างดึงภาพจากกล้องสด & AI v5")
    
    run_cam = st.checkbox("📸 สับสวิตช์เปิดกล้องอุตสาหกรรม (USB)", value=False)
    st_frame = st.image([]) 
    
    cam_index = st.number_input("🔄 เลือกอินเด็กซ์กล้อง (ถ้าภาพไม่ขึ้นลองเปลี่ยนเป็น 0, 1, 2)", min_value=0, max_value=5, value=0)

    if run_cam and model is not None:
        cap = cv2.VideoCapture(cam_index)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.write("❌ ไม่สามารถดึงภาพจากกล้องได้ ตรวจสอบสายต่อ USB ครับพี่")
                break
                
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(frame_rgb)
            
            # สั่งให้โมเดล v5 ประมวลผลภาพสด
            predictions = model.predict(pil_img, confidence=30).json()
            
            draw_frame = frame.copy()
            detected_items = []
            
            if "predictions" in predictions:
                for det in predictions["predictions"]:
                    x = int(det["x"])
                    y = int(det["y"])
                    w = int(det["width"])
                    h = int(det["height"])
                    label = det["class"]  # 💡 ระบบดึงชื่อที่ AI พ่นออกมา (เช่น "Pink" หรือ "Green")
                    conf = det["confidence"]
                    
                    detected_items.append(label)
                    
                    # คำนวณพิกัดเพื่อวาดกรอบ
                    x1, y1 = int(x - w/2), int(y - h/2)
                    x2, y2 = int(x + w/2), int(y + h/2)
                    
                    # วาดกรอบและแสดงข้อความชื่อคลาส (Pink / Green) ตามที่ AI ตรวจเจอสดๆ
                    cv2.rectangle(draw_frame, (x1, y1), (x2, y2), (0, 165, 255), 3)
                    cv2.putText(draw_frame, f"{label} {conf:.2f}", (x1, y1 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
            
            # อัปเดตยอดการนับวัตถุอัตโนมัติ
            st.session_state.sim_count = len(detected_items)
            if len(detected_items) >= 2:
                st.session_state.sim_status = "OK"
            elif len(detected_items) == 1:
                st.session_state.sim_status = "NG"
            else:
                st.session_state.sim_status = "READY"
                
            final_frame = cv2.cvtColor(draw_frame, cv2.COLOR_BGR2RGB)
            st_frame.image(final_frame, channels="RGB", use_container_width=True)
            
        cap.release()
    else:
        st_frame.image("https://images.unsplash.com/photo-1531747118685-ca8fa6e08806?q=80&w=640", use_container_width=True)

with col_result:
    st.subheader("📊 ข้อ 5: ตรรกะระบบ ผิด-ถูก (OK/NG) คำนวณจาก AI")
    st.write("ระบบจะปล่อยผ่าน (PASS) ก็ต่อเมื่อเจอทั้ง Pink และ Green ครบทั้งคู่")
    st.write("---")
    
    if st.session_state.sim_status == "OK":
        st.markdown(
            "<div style='background-color:#11caa0; padding:20px; border-radius:10px; text-align:center;'> "
            "<h1 style='color:white; margin:0;'>PASS (OK)</h1>"
            "<p style='color:white; margin:0; font-size:18px;'>ยอดเยี่ยม! ตรวจพบปากกาครบทั้งสองสีคู่กัน</p>"
            "</div>", unsafe_allow_html=True
        )
    elif st.session_state.sim_status == "NG":
        st.markdown(
            "<div style='background-color:#ef4444; padding:20px; border-radius:10px; text-align:center;'> "
            "<h1 style='color:white; margin:0;'>REJECT (NG) 🚨</h1>"
            "<p style='color:white; margin:0; font-size:18px;'>พบสิ่งผิดปกติ! วัตถุขาดหายไปหนึ่งสี (ของไม่ครบ)</p>"
            "</div>", unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div style='background-color:#64748b; padding:20px; border-radius:10px; text-align:center;'> "
            "<h1 style='color:white; margin:0;'>SYSTEM READY</h1>"
            "<p style='color:white; margin:0; font-size:18px;'>รอกล่องถัดไปเข้าจุดสแกนภาพ</p>"
            "</div>", unsafe_allow_html=True
        )

    st.write("")
    st.metric(label="จำนวนปากกาทีระบบสแกนเจอในกล่อง", value=f"{st.session_state.sim_count} / 2 แท่ง")
