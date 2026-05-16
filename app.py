import streamlit as st
import google.generativeai as genai
import urllib.parse

# १. एपको प्रिमियम लुक र सेटिङ
st.set_page_config(page_title="Denwa Backwater Escape AI", page_icon="🌿", layout="centered")

# २. जेमिनी एआई चाबी सेटिङ (स्ट्रिमलिट सेकेन्ड्सबाट लिने)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ३. रिसोर्ट ब्रान्डिङ र डिजाइन
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    h1, h2, h3 { color: #22c55e !important; font-family: 'Georgia', serif; }
    .stButton>button { background-color: #22c55e; color: white; font-weight: bold; border-radius: 8px; width: 100%; border: none; padding: 12px; }
    .stButton>button:hover { background-color: #16a34a; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 Denwa Backwater Escape")
st.markdown("### 🍸 Luxury AI Mixologist & Guest Assistant")
st.caption("Crafted by Saroj Kumal | Premium Hospitality Experience")

st.markdown("---")

# ४. पाहुनाको विवरण र सामग्री इनपुट
room_number = st.text_input("🚪 Enter Guest Cottage / Table Number:", placeholder="e.g. Cottage 04 वा Table 2")
ingredients = st.text_input("🍓 Enter Ingredients available at the bar:")

# ५. एआई मोडल जाँच्ने फंक्सन
def get_working_model():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    if available_models:
        return genai.GenerativeModel(available_models[0])
    return None

model = get_working_model()

# ६. बटन थिचेपछि जादु सुरु
if st.button("🔮 Craft Luxury Experience"):
    if not room_number:
        st.warning("कृपया अर्डर र सेवाका लागि कटेज वा टेबल नम्बर अनिवार्य राख्नुहोस्!")
    elif not ingredients:
        st.warning("कृपया उपलब्ध सामग्रीहरूको नाम लेख्नुहोस्!")
    elif model:
        with st.spinner("Denwa AI ले रेसिपी र ४K भिजुअल तयार पार्दैछ..."):
            try:
                # जेमिनीबाट प्रिमियम रेसिपी निकाल्ने
                prompt = (
                    f"You are Saroj Kumal, the professional Mixologist at Denwa Backwater Escape Resort. "
                    f"Create a high-end luxury resort-style cocktail or mocktail recipe using these ingredients: {ingredients}. "
                    f"Format it beautifully with measurements, professional steps, and a luxury hospitality garnishing tip."
                )
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.write(response.text)
                
                st.markdown("---")
                
                # 🔥 ४K ULTRA-HD फोटो जेनेरेटर
                st.write("### 📸 Live 4K AI Visual Preview:")
                photo_prompt = f"A professional 4k ultra-hd commercial food photography of a luxury cocktail served in a crystal glass on a rustic wooden bar table at Denwa Backwater Escape luxury nature resort background, dramatic cinematic lighting, photorealistic"
                encoded_prompt = urllib.parse.quote(photo_prompt)
                image_url = f"https://image.pollinations.ai/p/{encoded_prompt}?width=1200&height=900&seed=42&model=flux"
                st.image(image_url, caption="Premium 4K Presentation Preview", use_container_width=True)
                
                st.markdown("---")
                
                # 📲 ह्वाट्सएप अर्डर अलर्ट सिस्टम
                st.write("### 📲 Send Order to Bar / Kitchen")
                whatsapp_message = f"🌿 *NEW DENWA RESORT ORDER!* 🌿\n\n🚪 *Cottage/Table:* {room_number}\n🍓 *Ingredients:* {ingredients}\n\n_Crafted via Denwa AI Framework._"
                encoded_message = urllib.parse.quote(whatsapp_message)
                
                # 🚨 यहाँ आफ्नो वा बारको ह्वाट्सएप नम्बर कन्ट्री कोडसहित (जस्तै ९७७...) राख्न सक्नुहुन्छ
                whatsapp_link = f"https://wa.me/97798XXXXXXXX?text={encoded_message}"
                
                st.markdown(f'''
                    <a href="{whatsapp_link}" target="_blank">
                        <button style="background-color: #25D366; color: white; font-weight: bold; font-size: 16px; border-radius: 8px; width: 100%; border: none; padding: 12px; cursor: pointer;">
                            🟢 Send Order to Bar via WhatsApp
                        </button>
                    </a>
                ''', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.error("AI Model configuration error. Please check your API Key.")

st.markdown("---")
st.caption("© 2026 Denwa Backwater Escape | Digital AI Platform.")
