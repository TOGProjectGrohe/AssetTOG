import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บสไตล์สมาร์ทโฟน
st.set_page_config(page_title="TOG App", layout="centered", initial_sidebar_state="collapsed")

# 2. 🎨 CSS ตกแต่งหน้าจอโทรศัพท์ธีมพาสเทล
st.markdown("""
<style>
.stDeployButton, [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], header, footer, #MainMenu {
display: none !important; visibility: hidden !important; height: 0 !important;
}
[data-testid="stStatusWidget"], #stConnectionStatus, div[class*="viewerBadge"] {
display: none !important; visibility: hidden !important; height: 0 !important;
}
.stApp {
max-width: 420px !important; margin: 0px auto !important;
background: linear-gradient(180deg, #ffb07c 0%, #ffe3d1 30%, #fff7f2 100%) !important;
border: 12px solid #1e293b !important; border-radius: 40px !important;
padding: 95px 24px 24px 24px !important; box-shadow: 0 20px 50px rgba(0,0,0,0.3) !important;
min-height: 90vh !important; height: auto !important;
}
.login-card {
background-color: white !important; border-radius: 20px !important; padding: 15px !important; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important; margin-bottom: 15px !important; width: 100% !important;
}
.custom-top-navbar {
position: absolute !important; top: 20px !important; left: 20px !important; right: 20px !important; display: flex !important; justify-content: space-between !important; align-items: center !important; z-index: 999999 !important;
}
.nav-btn-link {
background-color: #007bc3 !important; color: white !important; border-radius: 20px !important; padding: 8px 16px !important; font-size: 13px !important; font-weight: bold !important; text-decoration: none !important;
}
.center-header-block {
display: flex !important; flex-direction: column !important; align-items: center !important; justify-content: center !important; text-align: center !important; margin-top: 10px !important; margin-bottom: 25px !important; width: 100% !important;
}

.drive-link-button {
display: block !important; text-align: center !important; background-color: #10b981 !important; color: white !important;
font-weight: bold !important; padding: 12px 20px !important; border-radius: 12px !important; text-decoration: none !important;
margin: 12px 0 !important; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25) !important; font-size: 14px !important;
}
.drive-link-button:hover {
background-color: #059669 !important; color: white !important;
}
</style>
""", unsafe_allow_html=True)

# 🌐 ฟังก์ชันดึงข้อมูลพนักงานจาก Google Sheet
def get_employee_from_sheet(input_id):
    sheet_id = 1sRher870S-P1w_kUVfryy-OqM67WjGpwek9y9wm29Ps"""
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
try:
df = pd.read_csv(url)
df.columns = df.columns.str.strip()
if 'ID' in df.columns:
df['ID'] = df['ID'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
match = df[df['ID'] == str(input_id).strip()]
if not match.empty:
row = match.iloc[0]
return {"status": "success", "found": True, "id": str(row['ID']), "name": str(row['Name']).strip()}
except:
pass
return {"status": "success", "found": False}

# 📊 ฟังก์ชันดึงข้อมูลดิบจากลิงก์ Google Sheet
@st.cache_data(ttl=60)
def load_real_defect_data():
sheet_url = "https://docs.google.com/spreadsheets/d/1qKY4ZBWYXM81Y8BZSMjOf7z1hJXeJFCjB5KeRPQBe4c/export?format=csv&gid=0"
try:
df = pd.read_csv(sheet_url)
df.columns = df.columns.str.strip()
return df
except Exception as e:
st.error(f"ไม่สามารถเชื่อมต่อข้อมูลจากชีตหลักได้: {e}")
return pd.DataFrame()

# 🔗 รายชื่อลิงก์ URL คลังภาพทั้ง 18 แฟ้ม (แก้ไข Syntax Error จุด "main_url" ของ C_261 แล้ว)
FOLDER_LINK_MAP = {
A: {
260: {"main_url": "https://drive.google.com/drive/folders/1QTQuQR8e7DUAYQF0yyYreCi9_bGcX6z0", "main_title": "A_260", "slave_url": "https://drive.google.com/drive/folders/1DQWgtMsVcPbpNGRH8WQX65VKfJkCxlp5", "slave_title": "SA_260"},
261: {"main_url": "https://drive.google.com/drive/folders/1phKW7eXcijB4U6P95JHnJm6BgG2bcKyQ", "main_title": "A_261", "slave_url": "https://drive.google.com/drive/folders/1n5KGFnub6z3urE09taiJh4TaUJXqElCF", "slave_title": "SA_261"},
380: {"main_url": "https://drive.google.com/drive/folders/1-77ViPZrWhRXiYMvpa2gTp63CDjxIcHu", "main_title": "A_380", "slave_url": "https://drive.google.com/drive/folders/1DlKAZot6QPHXdvuVu8ro_TIk26NsznDz", "slave_title": "SA_380"}
},
B: {
260: {"main_url": "https://drive.google.com/drive/folders/1NVgoWHj_WTOU7PDdKyozBYJKL7Ap-s4J", "main_title": "B_260", "slave_url": "https://drive.google.com/drive/folders/1mFPvOUYkuH57QSwkw0nOmFUNsQKhl3Tf", "slave_title": "SB_260"},
261: {"main_url": "https://drive.google.com/drive/folders/1q3Kb3ClsvnfulRCug33FoBYlyUvhKz-o", "main_title": "B_261", "slave_url": "https://drive.google.com/drive/folders/1Kf7jjhN1RIcaQG60uIs6bkDs2aafK8OQ", "slave_title": "SB_261"},
380: {"main_url": "https://drive.google.com/drive/folders/1b8jDU2ZJwWuFGihYFVqzbpIVgkH61bhK", "main_title": "B_380", "slave_url": "https://drive.google.com/drive/folders/179CQ6uNpDen5hao1a949EXpmYLOCu4LQ", "slave_title": "SB_380"}
},
C: {
260: {"main_url": "https://drive.google.com/drive/folders/13k1E0lDkRw4BQWKXCz637gHxo5ou7z3V", "main_title": "C_260", "slave_url": "https://drive.google.com/drive/folders/1P3qw10mB6zs4yC4w3Jd2rOXN6KnmuzNr", "slave_title": "SC_260"},
261: {"main_url": "https://drive.google.com/drive/folders/1slgqqMbiRttmRd70hbPkV_DAKoiqGbht", "main_title": "C_261", "slave_url": "https://drive.google.com/drive/folders/1FzfsI-xDgUQPnB_6kDrQ8iGxI5_N075P", "slave_title": "SC_261"},
380: {"main_url": "https://drive.google.com/drive/folders/14jkMpOZG-bIN6h0EYbZ3UrqiFAYUQ7A1", "main_title": "C_380", "slave_url": "https://drive.google.com/drive/folders/11OR4QaWPaLcM6EPaSPrMkQTQrpfqMMJT", "slave_title": "SC_380"}
}
}

if 'page' not in st.session_state: st.session_state.page = "login"
if 'user_info' not in st.session_state: st.session_state.user_info = None
if 'current_defect' not in st.session_state: st.session_state.current_defect = None

current_page = st.session_state.page

st.markdown('<div class="custom-top-navbar"><a href="?nav=reset" target="_self" class="nav-btn-link">🏠 Home</a><a href="?nav=reset" target="_self" class="nav-btn-link">🚪 Logout</a></div>', unsafe_allow_html=True)
if st.query_params.get("nav") == "reset":
st.session_state.page = "login"; st.session_state.user_info = None; st.session_state.current_defect = None
st.query_params.clear(); st.rerun()

st.markdown('<div class="center-header-block"><div style="width:50px; height:50px; background-color:#000000; border-radius:50%; display:flex; justify-content:center; align-items:center; color:#ffffff; font-weight:bold; font-size:15px; margin:0 auto 8px auto;">TOG</div><span style="font-size:18px; font-weight:bold; color:white;">TOG App</span></div>', unsafe_allow_html=True)

# ---------------- หน้าแรก: Login ----------------
if current_page == "login":
st.markdown('<div class="login-card">', unsafe_allow_html=True)
st.markdown("<h4 style='font-size:16px; margin-top:0; color:#2c3e50; text-align:center;'>🪪 ป้อนรหัสพนักงานเพื่อเข้าระบบ</h4>", unsafe_allow_html=True)
input_id = st.text_input("กรอกรหัส ID พนักงานของคุณ:", value="", placeholder="พิมพ์ตัวเลขรหัส เช่น 20", label_visibility="collapsed")
if input_id.strip() != "":
result = get_employee_from_sheet(input_id)
if result["status"] == "success" and result.get("found"):
st.markdown(f'<div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 10px; border-radius: 12px; margin-top: 10px; text-align: center; font-size:13px; color:#16a34a;"><b>✅ ข้อมูลถูกต้อง:</b> {result["name"]}</div>', unsafe_allow_html=True)
if st.button("🔓 กดเพื่อเข้าระบบ"):
st.session_state.user_info = {"id": result["id"], "name": result["name"]}
st.session_state.page = "select_defect"; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- หน้าสอง: คัดเลือก Defect ----------------
elif current_page == "select_defect":
st.markdown('<div class="login-card" style="text-align:center;"><b>🎯 โปรดเลือกประเภท Defect เพื่อตรวจสอบคลังงาน:</b></div>', unsafe_allow_html=True)
if st.button("🟠 ดูข้อมูล Defect 260 (Rough Lines)"):
st.session_state.current_defect = 260; st.session_state.page = "defect_view"; st.rerun()
if st.button("🔵 ดูข้อมูล Defect 261 (Grinding Structure)"):
st.session_state.current_defect = 261; st.session_state.page = "defect_view"; st.rerun()
if st.button("⚫ ดูข้อมูล Defect 380 (Contour/Design Fault)"):
st.session_state.current_defect = 380; st.session_state.page = "defect_view"; st.rerun()

# ---------------- หน้าสาม: บอร์ดสถิติอิง Material จริง ----------------
elif current_page == "defect_view":
defect = st.session_state.current_defect
defect_title = f"Defect {defect}"

if st.button("🔙 กลับไปเลือกประเภท Defect อื่น"):
st.session_state.page = "select_defect"; st.rerun()

st.markdown(f'<div class="login-card" style="text-align:center;"><b>📊 แผงวิเคราะห์รูปงานจริงของ {defect_title}</b></div>', unsafe_allow_html=True)

# 📥 โหลดข้อมูล Material จริง
raw_df = load_real_defect_data()
if not raw_df.empty and 'errortype' in raw_df.columns and 'Material' in raw_df.columns:
raw_df['errortype'] = pd.to_numeric(raw_df['errortype'], errors='coerce')
raw_df['Material'] = raw_df['Material'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
filtered_df = raw_df[raw_df['errortype'] == defect]
qty_col = 'rework quantity' if 'rework quantity' in raw_df.columns else raw_df.columns[-1]
filtered_df[qty_col] = pd.to_numeric(filtered_df[qty_col], errors='coerce').fillna(0)
summary_df = filtered_df.groupby('Material', as_index=False)[qty_col].sum()
chart_data = summary_df.sort_values(by=qty_col, ascending=False).head(10)
else:
chart_data = pd.DataFrame({
Material: ["407787135", "407787136", "407787137", "407787138", "407787139", "407787140", "407787141", "407787142", "407787143", "407787144"],
rework quantity: [45, 38, 32, 28, 25, 21, 18, 15, 12, 10]
})
qty_col = "rework quantity"

# 📊 แผงกราฟสถิติด้านบน
st.markdown('<div class="login-card">', unsafe_allow_html=True)
st.markdown(f"<b style='color:#1e293b; font-size:14px; display:block; text-align:center;'>📈 อัตราส่วนสถิติแยกตาม Material (Top 10)</b>", unsafe_allow_html=True)
st.markdown("<p style='font-size:12px; color:#64748b; text-align:center; margin-top:-2px; margin-bottom:10px;'>💡 จิ้มเลือกแท่งกราฟด้านล่างเพื่อเปลี่ยนชิ้นงานได้ทันที</p>", unsafe_allow_html=True)

if not chart_data.empty:
# 🎨 กำหนดเฉดสีพาสเทลมาตรฐาน
pastel_palette = px.colors.qualitative.Pastel
list_of_materials = chart_data['Material'].tolist()

# 🔑 ✨ สร้างคลัง Map สีผูกเข้ากับชื่อคีย์ชิ้นงานโดยตรง เพื่อป้องกันสีสลับกัน!
color_map = {}
for idx, mat in enumerate(list_of_materials):
color_map[mat] = pastel_palette[idx % len(pastel_palette)]

# 🍕 1. แผนภูมิวงกลม (Pie Chart) - ใช้ color_discrete_map
fig_pie = px.pie(
chart_data,
names="Material",
values=qty_col,
color="Material",
color_discrete_map=color_map
)
fig_pie.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=200, showlegend=False)
st.plotly_chart(fig_pie, use_container_width=True)

# 📊 2. แผนภูมิแท่งแนวตั้ง (Bar Chart) - บังคับระบายสีด้วยชุด Map เดียวกัน สีตรงกับวงกลม 100%
fig_bar = px.bar(
chart_data,
x="Material",
y=qty_col,
orientation='v',
color="Material",
color_discrete_map=color_map
)
fig_bar.update_layout(
margin=dict(l=10, r=10, t=10, b=10), height=250, showlegend=False,
xaxis_title=None, yaxis_title=None,
xaxis=dict(type='category', tickangle=45),
clickmode='event+select'
)

selected_bar = st.plotly_chart(fig_bar, use_container_width=True, on_select="rerun")
state_key = f"sel_mat_{defect}"

# 🎯 ตรวจสอบความเปลี่ยนแปลงจากการคลิกกราฟแท่ง
if selected_bar and "selection" in selected_bar and selected_bar["selection"]["points"]:
clicked_material = selected_bar["selection"]["points"][0]["x"]
st.session_state[state_key] = clicked_material

# กำหนดค่าดีฟอลต์ตัวแรกหากยังไม่มีการกดคลิกอะไรเลย
if state_key not in st.session_state or st.session_state[state_key] not in list_of_materials:
st.session_state[state_key] = list_of_materials[0] if list_of_materials else "ไม่มีข้อมูล"

selected_material = st.session_state[state_key]

st.markdown("<hr style='margin:10px 0; border:0; border-top:1px dashed #ccc;'>", unsafe_allow_html=True)
st.markdown(f'<div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 10px; border-radius: 12px; text-align: center; font-size:14px; color:#16a34a;"><b>🔍 Material ที่เลือกจากกราฟ:</b> <span style="font-size:16px; font-weight:bold; color:#007bc3;">{selected_material}</span></div>', unsafe_allow_html=True)
else:
st.info("ไม่พบข้อมูลสถิติของ Defect นี้ในชีตระบบ")
selected_material = "ไม่มีข้อมูล"
st.markdown('</div>', unsafe_allow_html=True)

# 🔘 ส่วนฟิลเตอร์เลือกพิกัดหน้างาน
selected_face = st.radio("เลือกพิกัดหน้างาน:", ["หน้า A", "หน้า B", "หน้า C"], horizontal=True, key=f"rf_{defect}")

if selected_face in ["หน้า A", "หน้า B", "หน้า C"]:
face_char = selected_face.split()[-1]
folder_info = FOLDER_LINK_MAP[face_char][defect]

# 📂 ส่วนที่ 1: คลังภาพหลักชิ้นงาน
st.markdown('<div class="login-card">', unsafe_allow_html=True)
st.markdown(f"<b style='color:#005aab; font-size:14px;'>📁 1. คลังภาพหลักชิ้นงาน ({folder_info['main_title']}) ของ {selected_material}</b>", unsafe_allow_html=True)
st.markdown(f'<a href="{folder_info["main_url"]}" target="_blank" class="drive-link-button">🖼️ กดเปิดคลังภาพใหญ่ {folder_info["main_title"]} ↗️</a>', unsafe_allow_html=True)

msg_main = f"แนบรูปภาพหลักที่เลือกของ {selected_material} ที่นี่:"
uploaded_main = st.file_uploader(msg_main, type=["png", "jpg", "jpeg"], key=f"up_m_{defect}")
if uploaded_main:
st.image(uploaded_main, caption=f"✅ รูปภาพหลัก {selected_material} ที่คุณเลือก", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# 📂 ส่วนที่ 2: คลังรูปรายละเอียดจุดย่อย
st.markdown('<div class="login-card">', unsafe_allow_html=True)
st.markdown(f"<b style='color:#007bc3; font-size:14px;'>📁 2. คลังรูปรายละเอียดจุดย่อย ({folder_info['slave_title']})</b>", unsafe_allow_html=True)
st.markdown(f'<a href="{folder_info["slave_url"]}" target="_blank" class="drive-link-button">🖼️ กดเปิดคลังภาพย่อย {folder_info["slave_title"]} ↗️</a>', unsafe_allow_html=True)

msg_slave = "แนบรูปรายละเอียดจุดย่อย (สูงสุด 5 รูป):"
uploaded_slaves = st.file_uploader(msg_slave, type=["png", "jpg", "jpeg"], accept_multiple_files=True, key=f"up_s_multiple_{defect}")

if uploaded_slaves:
allowed_slaves = uploaded_slaves[:5]
st.markdown(f"<p style='font-size:12px; color:#10b981; font-weight:bold;'>📸 รูปรายละเอียดจุดย่อยที่แนบ ({len(allowed_slaves)}/5 รูป):</p>", unsafe_allow_html=True)
for idx, img_file in enumerate(allowed_slaves):
st.image(img_file, caption=f"รูปภาพย่อยที่ {idx+1}: {img_file.name}", use_container_width=True)
if len(uploaded_slaves) > 5:
st.warning("⚠️ ระบบรองรับภาพย่อยสูงสุด 5 รูปต่อครั้ง")
st.markdown('</div>', unsafe_allow_html=True)

# 🔲 ส่วนสรุปรายละเอียดงาน AFTER
st.markdown('<div class="login-card" style="border-top: 4px solid #10b981;">', unsafe_allow_html=True)
st.markdown(f"<b style='color:#10b981; font-size:14px; display:block; margin-bottom:5px;'>✨ ส่วนอัปเดตงาน After ({defect_title} - {selected_material})</b>", unsafe_allow_html=True)
st.text_area("พิมพ์ข้อความสรุปรายละเอียดผลงาน After:", value="", key=f"ta_af_{defect}")
st.camera_input("ถ่ายภาพยืนยันผลงาน After ชิ้นงานจริง", key=f"c_af_{defect}_final")
st.markdown('</div>', unsafe_allow_html=True)
