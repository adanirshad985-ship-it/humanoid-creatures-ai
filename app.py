import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="AI Character Transformer", layout="wide")

# 2. Professional UI Styling (CSS)
st.markdown("""
<style>
    .stApp { background-color: #0f172a; color: white; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #38bdf8 !important;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #38bdf8 0%, #0ea5e9 100%);
        color: white;
        border: none;
        padding: 15px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 18px;
    }
    label { color: #38bdf8 !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🦁 Private AI Character Tool")
st.write("Apni marzi ke characters aur dressing set karein.")

# 3. API Key Management
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = "YAHAN_APNI_API_KEY_LIKHEIN"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Main Layout (Two Columns)
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("🖼️ Step 1: Upload Pose Reference")
    uploaded_file = st.file_uploader("Image select karein", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Reference Image", use_container_width=True)

with col2:
    st.subheader("⚙️ Step 2: Customization Boxes")
    
    # Blank Boxes as requested
    total_chars = st.number_input("Total Characters kitney hain?", min_value=1, value=3)
    
    animals_input = st.text_input("Characters/Animals", 
                                 placeholder="E.g. Male Lion, Female Tiger, Tiger Cub")
    
    gender_input = st.text_input("Genders (Order wise)", 
                                placeholder="E.g. Male, Female, Male Child")
    
    dress_input = st.text_input("Dressing Style", 
                               placeholder="E.g. Poor type, ragged vintage coats, old boots")
    
    color_input = st.text_input("Skin/Fur/Color", 
                               placeholder="E.g. Natural fur colors, golden mane, metallic skin")
    
    extra_details = st.text_area("Mazid details (Background etc.)", 
                                 placeholder="E.g. Same pose as original, rustic kitchen background")

# 5. Process Button
if st.button("Generate AI Magic ✨"):
    if uploaded_file and animals_input:
        with st.spinner("AI aapki details process kar raha hai..."):
            try:
                # Combining all boxes into one Master Prompt
                final_prompt = f"""
                Strict Instruction: I am providing an image for pose reference. 
                Task: Recreate this scene with exactly {total_chars} characters.
                Character Types: {animals_input}.
                Genders: {gender_input}.
                Dress Code: {dress_input}.
                Skin/Color: {color_input}.
                Environment & Pose: {extra_details}. Keep the poses identical to the image.
                """
                
                # Gemini Processing
                response = model.generate_content([final_prompt, img])
                
                st.success("✅ AI Analysis & Prompt Ready:")
                st.write(response.text)
                
                st.info("💡 Note: Yeh tool filhal Gemini 1.5 Flash use kar raha hai jo text details deta hai. Asli image generate karne ke liye Imagen-3 API connect karni hogi.")
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Pehle image upload karein aur kam az kam 'Animals' ka box bharain.")
