import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Config & White Text Style
st.set_page_config(page_title="BioMorph AI", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0b0f19; }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, h1, h2, h3, label {
        color: #ffffff !important;
    }
    input, textarea, [data-baseweb="select"] * {
        color: #ffffff !important;
        background-color: #1e293b !important;
    }
    .stButton>button {
        width: 100%; background: linear-gradient(90deg, #38bdf8 0%, #3b82f6 100%);
        color: white !important; border-radius: 10px; font-weight: bold; padding: 15px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🦁 BioMorph AI: Simple Character Switcher")

# 2. API Setup
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = "YAHAN_APNI_KEY_LIKHEIN"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Main Interface
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("📸 Step 1: Upload Photo")
    uploaded_file = st.file_uploader("Original image upload karein", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)

with col2:
    st.subheader("⚙️ Step 2: Custom Options")
    
    # 1. Animal Selection
    animal_opt = st.selectbox("Animal Select Karein:", ["Lion", "Tiger", "Cat", "Dog", "Wolf", "Panda", "Custom"])
    custom_animal = ""
    if animal_opt == "Custom":
        custom_animal = st.text_input("Apna Animal likhein:")

    # 2. Genders & Count (The most important part)
    st.info("Example: 1 Male, 1 Female, 2 Kittens")
    gender_details = st.text_input("Kitnay Characters aur kya Genders hain?", placeholder="e.g. 2 Male and 1 Kitten")

    # 3. Dressing
    dress_opt = st.selectbox("Dressing Style:", ["Royal Armor", "Poor/Ragged", "Space Suit", "Modern", "Custom"])
    custom_dress = ""
    if dress_opt == "Custom":
        custom_dress = st.text_input("Apna Dressing style likhein:")

# 4. Process Button
if st.button("BioMorph Magic ✨"):
    if uploaded_file and gender_details:
        with st.spinner("AI is working..."):
            try:
                # Prompt Building
                final_animal = custom_animal if animal_opt == "Custom" else animal_opt
                final_dress = custom_dress if dress_opt == "Custom" else dress_opt
                
                prompt = (
                    f"In this image, replace all characters with {final_animal}. "
                    f"The character breakdown is: {gender_details}. "
                    f"Dressing style should be: {final_dress}. "
                    f"Keep the exact same poses and positions as the original photo."
                )
                
                response = model.generate_content([prompt, img])
                
                st.markdown("### ✅ Result (White Text):")
                st.markdown(f"<div style='color: white; border: 1px solid #38bdf8; padding: 15px;'>{response.text}</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Pehle image aur details mukammal karein!")
