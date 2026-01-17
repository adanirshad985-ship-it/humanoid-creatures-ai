import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Config
st.set_page_config(page_title="BioMorph AI Transformer", layout="wide")

# 2. CSS Styling (Pure White Text & Dark UI)
st.markdown("""
<style>
    .stApp { background-color: #0b0f19; }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, h1, h2, h3, span, label {
        color: #ffffff !important;
    }
    input, textarea, [data-baseweb="select"] * {
        color: #ffffff !important;
        background-color: #1e293b !important;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #38bdf8 0%, #3b82f6 100%);
        color: white !important;
        border: none; padding: 18px; border-radius: 12px; font-weight: bold; font-size: 20px;
    }
    .stExpander { border: 1px solid #38bdf8; border-radius: 10px; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("🎨 BioMorph AI: Scene & Character Editor")

# 3. API Connection Logic (v1 Stable Force)
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = "YAHAN_APNI_NAYI_API_KEY_DAALEIN"

# API Configuration
genai.configure(api_key=API_KEY)

# 404 Fix: Model Selection
@st.cache_resource
def load_stable_model():
    # Direct model string to avoid discovery errors
    return genai.GenerativeModel('gemini-1.5-flash')

model = load_stable_model()

# 4. Interface Layout
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("📸 Reference Image")
    uploaded_file = st.file_uploader("Image upload karein", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Original Pose Reference", use_container_width=True)

with col2:
    st.subheader("⚙️ Customization Panel")
    
    with st.expander("👤 Characters & Genders", expanded=True):
        char_info = st.text_input("Genders & Species:", placeholder="e.g. 1 Male Lion, 2 Female Tigers, 3 Cubs")
        skin_info = st.text_input("Skin/Fur details:", placeholder="e.g. White fur, golden eyes")

    with st.expander("🍲 International Food & Objects", expanded=True):
        cuisine = st.selectbox("Cuisine:", ["Custom", "Desi (Biryani/Naan)", "American (Burgers)", "Chinese", "Italian"])
        food_details = st.text_input("Specific Dishes & Quantity:", placeholder="e.g. 2 Large Pizzas, 3 Drinks")

    with st.expander("👗 Appearance & Dressing"):
        dress = st.selectbox("Dress Style:", ["Poor/Ragged", "Royal Armor", "Modern", "Traditional"])
        extra = st.text_area("Extra Details:", placeholder="Background, Lighting, or specific mood...")

# 5. Process Button
if st.button("BioMorph Magic ✨"):
    if uploaded_file and char_info:
        with st.spinner("AI is transforming..."):
            try:
                final_food = food_details if cuisine == "Custom" else f"{cuisine}: {food_details}"
                prompt = (
                    f"Transform this image. Characters: {char_info}. "
                    f"Skin: {skin_info}. Food/Objects: {final_food}. Dressing: {dress}. "
                    f"Strictly keep the EXACT same poses and camera angle as the reference image. "
                    f"Provide a high-quality visual description."
                )
                
                response = model.generate_content([prompt, img])
                
                st.markdown("### ✅ Result (White Text):")
                st.markdown(f"""
                <div style="color: white; background-color: #1e293b; padding: 20px; border-radius: 10px; border: 2px solid #38bdf8;">
                    {response.text}
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Check your API Key in Streamlit Secrets.")
    else:
        st.warning("Pehle Image upload karein aur Character details likhein!")
