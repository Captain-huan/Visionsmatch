import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. 页面配置 (Page Configuration)
st.set_page_config(
    page_title="VisionsMatch | AI-Driven Social Lab", 
    page_icon="🏳️‍🌈", 
    layout="centered"
)

# 2. 自定义样式 (Custom Styling)
st.markdown("""
    <style>
    .main {
        background-color: #fcfaff;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #ff4bad;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 建立 Google Sheets 连接
# 根据 TOML 1.1.0 规范，只要 Secrets 里的 private_key 使用三单引号 ''' 包裹物理换行，
# 此处的 conn 会自动获取最纯净的密钥格式，无需手动 replace。
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Database connection failed during initialization.")
    st.stop()

st.title("🏳️‍🌈 VisionsMatch")
st.markdown("### Where Visions Align.")
st.write("Match with partners based on long-term life visions, not just photos.")
st.caption("Alpha Testing: AI will analyze your vision for the best match. Captain-Huan will ensure AI integrity.")

# 4. 表单设计 (Form Implementation)
with st.form("match_form"):
    st.info("📍 Basic Information")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name / Nickname")
        gender = st.selectbox("Gender Identity", ["Man", "Woman", "Non-binary", "Other"])
    with col2:
        age = st.number_input("Age", min_value=18, max_value=100, value=25)
        orientation = st.selectbox("Orientation", ["Gay", "Lesbian", "Bi", "Queer", "Other"])
    
    social_handle = st.text_input("Instagram / TikTok Handle (For verification)")
    birthday = st.date_input("Birthday (Optional, for astrological insights)")
    
    st.divider()
    st.info("🧠 Soul & Vision (Core)")
    
    my_quality = st.text_area("Your Core Qualities", 
                             placeholder="e.g., Career-driven, emotionally intelligent, animal lover...")
    
    partner_quality = st.text_area("What are you looking for in a partner?", 
                                  placeholder="e.g., International background, sense of humor, deep conversationalist...")
    
    vision = st.text_area("Describe your Dream Life Vision", 
                         placeholder="Be specific: Where do you want to live? Career goals? Thoughts on family/children?...",
                         height=150)

    st.divider()
    email = st.text_input("Email (To receive your Match Report)", placeholder="example@email.com")
    
    submit_button = st.form_submit_button("Submit Vision for Matching")

# 5. 提交逻辑与数据持久化
if submit_button:
    if not name or not email or not vision:
        st.error("Please fill in Name, Email, and Vision to ensure matching accuracy.")
    else:
        try:
            # 整理单行数据
            new_row = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Name": name,
                "Gender": gender,
                "Age": age,
                "Orientation": orientation,
                "Social_Handle": social_handle,
                "Birthday": str(birthday),
                "Self_Qualities": my_quality,
                "Partner_Qualities": partner_quality,
                "Vision": vision,
                "Email": email
            }
            
            # 尝试读取现有数据 (ttl=0 保证不读取缓存)
            try:
                existing_data = conn.read(worksheet="Sheet1", ttl=0)
                # 过滤掉全空行，防止索引混乱
                if existing_data is not None:
                    existing_data = existing_data.dropna(how="all")
            except Exception:
                # 如果是全新的表格或读取失败，初始化一个带表头的空表
                existing_data = pd.DataFrame(columns=new_row.keys())

            # 合并新旧数据
            if existing_data is not None and not existing_data.empty:
                updated_df = pd.concat([existing_data, pd.DataFrame([new_row])], ignore_index=True)
            else:
                updated_df = pd.DataFrame([new_row])
            
            # 写回 Google Sheets
            conn.update(worksheet="Sheet1", data=updated_df)
            
            st.success(f"Brilliant, {name}! Your vision has been uploaded to the VisionsMatch database.")
            st.balloons()
            st.markdown(f"""
            ### 🚀 What's next?
            1. **Captain-Huan** will process your vision using LLM for semantic analysis.
            2. A customized **Match Report** will be sent to your email (**{email}**) within 48 hours.
            """)
            
        except Exception as e:
            st.error("Submission failed.")
            st.info(f"Captain's Debug Log: {e}")

# 6. 页脚 (Footer)
st.divider()
st.caption("Developed by Captain-Huan | TikTok @captainhuan")
st.caption("VisionsMatch © 2026 - An AI-Native Social Experiment for the LGBTQ+ Community")
