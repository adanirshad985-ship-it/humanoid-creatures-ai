import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. UI Styling
st.set_page_config(page_title="BioMorph Pro", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #05070a; color: white; }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, h1, h2, h3, label {
        color: #ffffff !important;
    }
    .stButton>button {
        width: 100%; background: linear-gradient(90deg, #10b981 0%, #3b82f6 100%);
        color: white !important; font-weight: bold; padding: 15px; border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 2. API Configuration (Direct Key Paste)
# Maine aapki key yahan dal di hai
MY_API_KEY = "AIzaSyAYGG0_efV9MBtP_cg11jHkHAYQsWFhciI"
genai.configure(api_key=MY_API_KEY)

# Hum Gemini 1.5 Pro use kar rahe hain for best results
model = genai.GenerativeModel('gemini-1.5-pro')

st.title("🦁 BioMorph: Humanoid Character Transformer")

# 3. Input Section
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📸 Step 1: Image Upload")
    uploaded_file = st.file_uploader("Photo select karein", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)

with col2:
    st.subheader("⚙️ Step 2: Customization")
    
    gender_input = st.text_input("Genders & Count:", placeholder="e.g. 1 Male Lion, 2 Female Cats")
    
    species_opt = st.selectbox("Animal Species:", ["Cat", "Lion", "Tiger", "Wolf", "Panda", "Fox", "Custom"])
    final_species = species_opt
    if species_opt == "Custom":
        final_species = st.text_input("Enter Species Name:")

    dress_opt = st.selectbox("Dressing Style:", ["Modern Casual", "Royal Armor", "Cyberpunk", "Ragged", "Custom"])
    final_dress = dress_opt
    if dress_opt == "Custom":
        final_dress = st.text_input("Enter Outfit Detail:")

# 4. Action & Output
if st.button("Generate Transformation ✨"):
    if uploaded_file and gender_input:
        with st.spinner("AI is working on your story..."):
            try:
                prompt = (
                    f"Analyze this image. Replace the human characters with humanoid {final_species}. "
                    f"Character Breakdown: {gender_input}. Dressing Style: {final_dress}. "
                    f"STRICTLY KEEP: The exact same poses, the same background, and all objects like food or furniture. "
                    f"Describe the new transformed scene in detail where humans are now {final_species}."
                )
                
                response = model.generate_content([prompt, img])
                
                st.markdown("---")
                st.subheader("✅ Transformed Story Results:")
                st.markdown(f"<div style='border: 2px solid #10b981; padding: 20px; border-radius: 10px; background-color: #1e293b;'>{response.text}</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please upload photo and fill details.")
