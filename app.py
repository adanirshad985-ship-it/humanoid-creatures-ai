import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. UI Styling
st.set_page_config(page_title="BioMorph Pro AI", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #05070a; color: white; }
    .stButton>button {
        width: 100%; background: linear-gradient(90deg, #10b981 0%, #3b82f6 100%);
        color: white !important; font-weight: bold; padding: 15px; border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 2. API Configuration (Key yahan dal di hai)
MY_API_KEY = "AIzaSyAYGG0_efV9MBtP_cg11jHkHAYQsWFhciI"
genai.configure(api_key=MY_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🦁 BioMorph: Tiger & Red Panda Transformer")

# 3. Layout
col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader("Photo Upload Karein", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)

with col2:
    st.subheader("Character Details")
    char_info = st.text_input("Characters:", value="1 Male Tiger, 1 Female Red Panda, 1 Red Panda Kitten")
    dress_style = st.text_area("Dressing:", value="Tiger in leather jacket, Red Panda in floral dress, Kitten in sweater")

if st.button("Generate Transformation ✨"):
    if uploaded_file:
        with st.spinner("AI is thinking..."):
            try:
                prompt = f"Transform humans in image to: {char_info}. Dressing: {dress_style}. Keep same poses/background. Describe each in detail."
                response = model.generate_content([prompt, img])
                st.success("Transformation Ready!")
                st.markdown(f"<div style='border:2px solid #10b981; padding:20px; border-radius:10px;'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")
