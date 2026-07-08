import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บพื้นฐานให้กระชับเข้ามุมมองสไตล์สมาร์ทโฟน
st.set_page_config(page_title="TOG App", layout="centered", initial_sidebar_state="collapsed")

# 2. 🛠️ ชุดคำสั่งดักทำลายป้ายแอดมิน และสร้างระบบ Scrollable เลื่อนซ้าย-ขวาสำหรับกราฟบนมือถือ
st.markdown("""
    <style>
    /* 🚫 ซ่อนปุ่มแอดมิน, ปุ่มเครื่องมือ และป้าย Deploy ดั้งเดิมของ Streamlit ทั้งหมด */
    .stDeployButton, 
    [data-testid="stHeader"], 
    [data-testid="stToolbar"], 
    [data-testid="stDecoration"],
    header, 
    footer,
    #MainMenu {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }
    
    /* 🚫 ฝังบล็อกเลเยอร์ซ่อนปุ่มป้ายวงกลมเขียว (Manage App) บนหน้าจอมือถือ */
    [data-testid="stStatusWidget"], 
    #stConnectionStatus,
    .st-emotion-cache-zq59db,
    .st-emotion-cache-1wb763a,
    .st-emotion-cache-6q9sum,
    .st-emotion-cache-15z78k,
    .st-emotion-cache-b9st7z,
    .st-emotion-cache-h5g6vv,
    div[class*="st-emotion-cache-"] button[title="Manage app"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0 !important;
    }

    /* 📱 ดีไซน์คุมธีมหน้าจอมือถือ ส้มพาสเทลสวยงาม */
    .stApp {
        max-width: 420px !important;
        margin: 0px auto !important;
        background: linear-gradient(180deg, #ffb07c 0%, #ffe3d1 30%, #fff7f2 100%) !important;
        border: 12px solid #1e293b !important;
        border-radius: 40px !important;
        padding: 24px !important;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3) !important;
        min-height: 90vh !important;
        height: auto !important;
    }
    
    /* 🎯 เคลียร์ระยะห่างและแท่งแถบสีขาวรี ๆ ที่ชอบโผล่มาคั่นช่องว่างเลเยอร์ */
    div[data-testid="stVerticalBlock"] > div,
    div[data-testid="element-container"],
    [data-testid="stVerticalBlock"] {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0px !important;
        margin: 0px !important;
    }

    /* 🪪 กล่องพื้นหลังขาว Card ครอบส่วนเนื้อหาสำคัญ */
    .login-card {
        background-color: white !important;
        border-radius: 20px !important;
        padding: 15px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 15px !important;
    }

    /* 🎯 🛝 ไม้ตายสร้างกล่องเลื่อนสไลด์ ซ้าย-ขวา (Horizontal Scroll) สำหรับกราฟบนจอมือถือ */
    .scrollable-graph-container {
        width: 100% !important;
        overflow-x: auto !important;
        overflow-y: hidden !important;
        display: block !important;
        margin-bottom: 20px !important;
        -webkit-overflow-scrolling: touch; /* สไลด์ลื่นบน iOS */
    }
    
    /* บังคับความกว้างกล่องกราฟด้านในให้ยาวเกินจอ เพื่อให้ใช้นิ้วปัดเลื่อนดูรหัสเต็มๆ ได้ */
    .inner-graph-box {
        width: 600px !important; /* ถ่างพื้นที่ออกไปด้านข้างให้พิมรหัสเต็มชื่อ */
        display: block !important;
    }

    .bottom-wrapper {
        text-align: center !important;
        width: 100% !important;
        margin-top: 35px !important;
    }

    div.stButton {
        display: block !important;
        width: 100% !important;
    }

    /* บังคับปุ่ม Dashboard ให้ยาวใหญ่เต็มขอบจอ สีฟ้าสดใส และโค้งมน */
    div.stButton > button {
        background-color: #007bc3 !important;
        color: white !important;
        border-radius: 30px !important;
        padding: 14px 0px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        border: none !important;
        width: 100% !important;
        display: block !important;
        margin: 0 auto !important;
        box-shadow: 0 4px 15px rgba(0, 123, 195, 0.4) !important;
    }
    div.stButton > button:hover {
        background-color: #0c2340 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 📊 ฟังก์ชันเชื่อมต่อเพื่อดึงและแบ่งกลุ่มข้อมูลตามรหัส errortype ต่างๆ
@st.cache_data(ttl=15)
def get_graph_data(target_error):
    sheet_id = "1qKY4ZBWYXM81Y8BZSMjOf7z1hJXeJFCjB5KeRPQBe4c"
    gid = "0"
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    try:
        raw_df = pd.read_csv(csv_url)
        raw_df.columns = raw_df.columns.str.strip()
        
        raw_df['errortype'] = pd.to_numeric(raw_df['errortype'], errors='coerce')
        raw_df['rework quantity'] = pd.to_numeric(raw_df['rework quantity'], errors='coerce').fillna(0)
        
        filtered_df = raw_df[raw_df['errortype'] == target_error]
        
        grouped_df = filtered_df.groupby('Material', as_index=False)['rework quantity'].sum()
        top_10 = grouped_df.sort_values(by='rework quantity', ascending=False).head(10)
        
        # บังคับประเภทเป็น String ป้องกันแกน X เพี้ยนเป็นทศนิยมหรือค่า M
        top_10['Material'] = top_10['Material'].astype(str)
        return top_10
    except:
        return pd.DataFrame(columns=['Material', 'rework quantity'])

# 4. ระบบจัดการหน้าเพจด้วย Session State
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# --- ส่วนหัวแอปพลิเคชัน (Header) ---
st.markdown("""
<div class="bank-header">
    <div class="tog-circle-logo">TOG</div>
    <div>
        <small style="color:#fff; opacity:0.8; display:block; font-size:11px;">ยินดีต้อนรับ</small>
        <span style="font-size:16px; font-weight:600; color:white;">TOG App</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- หน้าแรก: Login ----------------
if st.session_state.page == 'login':
    st.markdown('<div style="background:rgba(255,255,255,0.4); border:1px solid rgba(255,255,255,0.5); border-radius:20px; padding:15px; text-align:center; color:#2c3e50; font-weight:bold; margin-bottom:20px;">✨ ปรับปรุงประสิทธิภาพการทำงานอย่างต่อเนื่อง</div>', unsafe_allow_html=True)

    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:18px; margin-top:0; color:#2c3e50;'>🪪 ส่วนพนักงานเข้าใช้งาน</h3>", unsafe_allow_html=True)

    enable_camera = st.checkbox("เปิดสิทธิ์ใช้งานกล้องถ่ายรูป", value=True)
    if enable_camera:
        st.markdown("<p style='font-size:13px; color:#64748b; margin-top:10px;'>สแกน QR Code พนักงานของคุณ</p>", unsafe_allow_html=True)
        picture = st.camera_input("", label_visibility="collapsed")
        if picture:
            st.session_state.page = 'dashboard'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="bottom-wrapper"><div style="color:#2c3e50; font-size:16px; margin-bottom:15px; font-weight:500;">ต้องการดูข้อมูลสรุปโดยไม่ล็อกอิน?</div></div>', unsafe_allow_html=True)
    if st.button("📊 ดูภาพรวม Dashboard"):
        st.session_state.page = 'dashboard'
        st.rerun()

# ---------------- หน้าสอง: Dashboard (สไลด์เลื่อนซ้าย-ขวาได้ ชื่อเต็มชัดเจน) ----------------
elif st.session_state.page == 'dashboard':
    st.markdown('<div style="text-align:center; font-size:20px; font-weight:bold; color:#2c3e50; margin-bottom:15px;">📊 สรุปภาพรวม Dashboard</div>', unsafe_allow_html=True)
    st.caption("👉 ใช้นิ้วปัดเลื่อนซ้าย-ขวาที่ตัวกราฟ เพื่อดูอันดับชิ้นงานเพิ่มเติมได้")

    # 📈 กราฟชุดที่ 1: รหัสความผิดพลาด 260
    st.markdown('<div class="login-card"><b>🔥 อันดับชิ้นงานสูงสุด อาการ 260 (Rough Lines)</b></div>', unsafe_allow_html=True)
    df_260 = get_graph_data(260)
    if not df_260.empty:
        # เปิดกล่องห่อหุ้มเลื่อนซ้ายขวาด้วย HTML
        st.markdown('<div class="scrollable-graph-container"><div class="inner-graph-box">', unsafe_allow_html=True)
        fig_260 = px.bar(df_260, x='Material', y='rework quantity', text='rework quantity', color='rework quantity', color_continuous_scale="Oranges")
        fig_260.update_traces(textposition='outside')
        # บังคับแกน X ตัวอักษรเอียง 45 องศาเพื่อหลบชื่อยาว และล็อกแกน Y เป็นเลขตัวชิ้นเดี่ยวๆ
        fig_260.update_layout(
            xaxis=dict(type='category', tickangle=45),
            yaxis=dict(tickformat='d'),
            margin=dict(l=10, r=10, t=25, b=50), 
            height=250, 
            showlegend=False, 
            coloraxis_showscale=False, 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_260, use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True) # ปิดกล่องเลื่อน
    else:
        st.caption("ไม่มีข้อมูลสำหรับรหัส 260")

    # 📈 กราฟชุดที่ 2: รหัสความผิดพลาด 261
    st.markdown('<div class="login-card"><b>⚡ อันดับชิ้นงานสูงสุด อาการ 261 (Grinding Structure Visible)</b></div>', unsafe_allow_html=True)
    df_261 = get_graph_data(261)
    if not df_261.empty:
        st.markdown('<div class="scrollable-graph-container"><div class="inner-graph-box">', unsafe_allow_html=True)
        fig_261 = px.bar(df_261, x='Material', y='rework quantity', text='rework quantity', color='rework quantity', color_continuous_scale="Purples")
        fig_261.update_traces(textposition='outside')
        fig_261.update_layout(
            xaxis=dict(type='category', tickangle=45),
            yaxis=dict(tickformat='d'),
            margin=dict(l=10, r=10, t=25, b=50), 
            height=250, 
            showlegend=False, 
            coloraxis_showscale=False, 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_261, use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)
    else:
        st.caption("ไม่มีข้อมูลสำหรับรหัส 261")

    # 📈 กราฟชุดที่ 3: รหัสความผิดพลาด 380
    st.markdown('<div class="login-card"><b>💥 อันดับชิ้นงานสูงสุด อาการ 380</b></div>', unsafe_allow_html=True)
    df_380 = get_graph_data(380)
    if not df_380.empty:
        st.markdown('<div class="scrollable-graph-container"><div class="inner-graph-box">', unsafe_allow_html=True)
        fig_380 = px.bar(df_380, x='Material', y='rework quantity', text='rework quantity', color='rework quantity', color_continuous_scale="Blues")
        fig_380.update_traces(textposition='outside')
        fig_380.update_layout(
            xaxis=dict(type='category', tickangle=45),
            yaxis=dict(tickformat='d'),
            margin=dict(l=10, r=10, t=25, b=50), 
            height=250, 
            showlegend=False, 
            coloraxis_showscale=False, 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_380, use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)
    else:
        st.caption("ไม่มีข้อมูลสำหรับรหัส 380")

    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    
    # ปุ่มควบคุมท้ายเพจ
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 ประวัติย้อนหลัง", use_container_width=True):
            st.toast("กำลังพัฒนาส่วนนี้...")
    with col2:
        if st.button("➕ เพิ่มตัว Imp.", use_container_width=True):
            st.toast("กำลังพัฒนาส่วนนี้...")
            
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    if st.button("🔙 ออกจากระบบ", use_container_width=True):
        st.session_state.page = 'login'
        st.rerun()
