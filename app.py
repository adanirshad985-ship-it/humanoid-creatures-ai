import streamlit as st
from google import genai

# --- Tool Setup ---
st.set_page_config(page_title="Humanoid Pro Lab", layout="wide")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("Secrets mein API Key missing hai!")
    st.stop()

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🎭 Professional Humanoid Character Creator")
st.markdown("Yeh tool aapki details ko aik high-end cinematic prompt mein convert karta hai.")

# --- Detail Inputs ---
with st.sidebar:
    st.header("🎨 Style & Quality")
    art_style = st.selectbox("Art Style", ["Cinematic 3D", "Disney Pixar Style", "Hyper-Realistic", "Anime/Manga"])
    lighting = st.selectbox("Lighting", ["Golden Hour", "Cyberpunk Neon", "Studio Portrait", "Soft Sunlight"])
    resolution = "8k resolution, highly detailed, masterwork, unreal engine 5 render"

# Main Form for Full Details
with st.form("character_form"):
    st.subheader("Character Deep Details")
    col1, col2 = st.columns(2)
    
    with col1:
        animal_type = st.text_input("Animal Species", placeholder="e.g. Snow Leopard, Golden Retriever")
        outfit_detail = st.text_area("Outfit Details (Material, Color, Style)", placeholder="e.g. Wearing a silk royal sherwani with gold embroidery and a matching turban")
    
    with col2:
        physical_traits = st.text_input("Physical Traits", placeholder="e.g. Deep blue eyes, muscular build, scar on left ear")
        pose_action = st.text_input("Pose/Action", placeholder="e.g. Standing confidently holding a staff, looking at the camera")

    scene_detail = st.text_input("Background & Environment", placeholder="e.g. Inside an ancient Mughal palace with marble floors and lanterns")

    submit = st.form_submit_button("Generate Professional Humanoid")

# --- Processing & Generation ---
if submit:
    with st.spinner("Analyzing details and generating masterpiece..."):
        # Yahan hum Gemini ko detail de rahe hain ke wo "Pro Prompt" banaye
        full_detailed_prompt = f"""
        TASK: Create a professional humanoid {animal_type} character.
        CHARACTER SPECS: Standing on two legs, human-like anatomy but keeping animal features. 
        PHYSICAL: {physical_traits}.
        CLOTHING: {outfit_detail}.
        ACTION: {pose_action}.
        ENVIRONMENT: {scene_detail}.
        STYLE: {art_style} with {lighting} lighting. 
        TECHNICAL: {resolution}, intricate textures, sharp focus, cinematic composition.
        """
        
        try:
            response = client.models.generate_image(
                model="imagen-3.0-generate-001",
                prompt=full_detailed_prompt
            )
            st.image(response.images[0], caption=f"Detailed Humanoid {animal_type}", use_container_width=True)
            st.success("Masterpiece Generated!")
        except Exception as e:
            st.error(f"Error: {e}")
