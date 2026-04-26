import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 设置页面配置
st.set_page_config(page_title="VisionsMatch", page_icon="🚀")

st.title("🚀 VisionsMatch")
st.markdown("Share your vision, find your match.")

# --- 关键修改部分：手动修复 Secrets 里的 Private Key ---
# 因为 TOML 经常把 \n 读错，我们在这里强行把它变回 Google 需要的真实换行
if "connections" in st.secrets and "gsheets" in st.secrets["connections"]:
    raw_key = st.secrets["connections"]["gsheets"]["private_key"]
    # 将字符串里的 \n 替换为真实的换行符，并确保两端干净
    st.secrets["connections"]["gsheets"]["private_key"] = raw_key.replace("\\n", "\n")

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
            updated_df = pd.concat([existing_data, pd.DataFrame([new_row])], ignore_index=True)
            
            # 4. 写回 Google Sheets
            conn.update(worksheet="Sheet1", data=updated_df)
            
            st.success(f"Brilliant, {name}! Your vision has been uploaded to the collective mind.")
            st.balloons()
            
        except Exception as e:
            st.error("Connection failed. Please check if the Bot Email is added as an 'Editor' in your Google Sheet.")
            st.info("Technical details for Captain: " + str(e))
    else:
        st.warning("Please fill in both your name and your vision!")

# 展示目前的集体愿景
st.divider()
st.subheader("🌟 Collective Visions")
try:
    data = conn.read(worksheet="Sheet1", ttl=5) # 5秒缓存
    st.dataframe(data, use_container_width=True)
except:
    st.info("The vision board is currently empty. Be the first to lead!")
