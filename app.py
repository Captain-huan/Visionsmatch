import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

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
# 确保你在 Streamlit Secrets 中配置了 [connections.gsheets]
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🏳️‍🌈 VisionsMatch")
st.markdown("### Where Visions Align.")
st.write("Match with partners based on long-term life visions, not just photos.")
st.caption("Alpha Testing: AI will analyze your vision for the best match. Captain-Huan will make sure AI doesn't hallucinate.")

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
        st.error("Please fill in required fields.")
    else:
        try:
            # 简化数据，直接创建一个只有这一行数据的 DataFrame
            new_data = pd.DataFrame([{
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
            }])
            
            # 暴力写入：不读旧数据，直接覆盖或写入到 Sheet1
            # 这一步如果通了，说明 Secrets 和权限就没问题了
            conn.update(worksheet="Sheet1", data=new_data)
            
            st.success("Connection Success! Data written.")
            st.balloons()
        except Exception as e:
            st.error(f"Error: {e}")

            # 合并新旧数据
            updated_df = pd.concat([existing_data, pd.DataFrame([new_row])], ignore_index=True)
            
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
            st.error("Submission failed. Technical issues with database connection.")
            st.warning("Please ensure your Google Sheet tab is named 'Sheet1' and headers are correctly set.")
            # 打印具体错误方便调试，上线后可以注释掉下面这行
            st.write(f"Error details: {e}")

# 6. 页脚 (Footer)
st.divider()
st.caption("Developed by Captain-Huan | TikTok @captainhuan")
st.caption("VisionsMatch © 2026 - An AI-Native Social Experiment for the LGBTQ+ Community")
