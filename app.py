import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="AI Universal Transformer", layout="wide")

# 2. CSS Styling (Pure White Text & Dark Theme)
st.markdown("""
<style>
    /* Dark Theme Background */
    .stApp { background-color: #0b0f19; }
    
    /* Global White Text */
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, h1, h2, h3 {
        color: #ffffff !important;
    }
    
    /* Input Box Text Color */
    input, textarea, [data-baseweb="select"] * {
        color: #ffffff !important;
        background-color: #1e293b !important;
    }

    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: #1e293b !important;
        color: white !important;
        border-radius: 10px;
    }

    /* Magic Button Styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #38bdf8 0%, #3b82f6 100%);
        color: white !important;
        border: none;
        padding: 18px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 20px;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.3);
    }
</style>
""", unsafe_allow_html=True)

st.title("🦁 Universal AI Character & Food Tool")

# 3. API Setup (Force Stable Version to fix 404)
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = "YAHAN_APNI_API_KEY_DAALEIN"

# IMPORTANT: v1 endpoint use karna hai taake 404 error na aaye
genai.configure(api_key=API_KEY)

# Model Initialization
try:
    # Force stable model name
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Model Init Error: {e}")

# 4. Interface Layout
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("📸 Upload Reference Image")
    uploaded_file = st.file_uploader("Image select karein", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Original Pose Reference", use_container_width=True)

with col2:
    st.subheader("⚙️ Transformation Panel")
    
    # CHARACTERS SECTION
    with st.expander("👤 Characters, Genders & Kids", expanded=True):
        total_chars = st.number_input("Total Characters?", min_value=1, value=3)
        char_detail = st.text_input("Genders/Species Details:", 
                                   placeholder="e.g. 1 Male Lion, 1 Female Tiger, 2 Tiger Cubs")
    
    # DRESSING & SKINS
    with st.expander("👗 Dressing & Appearance"):
        dress_list = ["Custom", "Poor/Ragged Vintage", "Royal Golden Armor", "Modern Streetwear", "Traditional"]
        sel_dress = st.selectbox("Style Select Karein:", dress_list)
        custom_dress = st.text_input("Custom Dress Detail (Agar kuch khas ho):")
        skin_color = st.text_input("Skin/Fur details:", placeholder="e.g. White fur, Orange stripes")

    # FOOD SECTION
    with st.expander("🍲 International Food & Objects", expanded=True):
        cuisine_list = ["Custom", "American (Burgers & Fries)", "Chinese (Noodles)", "Desi (Biryani & Karahi)", "Italian (Pizza)"]
        sel_cuisine = st.selectbox("Cuisine Type:", cuisine_list)
        food_items = st.text_input("Specific Dishes & Items:", placeholder="e.g. 3 Pizza boxes, 2 Coke bottles")

# 5. The Final Process
if st.button("Generate Transformation Logic ✨"):
    if uploaded_file and char_detail:
        final_dress = custom_dress if sel_dress == "Custom" else sel_dress
        final_food = food_items if sel_cuisine == "Custom" else f"{sel_cuisine}: {food_items}"
        
        with st.spinner("AI is processing (Safe Mode)..."):
            try:
                # Making the Prompt
                prompt_text = (
                    f"Pose-to-Image Transformation Logic.\n"
                    f"Reference: Use uploaded image for POSES ONLY.\n"
                    f"New Characters: {char_detail} (Total: {total_chars}).\n"
                    f"Dress: {final_dress}.\n"
                    f"Skin: {skin_color}.\n"
                    f"Table Objects: Replace existing food with {final_food}.\n"
                    f"Background: Keep the same rustic kitchen style."
                )
                
                # API Call
                response = model.generate_content([prompt_text, img])
                
                st.markdown("### ✅ Result (Stable Output):")
                # Showing result in a white-text box
                st.markdown(f"""
                <div style="color: white; background-color: #1e293b; padding: 20px; border-radius: 10px; border: 1px solid #38bdf8;">
                    {response.text}
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error encountered: {e}")
                st.info("Check if your API Key is correctly set in Streamlit Secrets.")
    else:
        st.warning("Pehle image upload karein aur details fill karein!")
