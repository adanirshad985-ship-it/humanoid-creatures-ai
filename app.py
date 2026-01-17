import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Config & Pure White Text Styling
st.set_page_config(page_title="BioMorph AI", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0b0f19; }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, h1, h2, h3, label, span {
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

# 2. API Setup (Zero-Error Version)
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = "YAHAN_APNI_NEW_KEY_LIKHEIN"

genai.configure(api_key=API_KEY)

# Force stable model call to avoid 404
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# 3. Main Interface
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("📸 Step 1: Reference Photo")
    uploaded_file = st.file_uploader("Original image upload karein", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)

with col2:
    st.subheader("⚙️ Step 2: Custom Options")
    
    # Character Details (Multiple: Male, Female, Kitten)
    st.markdown("**Genders & Count:**")
    gender_details = st.text_input("Details likhein:", placeholder="e.g. 1 Male, 1 Female, 2 Kittens")
    
    # Animal Selection
    animal_opt = st.selectbox("Animal:", ["Lion", "Tiger", "Cat", "Dog", "Wolf", "Panda", "Custom"])
    final_animal = animal_opt
    if animal_opt == "Custom":
        final_animal = st.text_input("Enter Animal Name:")

    # Dressing
    dress_opt = st.selectbox("Dressing Style:", ["Royal Armor", "Poor/Ragged", "Space Suit", "Modern", "Custom"])
    final_dress = dress_opt
    if dress_opt == "Custom":
        final_dress = st.text_input("Enter Dressing Style:")

# 4. Process Button
if st.button("BioMorph Magic ✨"):
    if uploaded_file and gender_details:
        with st.spinner("AI is transforming..."):
            try:
                # Prompt Building
                prompt = (
                    f"Task: Replace characters in this image with {final_animal}. "
                    f"Breakdown: {gender_details}. Dressing: {final_dress}. "
                    f"Keep the exact poses and positions from the reference photo."
                )
                
                # API Call
                response = model.generate_content([prompt, img])
                
                st.markdown("### ✅ Result:")
                st.markdown(f"""
                <div style="color: white; border: 2px solid #38bdf8; padding: 20px; border-radius: 10px; background-color: #1e293b;">
                    {response.text}
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Tip: Make sure your API key is correct in Streamlit Secrets.")
    else:
        st.warning("Pehle image aur details mukammal karein!")
