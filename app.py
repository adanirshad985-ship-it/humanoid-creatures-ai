import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Config
st.set_page_config(page_title="Global AI Transformer", layout="wide")

# 2. Modern UI Styling
st.markdown("""
<style>
    .stApp { background-color: #0f172a; color: white; }
    .stSelectbox div div, .stNumberInput div div, .stTextInput div div { 
        background-color: #1e293b !important; color: white !important; border: 1px solid #38bdf8 !important; 
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #10b981 0%, #3b82f6 100%);
        color: white; border: none; padding: 15px; border-radius: 12px; font-weight: bold;
    }
    label { color: #38bdf8 !important; font-weight: bold; }
    .expander-label { font-size: 20px; font-weight: bold; color: #10b981; }
</style>
""", unsafe_allow_html=True)

st.title("🦁 Universal Character & International Food Editor")

# 3. API Connection with Auto-Fix
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = "YAHAN_APNI_API_KEY_DAALEIN" # Apni key yahan paste karein

genai.configure(api_key=API_KEY)

# --- ERROR 404 AUTO-FIX LOGIC ---
@st.cache_resource
def get_working_model():
    # Hum pehle 1.5 flash try karenge, phir pro vision
    models_to_try = ['gemini-1.5-flash', 'gemini-pro-vision', 'gemini-1.0-pro-vision-latest']
    for m in models_to_try:
        try:
            temp_model = genai.GenerativeModel(m)
            # Chota sa test
            return temp_model
        except:
            continue
    return genai.GenerativeModel('gemini-1.5-flash') # Default

model = get_working_model()

# 4. Interface Layout
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("🖼️ Original Reference")
    uploaded_file = st.file_uploader("Image select karein", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Base Pose Reference", use_container_width=True)

with col2:
    st.subheader("⚙️ Customization Panel")
    
    # CHARACTERS & GENDERS (Multiple options)
    with st.expander("👤 Step 1: Characters & Kids", expanded=True):
        total_chars = st.number_input("Total Characters?", min_value=1, value=3)
        char_detail = st.text_input("Genders/Species Details:", 
                                   placeholder="e.g. 1 Male Lion, 1 Female Tiger, 2 Tiger Cubs (Total 4)")
    
    # DRESSING & SKINS
    with st.expander("👗 Step 2: Dressing & Skin"):
        dress_list = ["Custom", "Poor/Ragged Vintage", "Royal Armor", "Modern Streetwear", "Traditional Indian/Pakistani"]
        sel_dress = st.selectbox("Style:", dress_list)
        custom_dress = st.text_input("Custom Dress Detail (if any):")
        skin_color = st.text_input("Skin/Fur Texture:", placeholder="e.g. White Persian fur, Orange stripes, Golden mane")

    # FOOD & OBJECTS (International Cuisines)
    with st.expander("🍲 Step 3: International Food & Items", expanded=True):
        cuisine_list = ["Custom", "American (Burgers, Fries, Coke)", "Chinese (Noodles, Dumplings)", 
                        "Desi (Biryani, Naan, Karahi)", "Italian (Pizza, Pasta)", "Japanese (Sushi, Ramen)"]
        sel_cuisine = st.selectbox("Cuisine Type:", cuisine_list)
        item_count = st.number_input("Food items ki tadaad?", min_value=1, value=3)
        specific_food = st.text_input("Specific Dishes:", placeholder="e.g. 2 Large Pizzas, 1 Salad bowl, 3 Glass of juice")

# 5. The Magic Button
if st.button("Generate Transformation Logic ✨"):
    if uploaded_file and char_detail:
        final_dress = custom_dress if sel_dress == "Custom" else sel_dress
        final_food = specific_food if sel_cuisine == "Custom" else f"{sel_cuisine}: {specific_food}"
        
        with st.spinner("AI is fixing everything..."):
            try:
                # Combining everything into a Master Prompt
                prompt_text = (
                    f"Pose-to-Image transformation logic:\n"
                    f"1. Replace existing characters with: {char_detail}.\n"
                    f"2. Total count: {total_chars} characters.\n"
                    f"3. Outfit: {final_dress}.\n"
                    f"4. Skin details: {skin_color}.\n"
                    f"5. REPLACE ALL FOOD/OBJECTS with: {item_count} items of {final_food}.\n"
                    f"6. Keep the exact same poses, camera angle, and rustic background."
                )
                
                response = model.generate_content([prompt_text, img])
                st.success("✅ AI Logic Ready!")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Check if your API Key is restricted to certain models in Google AI Studio.")
    else:
        st.warning("Pehle Image aur Character details bharein!")
