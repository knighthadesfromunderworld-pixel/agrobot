import streamlit as st
import matplotlib.pyplot as plt
from gtts import gTTS
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Agro Twin Dynamic", layout="wide")
st.title("🌱 Agro Twin: Dynamic Soil Intelligence")

# --- TRANSLATIONS ---
translations = {
    "Teak": "தேக்கு மரம்", "Mahogany": "மஹோகனி",
    "Turmeric": "மஞ்சள்", "Groundnut": "நிலக்கடலை",
    "Banana": "வாழை", "Papaya": "பப்பாளி",
    "Fertility": "மண் வளம்", "Recommendation": "பரிந்துரை"
}

# --- INPUT SECTION ---
st.subheader("📍 Real-Time Soil Input")
col1, col2, col3 = st.columns(3)
with col1:
    ph = st.slider("pH Level", 0.0, 14.0, 6.5, step=0.1)
with col2:
    n_val = st.slider("Nitrogen (ppm)", 0, 100, 25)
with col3:
    moisture = st.slider("Moisture %", 0, 100, 40)

# --- DYNAMIC CALCULATION LOGIC ---
# 1. Calculate Fertility Rate (Ideal pH: 6-7, Ideal N > 30)
ph_score = 100 - (abs(6.5 - ph) * 15)
n_score = (n_val / 50) * 100
fertility_rate = min(100, max(0, (ph_score + n_score) / 2))

# 2. Dynamic Plant Suitability
lt = "Teak" if ph > 6.5 else "Mahogany"
st_c = "Turmeric" if n_val > 30 else "Groundnut"
hp = "Banana" if moisture > 50 else "Papaya"

# 3. Dynamic Land Allocation (Changes based on Nitrogen)
# If Nitrogen is high, we give more space to the Cash Crop
p_st = min(50, 20 + (n_val / 2))
p_lt = (100 - p_st) * 0.6
p_hp = 100 - p_st - p_lt

# --- VISUAL DASHBOARD ---
st.divider()
k1, k2 = st.columns([1, 2])

with k1:
    st.metric("Soil Fertility Rate", f"{fertility_rate:.1f}%")
    st.subheader("🌾 Best Combination")
    st.write(f"1. **{lt}** ({translations[lt]})")
    st.write(f"2. **{st_c}** ({translations[st_c]})")
    st.write(f"3. **{hp}** ({translations[hp]})")

    # Voice Generation
    voice_text = f"மண் வளம் {int(fertility_rate)} சதவீதம். சிறந்த பயிர்கள்: {translations[lt]}, {translations[st_c]}, மற்றும் {translations[hp]}."
    if st.button("🔊 Play Advice"):
        tts = gTTS(text=voice_text, lang='ta')
        tts.save("dynamic_voice.mp3")
        st.audio("dynamic_voice.mp3")

with k2:
    tab_bar, tab_pie = st.tabs(["Bar Chart: Nutrient Analysis", "Pie Chart: Land Use"])
    
    with tab_bar:
        # Bar Chart showing pH and Nitrogen vs Ideal
        fig1, ax1 = plt.subplots(figsize=(6, 3))
        ax1.bar(["Sensed pH", "Sensed N"], [ph, n_val/10], color=['#4CAF50', '#2196F3'])
        ax1.axhline(y=6.5, color='r', linestyle='--', label="Target pH")
        st.pyplot(fig1)

    with tab_pie:
        # Pie Chart that moves based on Nitrogen/pH
        fig2, ax2 = plt.subplots(figsize=(6, 3))
        ax2.pie([p_lt, p_st, p_hp], labels=[lt, st_c, hp], autopct='%1.1f%%', colors=['#2e7d32', '#fbc02d', '#d32f2f'])
        st.pyplot(fig2)
