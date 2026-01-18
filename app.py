import streamlit as st
import google.generativeai as genai
from PIL import Image

# UI Styling (Professional Dark Mode)
st.set_page_config(page_title="BioMorph Pro AI", layout="wide")
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
    .stExpander { border: 1px solid #38bdf8; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("🦁 BioMorph Pro: Humanoid Character Transformer")

# API Setup
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = "YAHAN_APNI_KEY_LIKHEIN"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Main Layout
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("📸 Reference Photo")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)

with col2:
    st.subheader("⚙️ Customization (Inspired by CatStory AI)")
    
    # 1. Humanoid Species
    species_opt = st.selectbox("Select Humanoid Species:", 
                              ["Lion", "Tiger", "Cat", "Wolf", "Panda", "Fox", "Bear", "Custom"])
    final_species = species_opt
    if species_opt == "Custom":
        final_species = st.text_input("Enter Custom Species Name:")

    # 2. Gender & Count Breakdown
    st.markdown("**Character Breakdown (Male/Female/Kittens):**")
    gender_input = st.text_input("e.g. 1 Male, 1 Female, 2 Kittens", placeholder="Enter count and genders...")

    # 3. Dressing (From your link features)
    dress_opt = st.selectbox("Dressing Style:", 
                            ["Royal Golden Armor", "Poor/Ragged Vintage", "Cyberpunk Suite", "Modern Casual", "Custom"])
    final_dress = dress_opt
    if dress_opt == "Custom":
        final_dress = st.text_input("Enter Custom Outfit Detail:")

    # 4. Same Scene Logic (Locking objects and background)
    st.info("Note: Objects (like table, food) and Background will stay identical.")

# Magic Button
if st.button("Generate Transformation ✨"):
    if uploaded_file and gender_input:
        with st.spinner("Transforming into Humanoid..."):
            try:
                # Advanced Prompt for Humanoid Transformation
                prompt = (
                    f"Transform the characters in this image into humanoid {final_species}. "
                    f"Breakdown: {gender_input}. Dressing: {final_dress}. "
                    f"CRITICAL: Keep the exact same poses, camera angle, background, and all objects (like food, table, furniture) unchanged. "
                    f"The result should look like the original scene but with {final_species} people."
                )
                
                response = model.generate_content([prompt, img])
                
                st.markdown("### ✅ Result Logic:")
                st.markdown(f"<div style='color: white; border: 2px solid #10b981; padding: 20px; border-radius: 10px; background-color: #1e293b;'>{response.text}</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please upload an image and fill in the character details!")
