import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. Page Config (Interface ko khoobsurat banane ke liye)
st.set_page_config(page_title="Personal AI Editor", layout="centered")

# 2. CSS Styling (Buttons aur Look ke liye)
st.markdown("""
<style>
    .stApp { background-color: #0f172a; color: white; }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #38bdf8 0%, #0ea5e9 100%);
        color: white;
        border: none;
        padding: 15px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 18px;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 5px 15px rgba(56, 189, 248, 0.4); }
    input { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

st.title("🎨 Private AI Character Editor")
st.write("Apni image upload karein aur jo dil chahe change likhein (Dress, Skin, Animals, etc.)")

# 3. API Key Management (Safe Tareeqa)
# Pehle Streamlit Secrets check karega, agar wahan nahi mili toh niche wala string use karega
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = "YAHAN_APNI_API_KEY_LIKHEIN" # <-- Agar secrets use nahi kar rahe toh yahan key dalein

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Image Upload Section
uploaded_file = st.file_uploader("Apni Photo Select Karein", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Image Display
    image = Image.open(uploaded_file)
    st.image(image, caption="Aapki Base Image", use_container_width=True)

    # 5. Open-Ended Customization Box
    user_prompt = st.text_input(
        "Kya tabdeeli karni hai?", 
        placeholder="Maslan: Change dress to gold armor, add a wolf in background, make skin silver..."
    )

    if st.button("Magic Process ✨"):
        if user_prompt:
            with st.spinner("AI Aapki instruction par ghaur kar raha hai..."):
                try:
                    # AI Processing
                    # Hum image aur prompt dono bhej rahe hain
                    response = model.generate_content([user_prompt, image])
                    
                    st.success("AI Response:")
                    st.write(response.text)
                    
                    st.info("💡 Note: Filhal ye model image ko analyze karke description de raha hai. Nayi image generate karne ka feature agle step mein add karenge.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Pehle likhein ke aapko kya change chahiye!")

else:
    st.info("Shuru karne ke liye koi bhi image upload karein
