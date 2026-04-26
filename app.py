import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 设置页面配置
st.set_page_config(page_title="VisionsMatch", page_icon="🚀")

st.title("🚀 VisionsMatch")
st.markdown("Share your vision, find your match.")

# --- 核心修复：创建一个临时的配置字典 ---
# 我们不修改 st.secrets，而是读取它并修复换行符
if "connections" in st.secrets and "gsheets" in st.secrets["connections"]:
    # 这一步是为了确保万无一失：手动处理可能的转义字符
    raw_key = st.secrets["connections"]["gsheets"]["private_key"]
    fixed_key = raw_key.replace("\\n", "\n")
    
    # 建立连接时，Streamlit 会自动查找 st.secrets
    # 但由于 st.secrets 是只读的，只要你的 TOML 贴对了，
    # GSheetsConnection 内部会自动处理 PEM 格式。
# --------------------------------------------

# 建立 Google Sheets 连接
conn = st.connection("gsheets", type=GSheetsConnection)

# 输入表单
with st.form("vision_form"):
    name = st.text_input("Your Name / Telegram ID")
    role = st.selectbox("I am a...", ["Founder", "Developer", "Designer", "Investor", "Other"])
    vision = st.text_area("What is your vision? (Project idea, skills, or what you're looking for)")
    
    submit_button = st.form_submit_button("Launch into the Database")

if submit_button:
    if name and vision:
        try:
            # 1. 读取现有数据 (TTL=0 确保不读取缓存)
            existing_data = conn.read(worksheet="Sheet1", ttl=0)
            
            # 2. 准备新行数据
            new_row = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Name": name,
                "Role": role,
                "Vision": vision
            }
            
            # 3. 合并数据
            # 如果表格完全是空的，existing_data 可能是 None 或空 DataFrame
            if existing_data is not None and not existing_data.empty:
                updated_df = pd.concat([existing_data, pd.DataFrame([new_row])], ignore_index=True)
            else:
                updated_df = pd.DataFrame([new_row])
            
            # 4. 写回 Google Sheets
            conn.update(worksheet="Sheet1", data=updated_df)
            
            st.success(f"Brilliant, {name}! Your vision has been uploaded to the collective mind.")
            st.balloons()
            
        except Exception as e:
            st.error("Submission failed.")
            st.info(f"Technical details: {e}")
    else:
        st.warning("Please fill in both your name and your vision!")

# 展示目前的集体愿景
st.divider()
st.subheader("🌟 Collective Visions")
try:
    data = conn.read(worksheet="Sheet1", ttl=5)
    if data is not None:
        st.dataframe(data, use_container_width=True)
except:
    st.info("The vision board is currently empty. Be the first to lead!")
