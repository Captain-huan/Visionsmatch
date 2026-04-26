import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="VisionsMatch | AI-Driven Social Lab", 
    page_icon="🏳️‍🌈", 
    layout="centered"
)

# Custom Styling
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

# 统一使用 VisionsMatch
st.title("🏳️‍🌈 VisionsMatch")
st.markdown("### Where Visions Align.")
st.write("Match with partners based on long-term life visions, not just photos.")
st.caption("Alpha Testing: AI will analyze your vision for the best match. Captain-Huan will make sure AI doesn't hallucinate.")

# Form Implementation
with st.form("match_form"):
    st.info("📍 Basic Information")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name / Nickname")
        gender = st.selectbox("Gender Identity", ["Man", "Woman", "Non-binary", "Other"])
    with col2:
        age = st.number_input("Age", min_value=18, max_value=100, value=25)
        orientation = st.selectbox("Orientation", ["Gay", "Lesbian", "Bi", "Queer", "Other"])
    
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

if submit_button:
    if not name or not email or not vision:
        st.error("Please fill in your Name, Email, and Vision to ensure matching accuracy.")
    else:
        st.success(f"Brilliant, {name}! Your vision has been uploaded to the VisionsMatch database.")
        st.balloons()
        st.markdown(f"""
        ### 🚀 What's next?
        1. **Captain-Huan** will process your vision using LLM (Large Language Models) for semantic analysis.
        2. A customized **Match Report** will be sent to your email (**{email}**) as soon as possible.
        3. Keep an eye on your inbox from `VisionsMatch`.
        """)

# Footer
st.divider()
st.caption("Developed by Captain-Huan | TikTok @captainhuan")
st.caption("VisionsMatch © 2026 - An AI-Native Social Experiment for the LGBTQ+ Community")
