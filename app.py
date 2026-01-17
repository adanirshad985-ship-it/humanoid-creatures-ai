import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Setup
st.set_page_config(page_title="Universal AI Transformer", layout="wide")

# 2. Styling
st.markdown("""
<style>
    .stApp { background-color: #0b172a; color: white; }
    .stSelectbox div div { background-color: #1e293b !important; color: white !important; }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        color: white; border: none; padding: 15px; border-radius: 12px; font-weight: bold; font-size: 18px;
    }
    label { color: #34d399 !important; font-size: 16px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🌍 AI Universal Transformer (Characters, Food & Objects)")

# 3. API Connection Fix
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = "YAHAN_APNI_API_KEY_DAALEIN"

genai.configure(api_key=API_KEY)

# ERROR FIX: Model ka naam yahan change kiya gaya hai
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Main UI Layout
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("📸 Step 1: Reference Image")
    uploaded_file = st.file_uploader("Image upload karein", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Original Pose & Scene", use_container_width=True)

with col2:
    st.subheader("⚙️ Step 2: Customization Panel")
    
    # --- SECTION 1: CHARACTERS ---
    with st.expander("👤 Characters & Genders", expanded=True):
        total_chars = st.number_input("Total Characters kitney hon?", min_value=1, value=3)
        animal_list = ["Custom", "Lion", "Tiger", "Persian Cat", "Orange Tabby", "Husky", "Wolf", "Panda"]
        sel_animal = st.selectbox("Popular Animals:", animal_list)
        char_detail = st.text_input("Genders/Species Details:", placeholder="e.g. 1 Male Lion, 1 Female Tiger, 1 Cub")

    # --- SECTION 2: DRESS & SKIN ---
    with st.expander("👗 Dressing & Appearance"):
        dress_list = ["Custom", "Poor/Ragged", "Royal Armor", "Cyberpunk", "Traditional", "Space Suit"]
        sel_dress = st.selectbox("Dress Style Select Karein:", dress_list)
        custom_dress = st.text_input("Ya custom dress likhein:")
        
        skin_list = ["Custom", "Natural Fur", "White Fur", "Golden", "Metallic", "Neon"]
        sel_skin = st.selectbox("Skin Texture Select Karein:", skin_list)

    # --- SECTION 3: FOOD & INTERNATIONAL OBJECTS ---
    with st.expander("🍲 Food & Objects", expanded=True):
        food_count = st.number_input("Kitney food items/objects hon?", min_value=0, value=2)
        cuisine_list = ["Custom", "American (Burgers/Fries)", "Chinese (Noodles)", "Desi (Biryani/Naan)", "Italian (Pizza)", "Japanese (Sushi)"]
        sel_cuisine = st.selectbox("Cuisine select karein:", cuisine_list)
        custom_objects = st.text_input("Specific Food items (e.g. 2 Pizza boxes, a Coke bottle):")

    extra_details = st.text_area("Mazid details (Background, Mood, etc.)", placeholder="e.g. Rainy night, candles on table")

# 5. Master Prompt & Generation
if st.button("Generate Transformation Logic ✨"):
    if uploaded_file:
        # Handling logic
        final_char = char_detail if sel_animal == "Custom" else f"{total_chars} {sel_animal}s"
        final_dress = custom_dress if sel_dress == "Custom" else sel_dress
        final_food = custom_objects if sel_cuisine == "Custom" else sel_cuisine
        
        with st.spinner("AI is crafting your scene..."):
            try:
                # API Call logic
                response = model.generate_content([
                    f"Task: Pose-to-Image transformation. Characters: {final_char}. Dress: {final_dress}. Food items ({food_count}): {final_food}. Skin: {sel_skin}. Extra: {extra_details}. Keep the same poses as the uploaded photo.", 
                    img
                ])
                st.success("✅ AI Transformation Details Ready!")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Pehle image upload karein!")
