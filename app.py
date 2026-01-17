import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Private AI Editor", layout="centered")

st.title("🎨 Personal AI Character Editor")
st.write("Apni marzi ka dress, skin color, ya animal add karein.")

# 2. API Setup (Apni Key Yahan Dalein)
API_KEY = "YOUR_GEMINI_API_KEY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Image Upload Option
uploaded_file = st.file_uploader("Apni Image Upload Karein...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Image Display
    image = Image.open(uploaded_file)
    st.image(image, caption="Aapki Uploaded Image", use_container_width=True)

    # 4. Custom Prompt Box (Yahan aap kuch bhi likh sakte hain)
    user_prompt = st.text_input(
        "Kya tabdeeli karni hai?", 
        placeholder="E.g. Change dress to Cyberpunk Armor, make skin blue, add a pet dragon"
    )

    if st.button("Magic Edit ✨"):
        if user_prompt:
            with st.spinner("AI kaam kar raha hai..."):
                try:
                    # AI ko image aur prompt bhejna
                    response = model.generate_content([user_prompt, image])
                    
                    st.subheader("AI ka Jawab:")
                    st.write(response.text)
                    st.info("Note: Gemini 1.5 Flash filhal text/analysis deta hai. Image manipulation ke liye aapko Google ka 'Imagen' model ya API connect karni hogi.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Pehle bataein ke kya change karna hai!")

# --- Styling (Optional) ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #38bdf8;
        color: white;
        border-radius: 10px;
        height: 3em;
    }
</style>
""", unsafe_allow_status=True)
