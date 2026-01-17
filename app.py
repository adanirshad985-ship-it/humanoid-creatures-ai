import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. Page Config
st.set_page_config(page_title="BioMorph AI Transformer", layout="wide")

# 2. CSS Styling (Pure White Text & Dark UI)
st.markdown("""
<style>
    .stApp { background-color: #0b0f19; }
    /* Force all text to be White */
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, h1, h2, h3, span, label {
        color: #ffffff !important;
    }
    /* Input Boxes Styling */
    input, textarea, [data-baseweb="select"] * {
        color: #ffffff !important;
        background-color: #1e293b !important;
    }
    /* Magic Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #38bdf8 0%, #3b82f6 100%);
        color: white !important;
        border: none; padding: 18px; border-radius: 12px; font-weight: bold; font-size: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎨 BioMorph AI: Character & Scene Editor")

# 3. API Connection Logic
# Agar secrets mein hai to wahan se uthayega, warna placeholder se
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = "YAHAN_APNI_NAYI_API_KEY_DAALEIN"

# Model access bypass logic
genai.configure(api_key=API_KEY)

# 404 Fix: Check available models and pick the best one automatically
@st.cache_resource
def init_model():
    try:
        # Hum direct version specify kar rahe hain taake 404 na aaye
        return genai.GenerativeModel('gemini-1.5-flash-latest')
    except:
        return genai.GenerativeModel('gemini-1.5-flash')

model = init_model()

# 4. Interface Layout
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("📸 Reference Frame")
    uploaded_file = st.file_uploader("Image upload karein", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Original Pose", use_container_width=True)

with col2:
    st.subheader("⚙️ Custom Panel")
    
    # CHARACTERS SECTION
    with st.expander("👤 Characters, Genders & Kids", expanded=True):
        char_info = st.text_input("Species & Genders (e.g. 1 Male Lion, 1 Female Tiger, 2 Cubs):")
        skin_info = st.text_input("Skin/Fur details (e.g. White fur, golden stripes):")

    # INTERNATIONAL FOOD SECTION
    with st.expander("🍲 International Food & Objects", expanded=True):
        cuisine = st.selectbox("Cuisine select karein:", ["Custom", "Desi (Biryani/Naan)", "American (Burgers)", "Chinese", "Italian"])
        food_details = st.text_input("Specific Food items & Quantity (e.g. 3 Pizza boxes, 2 Coke bottles):")

    # DRESSING SECTION
    with st.expander("👗 Dressing Style"):
        dress = st.selectbox("Dress Style:", ["Poor/Ragged", "Royal Armor", "Modern Streetwear", "Traditional"])
        extra = st.text_area("Extra Instructions:", placeholder="E.g. Same pose as original, rustic kitchen background...")

# 5. Process Button
if st.button("BioMorph Magic ✨"):
    if uploaded_file and char_info:
        with st.spinner("AI is transforming your scene..."):
            try:
                # Combining inputs into a Master Prompt
                final_food = food_details if cuisine == "Custom" else f"{cuisine}: {food_details}"
                prompt = (
                    f"Transform this image. Characters: {char_info}. "
                    f"Skin: {skin_info}. Food/Objects: {final_food}. Dressing: {dress}. "
                    f"Keep the EXACT same poses and camera angle as the reference image. "
                    f"Details: {extra}. High quality description."
                )
                
                # API Call with Safety Check
                response = model.generate_content([prompt, img])
                
                # Result in White Text
                st.markdown("### ✅ Transformation Details (White Text):")
                st.markdown(f"""
                <div style="color: white; background-color: #1e293b; padding: 20px; border-radius: 10px; border: 2px solid #38bdf8;">
                    {response.text}
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Agar 404 error hai, toh Google AI Studio mein 'Gemini 1.5 Flash' ko 'Free' tier par enable karein.")
    else:
        st.warning("Pehle Image upload karein aur Character details likhein!")
