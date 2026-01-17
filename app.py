import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Config
st.set_page_config(page_title="Pro AI Transformer", layout="wide")

# 2. Styling
st.markdown("""
<style>
    .stApp { background-color: #0b172a; color: white; }
    .stSelectbox div div { background-color: #1e293b !important; color: white !important; border: 1px solid #38bdf8 !important; }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        color: white; border: none; padding: 15px; border-radius: 12px; font-weight: bold; font-size: 18px;
    }
    label { color: #34d399 !important; font-size: 16px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🌍 AI Character & Food Transformer")

# 3. API Connection (Updated Fix)
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = "YAHAN_APNI_API_KEY_LIKHEIN"

genai.configure(api_key=API_KEY)

# FIXED: Model name without 'models/' prefix or versioning issues
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. UI Layout
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("📸 Step 1: Reference Photo")
    uploaded_file = st.file_uploader("Image upload karein", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Original Pose Reference", use_container_width=True)

with col2:
    st.subheader("⚙️ Step 2: Customization Panel")
    
    # CHARACTERS SECTION
    with st.expander("👤 Characters & Genders", expanded=True):
        total_chars = st.number_input("Total Characters?", min_value=1, value=3)
        char_detail = st.text_input("Genders/Species Details:", 
                                   placeholder="e.g. 1 Male Lion, 1 Female Tiger, 1 Cub")

    # DRESSING SECTION
    with st.expander("👗 Appearance & Dressing"):
        dress_list = ["Custom", "Poor/Ragged", "Royal Armor", "Cyberpunk", "Space Suit"]
        sel_dress = st.selectbox("Dress Style:", dress_list)
        custom_dress = st.text_input("Custom Dress Detail (Optional):")
        skin_color = st.text_input("Skin/Fur Color:", placeholder="e.g. Golden, White, Metallic")

    # FOOD & OBJECTS SECTION (NEW!)
    with st.expander("🍲 International Food & Objects", expanded=True):
        food_count = st.number_input("Kitney food items hon?", min_value=0, value=2)
        cuisine_list = ["Custom", "American (Burgers/Fries)", "Chinese (Noodles)", "Desi (Biryani/Naan)", "Italian (Pizza)", "Japanese (Sushi)"]
        sel_cuisine = st.selectbox("Cuisine select karein:", cuisine_list)
        custom_food = st.text_input("Specific Food items:", placeholder="e.g. 2 Pizza boxes, a Coke bottle")

# 5. Master Prompt Logic
if st.button("Generate Transformation ✨"):
    if uploaded_file:
        # Prompt build up
        final_dress = custom_dress if sel_dress == "Custom" else sel_dress
        final_food = custom_food if sel_cuisine == "Custom" else sel_cuisine
        
        with st.spinner("AI is analyzing the scene..."):
            try:
                # Combining everything for Gemini
                prompt = (
                    f"Pose-to-Image Transformation Instruction:\n"
                    f"1. Replace characters with: {char_detail} (Total: {total_chars})\n"
                    f"2. Dressing: {final_dress}\n"
                    f"3. Skin/Fur: {skin_color}\n"
                    f"4. Food/Objects: Replace existing food with {food_count} items of {final_food}\n"
                    f"5. Maintain exactly the same poses and spatial positions as the original photo."
                )
                
                response = model.generate_content([prompt, img])
                st.success("✅ AI Transformation Instructions Ready!")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}. Tip: Check if your API Key is correct.")
    else:
        st.warning("Pehle image upload karein!")
