import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Config
st.set_page_config(page_title="AI Master Editor", layout="wide")

# 2. CSS Styling (Text ko White karne ke liye)
st.markdown("""
<style>
    /* Main Background */
    .stApp { background-color: #0f172a; color: white; }
    
    /* All Text and Labels to White */
    h1, h2, h3, p, label, .stMarkdown, .stText {
        color: white !important;
    }
    
    /* Input Boxes Text Color */
    input, textarea, .stSelectbox div div {
        color: white !important;
        background-color: #1e293b !important;
    }

    /* AI Output Box styling */
    .stWrite, .stSuccess {
        color: white !important;
        background-color: #1e293b;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #38bdf8;
    }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #10b981 0%, #3b82f6 100%);
        color: white !important;
        border: none;
        padding: 15px;
        border-radius: 12px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌍 AI Universal Character & Food Editor")

# 3. API Connection with Safe Model Picker
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = "YAHAN_APNI_API_KEY_DAALEIN"

genai.configure(api_key=API_KEY)

def get_available_model():
    try:
        # Check models for current API key
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'gemini-1.5-flash' in m.name:
                    return genai.GenerativeModel('gemini-1.5-flash')
        return genai.GenerativeModel('gemini-1.5-flash')
    except:
        return genai.GenerativeModel('gemini-1.5-flash')

model = get_available_model()

# 4. Interface Layout
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("📸 Reference Frame")
    uploaded_file = st.file_uploader("Image upload karein", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Original Pose Reference", use_container_width=True)

with col2:
    st.subheader("⚙️ Customization Panel")
    
    # CHARACTERS SECTION
    with st.expander("👤 Characters, Genders & Kids", expanded=True):
        total_chars = st.number_input("Total Characters?", min_value=1, value=3)
        char_detail = st.text_input("Genders/Species Details:", 
                                   placeholder="e.g. 1 Male Lion, 1 Female Tiger, 2 Tiger Cubs")
    
    # DRESSING SECTION
    with st.expander("👗 Dressing & Skins"):
        dress_list = ["Custom", "Poor/Ragged Vintage", "Royal Golden Armor", "Modern Streetwear", "Traditional"]
        sel_dress = st.selectbox("Style:", dress_list)
        custom_dress = st.text_input("Custom Dress Detail:")
        skin_color = st.text_input("Skin/Fur details:", placeholder="e.g. White fur, orange stripes")

    # FOOD SECTION
    with st.expander("🍲 International Food & Objects", expanded=True):
        cuisine_list = ["Custom", "American (Burgers)", "Chinese (Noodles)", "Desi (Biryani)", "Italian (Pizza)"]
        sel_cuisine = st.selectbox("Cuisine Type:", cuisine_list)
        food_items = st.text_input("Specific Dishes & Quantity:", placeholder="e.g. 3 Pizza boxes, 2 Coke bottles")

# 5. Process Button
if st.button("Generate Transformation Logic ✨"):
    if uploaded_file and char_detail:
        final_dress = custom_dress if sel_dress == "Custom" else sel_dress
        final_food = food_items if sel_cuisine == "Custom" else f"{sel_cuisine}: {food_items}"
        
        with st.spinner("AI is thinking..."):
            try:
                prompt_text = (
                    f"Pose-to-Image Transformation.\n"
                    f"Characters: {char_detail} (Total: {total_chars}).\n"
                    f"Dressing: {final_dress}.\n"
                    f"Skin: {skin_color}.\n"
                    f"Food/Objects: {final_food}.\n"
                    f"Keep exact poses and rustic background."
                )
                
                response = model.generate_content([prompt_text, img])
                
                # Yeh hissa ab Pure White text mein dikhayi dega
                st.markdown("### ✅ AI Result (White Text):")
                st.markdown(f"<div style='color: white; border: 1px solid #38bdf8; padding: 10px; border-radius: 5px;'>{response.text}</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Pehle image aur details fill karein!")
