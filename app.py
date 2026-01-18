import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. UI Styling
st.set_page_config(page_title="BioMorph Pro AI", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #05070a; color: white; }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, h1, h2, h3, label {
        color: #ffffff !important;
    }
    .stButton>button {
        width: 100%; background: linear-gradient(90deg, #10b981 0%, #3b82f6 100%);
        color: white !important; font-weight: bold; padding: 15px; border-radius: 10px;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# 2. API Configuration (DIRECT KEY IN CODE)
# Yahan maine aapki API key dal di hai:
MY_API_KEY = "AIzaSyAYGG0_efV9MBtP_cg11jHkHAYQsWFhciI"
genai.configure(api_key=MY_API_KEY)

# Gemini 1.5 Flash use kar rahe hain takay 404 error na aaye
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🦁 BioMorph: Multi-Character Transformer")

# 3. Input Layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📸 Step 1: Upload Image")
    uploaded_file = st.file_uploader("Select image...", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)

with col2:
    st.subheader("⚙️ Step 2: Customization")
    character_info = st.text_input("Genders & Characters:", value="1 Male Tiger, 1 Female Red Panda, 1 Red Panda Kitten")
    dress_style = st.text_area("Dressing Details:", value="Tiger in a leather jacket, Female Red Panda in a floral dress, Kitten in a small sweater.")

# 4. Action & Result
if st.button("Generate Transformation ✨"):
    if uploaded_file and character_info:
        with st.spinner("AI is transforming your scene..."):
            try:
                prompt = (
                    f"Task: Transform humans in the image into humanoid animals. "
                    f"Characters to create: {character_info}. "
                    f"Dressing: {dress_style}. "
                    f"Instructions: Keep the EXACT background, poses, lighting, and objects. "
                    f"Describe the new scene in detail for each character separately."
                )
                response = model.generate_content([prompt, img])
                st.markdown("---")
                st.subheader("✅ Transformation Story:")
                st.markdown(f"<div style='border: 2px solid #10b981; padding: 20px; border-radius: 10px; background-color: #1e293b; font-size: 18px;'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred: {e}")
