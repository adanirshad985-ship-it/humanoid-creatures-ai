import streamlit as st

st.set_page_config(page_title="Humanoid AI Creator", layout="wide")

st.title("🐯 Humanoid Creatures AI")
st.sidebar.header("Character Design")

# User Inputs
species = st.sidebar.text_input("Animal Species", "White Tiger")
traits = st.sidebar.text_area("Physical Traits", "Muscular, ice-blue eyes")
outfit = st.sidebar.text_area("Outfit Details", "Tailored midnight blue tuxedo")
pose = st.sidebar.text_area("Pose/Action", "Standing like a boss")
env = st.sidebar.text_area("Background", "Futuristic Cyberpunk city")

if st.sidebar.button("Generate Character"):
    # Creating a rich prompt
    full_prompt = f"Humanoid {species}, {traits}, wearing {outfit}, {pose}, in {env}, cinematic lighting, 8k resolution, masterpiece art."
    
    # Cleaning prompt for URL
    clean_prompt = full_prompt.replace(" ", "%20")
    
    # Using a reliable Image Generation URL (Pollinations)
    image_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width=1024&height=1024&nologo=true"
    
    st.subheader(f"The {species} Humanoid")
    st.image(image_url, caption="Your AI Generated Character")
    st.success("Character Generated Successfully!")
