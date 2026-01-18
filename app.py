import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- UI STYLING ---
st.set_page_config(page_title="BioMorph Pro", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #0b0f19; color: white; }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, h1, h2, h3, label, span {
        color: #ffffff !important;
    }
    .stButton>button {
        width: 100%; background: linear-gradient(90deg, #10b981 0%, #3b82f6 100%);
        color: white !important; font-weight: bold; padding: 15px; border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🦁 BioMorph AI: Humanoid Character Transformer")

# --- API SETUP ---
# Secrets se key uthayega
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
else:
    st.error("API Key not found in Secrets!")
    st.stop()

# Force using the stable 1.5-flash model
model = genai.GenerativeModel('gemini-1.5-flash')

# --- LAYOUT ---
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("📸 Step 1: Upload Photo")
    uploaded_file = st.file_uploader("Image select karein", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)

with col2:
    st.subheader("⚙️ Step 2: Customization")
    
    # Character Breakdown
    gender_input = st.text_input("Genders & Count:", placeholder="e.g. 1 Male Lion, 2 Female Kittens")
    
    # Species Dropdown
    species_opt = st.selectbox("Select Animal Species:", ["Lion", "Tiger", "Cat", "Wolf", "Panda", "Fox", "Custom"])
    final_species = species_opt
    if species_opt == "Custom":
        final_species = st.text_input("Enter Custom Species Name:")

    # Dressing
    dress_opt = st.selectbox("Dressing Style:", ["Royal Armor", "Modern Casual", "Cyberpunk", "Ragged", "Custom"])
    final_dress = dress_opt
    if dress_opt == "Custom":
        final_dress = st.text_input("Enter Custom Outfit:")

# --- PROCESSING ---
if st.button("Generate Transformation ✨"):
    if uploaded_file and gender_input:
        with st.spinner("AI is analyzing image and transforming..."):
            try:
                # Instruction to AI
                prompt = (
                    f"ACT AS AN IMAGE EDITOR. Look at the characters in this photo. "
                    f"Replace them with humanoid {final_species}. "
                    f"Breakdown: {gender_input}. Dressing: {final_dress}. "
                    f"Keep the EXACT same poses, background, and objects like food or furniture. "
                    f"Do not change the scene, only transform the characters."
                )
                
                # Model Call
                response = model.generate_content([prompt, img])
                
                st.markdown("### ✅ Analysis Result (White Text):")
                st.markdown(f"<div style='color: white; border: 2px solid #10b981; padding: 20px; border-radius: 10px; background-color: #1e293b;'>{response.text}</div>", unsafe_allow_html=True)
                
            except Exception as e:
                # Agar ab bhi error aaye toh poora error message dikhayega
                st.error(f"Error Details: {e}")
    else:
        st.warning("Please upload image and fill character details.")
