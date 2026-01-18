import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="BioMorph Debugger", layout="wide")

# UI Styling
st.markdown("<style>html, body, .stMarkdown, p, h1, h2, h3, label {color: white !important;} .stApp {background-color: #0b0f19;}</style>", unsafe_allow_html=True)

# --- DEBUG SECTION ---
st.sidebar.header("🔍 System Debugger")
try:
    if "GEMINI_API_KEY" in st.secrets:
        # API Key ke aakhri 4 digits dikhayega confirm karne ke liye
        key_check = st.secrets["GEMINI_API_KEY"]
        st.sidebar.success(f"API Key Found (Ends with: ...{key_check[-4:]})")
        genai.configure(api_key=key_check)
    else:
        st.sidebar.error("API Key missing in Secrets!")
except Exception as e:
    st.sidebar.error(f"Secret Error: {e}")

# --- THE FIX: Force Stable API ---
# Hum yahan check karenge ke model connect ho raha hai ya nahi
model_name = 'gemini-1.5-flash'
st.sidebar.info(f"Target Model: {model_name}")

try:
    model = genai.GenerativeModel(model_name)
    st.sidebar.success("Model Object Created")
except Exception as e:
    st.sidebar.error(f"Model Init Error: {e}")

# --- MAIN UI ---
st.title("🦁 BioMorph Pro AI")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
gender_input = st.text_input("Genders & Count (e.g. 1 Male Lion)")

if st.button("Generate Transformation ✨"):
    if uploaded_file and gender_input:
        with st.spinner("Processing..."):
            try:
                img = Image.open(uploaded_file)
                # Test call to see version
                st.write("🔄 Sending request to Google...")
                
                prompt = f"Transform characters to humanoid animals. Breakdown: {gender_input}. Same pose."
                response = model.generate_content([prompt, img])
                
                st.markdown("### ✅ Success!")
                st.write(response.text)
                
            except Exception as e:
                # YEH SABSE ZAROORI HAI: Ye batayega ke error v1beta se aa raha hai ya v1 se
                st.error("❗ API Error Detected")
                st.code(f"Error Message: {str(e)}")
                
                if "v1beta" in str(e):
                    st.warning("⚠️ Streamlit is still forcing 'v1beta' internally. Please Delete the app from Streamlit Dashboard and Redeploy.")
                elif "404" in str(e):
                    st.info("💡 Tip: Try changing model to 'gemini-1.5-flash-latest' in the code.")
