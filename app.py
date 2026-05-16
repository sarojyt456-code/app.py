import streamlit as st
import google.generativeai as genai
import urllib.parse

# १. एपको लक्जरी सेटिङ
st.set_page_config(page_title="Denwa Backwater Escape AI", page_icon="🌿", layout="centered")

# २. जेमिनी एआई चाबी कन्फिगर
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ३. प्रिमियम रिसोर्ट थिम डिजाइन
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    h1, h2, h3 { color: #22c55e !important; font-family: 'Georgia', serif; }
    .stButton>button { background-color: #22c55e; color: white; font-weight: bold; border-radius: 8px; width: 100%; border: none; padding: 12px; }
    .stButton>button:hover { background-color: #16a34a; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 Denwa Backwater Escape")
st.markdown("### 🍸 Luxury AI Mixologist & Menu Assistant")
st.caption("Designed by Saroj Kumal | Head of Beverage Experience")

st.markdown("---")

# ४. कोठा, ट्री हाउस, स्ट्यान्डर्ड रुम र टेबलको आधिकारिक लिस्ट
room_options = ["Select Cottage / Room / Table"]
for i in range(1, 9): room_options.append(f"🏠 Cottage {i:02d}")
room_options.extend(["🌲 Tree House 09", "🌲 Tree House 10"])
room_options.extend(["🛏️ Standard Room 11", "🛏️ Standard Room 12", "🛏️ Standard Room 14", "🛏️ Standard Room 15"])
for i in range(1, 6): room_options.append(f"🍽️ Dining Table {i}")

selected_room = st.selectbox("🚪 Select Guest Location / Room:", room_options)

st.markdown("---")

# ५. सर्भिस मोड (मेनुका ४ वटा पाना र एआई जेनेरेटर)
st.write("## 📜 Digital Bar & Beverage Menu")
menu_type = st.selectbox("Choose Category:", [
    "--- Select Category ---",
    "🍹 Denwa House Cocktails",
    "🥤 Mocktails & Coolers",
    "☕ Fresh Brew & Soft Drinks",
    "🥃 Straight Drinks (Premium Liquor)",
    "🔮 AI Custom Cocktail/Mocktail Generator"
])

recipe_title = ""
search_trigger = False
ingredients_used = ""
base_price = 0
is_corkage = False

# --- ककटेल मेनु (पाना २ को हुबहु रेट) ---
if menu_type == "🍹 Denwa House Cocktails":
    cocktail = st.selectbox("Select Cocktail:", [
        "Select Drink",
        "Gauva Chilli Sour - INR 850",
        "Ginto - INR 850",
        "Bees Knees - INR 850",
        "Sip & Smile - INR 800",
        "Beet Ginger Whisper - INR 800",
        "Classic Mojito - INR 750",
        "Screwdriver - INR 750",
        "Jungle Toddy - INR 750",
        "Leopard Paw - INR 750",
        "Bloody Mary - INR 750",
        "Picante - INR 750",
        "Cuba Libre - INR 750",
        "Gauva Martini - INR 650",
        "Mahua Bloom - INR 650"
    ])
    if cocktail != "Select Drink":
        recipe_title = cocktail.split(" - ")[0]
        base_price = int(cocktail.split(" - ")[1].replace("INR ", ""))
        ingredients_used = recipe_title
        search_trigger = st.button("Order Cocktail")

# --- मकटेल मेनु (पाना ३ को हुबहु रेट) ---
elif menu_type == "🥤 Mocktails & Coolers":
    mocktail = st.selectbox("Select Mocktail / Cooler:", [
        "Select Drink",
        "Ginger Limeade - INR 450",
        "Virgin Coco Colada - INR 450",
        "Melon Basil Cooler - INR 450",
        "Sunset Glory - INR 450",
        "Virgin Mary - INR 450",
        "Virgin Mojito - INR 450",
        "Chilli Amrud - INR 450",
        "Pomegranate Mint Sparkle - INR 450"
    ])
    if mocktail != "Select Drink":
        recipe_title = mocktail.split(" - ")[0]
        base_price = int(mocktail.split(" - ")[1].replace("INR ", ""))
        ingredients_used = recipe_title
        search_trigger = st.button("Order Mocktail")

# --- कफी र सफ्ट ड्रिंक्स (पाना ३ को हुबहु रेट) ---
elif menu_type == "☕ Fresh Brew & Soft Drinks":
    soft = st.selectbox("Select Beverage:", [
        "Select Drink",
        "Fresh Brew: Cold Coffee - INR 350",
        "Fresh Brew: Ice Latte - INR 350",
        "Fresh Brew: Iced Coffee Lemonade - INR 350",
        "Fresh Brew: Affogato - INR 350",
        "Fresh Brew: Phoenix Fantasy - INR 350",
        "Fresh Brew: Coffee Tonic - INR 350",
        "Fresh Fruit Juice - INR 300",
        "Homemade Iced Tea - INR 300",
        "Choice of Smoothies - INR 300",
        "Himalayan Sparkling Water - INR 300",
        "Tonic Water / Gingerale - INR 250",
        "Flavoured Lassi - INR 250",
        "Fresh Lime Soda - INR 250",
        "Himalaya Still Mineral Water - INR 250",
        "Soft Drinks / Soda - INR 200",
        "Bottled Water - INR 100"
    ])
    if soft != "Select Drink":
        recipe_title = soft.split(" - ")[0]
        base_price = int(soft.split(" - ")[1].replace("INR ", ""))
        ingredients_used = recipe_title
        search_trigger = st.button("Order Beverage")

# --- हार्ड ड्रिंक्स मेनु (पाना १ को हुबहु रेट र कर्कवेज) ---
elif menu_type == "🥃 Straight Drinks (Premium Liquor)":
    liquor = st.selectbox("Select Premium Liquor:", [
        "Select Drink",
        "Jacob's Creek (Red/White Bottle) - INR 4000",
        "Sula (Red/White Bottle) - INR 3500",
        "Taliskar X-Yrs - INR 900",
        "The Glenlivet XII-Yrs - INR 900",
        "The Glenfedich XII-Yrs - INR 900",
        "Imported Beer (650 ML) - INR 700",
        "Grey Goose Vodka - INR 700",
        "Indri (Indian Single Malt) - INR 700",
        "Amrut Amalgum (Indian Single Malt) - INR 700",
        "Indian Beer (650 ML) - INR 650",
        "Chivas Regal XII-Yrs - INR 600",
        "JW Black Label XII-Yrs - INR 600",
        "Bombay Sapphire (London Dry Gin) - INR 600",
        "JW Red Label - INR 555",
        "Teacher's 50 - INR 555",
        "Ballantine - INR 555",
        "Absolut Vodka - INR 500",
        "Jaisalmer (Indian Craft Gin) - INR 500",
        "Tanqueray (London Dry Gin) - INR 500",
        "Jameson Irish - INR 500",
        "100-Pipers - INR 450",
        "Smirnoff Vodka - INR 400",
        "Bacardi White Rum - INR 400",
        "Bacardi Black Rum - INR 400",
        "Morpheus XO (Indian Brandy) - INR 400",
        "Camino (Tequila) - INR 400",
        "Old Monk - INR 300",
        "Mahulo (Heritage Mahua Liquor) - INR 300",
        "🍾 [BYOB] Bring Your Own Bottle (Corkage Charge)"
    ])
    if liquor != "Select Drink":
        if "[BYOB]" in liquor:
            recipe_title = "Guest Own Bottle Service (Corkage)"
            # मेनु अनुसार: बियर ३००, वाइन १०००, अन्य रक्सी २००० कर्कवेज लाग्ने नियम
            corkage_type = st.radio("Select Bottle Type for Corkage:", ["Beer (INR 300)", "Wine (INR 1000)", "Other Liquor (INR 2000)"])
            if "Beer" in corkage_type: base_price = 300
            elif "Wine" in corkage_type: base_price = 1000
            else: base_price = 2000
            is_corkage = True
        else:
            recipe_title = liquor.split(" - ")[0]
            base_price = int(liquor.split(" - ")[1].replace("INR ", ""))
        ingredients_used = recipe_title
        search_trigger = st.button("Order Straight Drink")

# --- एआई कस्टम जेनेरेटर ---
elif menu_type == "🔮 AI Custom Cocktail/Mocktail Generator":
    st.write("### 🍓 AI Custom Creation")
    custom_ingredients = st.text_input("Enter available ingredients (e.g., Vodka, Mint, Lime):")
    if st.button("Craft Unique AI Recipe"):
        if custom_ingredients:
            recipe_title = f"Custom AI Creation with {custom_ingredients}"
            ingredients_used = custom_ingredients
            base_price = 750  # एआई कस्टमाइजेसनको एउटा एभरेज रेट सेट गरिएको
            search_trigger = True
        else:
            st.warning("कृपया एआई रेसिपीका लागि सामग्रीहरूको नाम लेख्नुहोस्!")

# ६. एआई प्रोसेसिङ र ४K फोटो जेनेरेसन
def get_working_model():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    if available_models: return genai.GenerativeModel(available_models[0])
    return None

model = get_working_model()

if search_trigger:
    if selected_room == "Select Cottage / Room / Table":
        st.error("🚨 कृपया अर्डर अगाडि बढाउन पाहुनाको कटेज, रुम वा टेबल नम्बर सेलेक्ट गर्नुहोस्!")
    elif model:
        with st.spinner("Processing your order & premium visuals..."):
            try:
                # ट्याक्स र टोटल हिसाब (१०% सर्भिस चार्ज र ५% भ्याट जस्तै गरी एउटा स्ट्यान्डर्ड रिसोर्ट ट्याक्स सेट गरिएको)
                estimated_tax = round(base_price * 0.15, 2)
                total_price = round(base_price + estimated_tax, 2)

                # जेमिनी प्रम्प्ट
                prompt = (
                    f"You are Saroj Kumal, the professional Mixologist at Denwa Backwater Escape Luxury Resort. "
                    f"Provide a premium presentation description, taste notes, and elite serving standard for: '{recipe_title}'. "
                    f"Always maintain a luxury hospitality tone."
                )
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.write(response.text)
                
                # --- बिलिङ बक्स ---
                st.markdown("### 📊 Order Billing Details (INR)")
                col1, col2, col3 = st.columns(3)
                col1.metric("Base Price", f"₹ {base_price}")
                col2.metric("Estimated Taxes", f"₹ {estimated_tax}")
                col3.metric("Total Bill Amount", f"₹ {total_price}")
                
                if is_corkage:
                    st.warning("⚠️ यो शुल्क रिसोर्टको Corkage Policy अनुसार बोतल खोले बापत मात्र लगाइएको हो।")
                st.markdown("---")
                
                # ४K ULTRA-HD फोटो जेनेरेटर
                st.write("### 📸 Live 4K Presentation Preview:")
                photo_prompt = f"A high-end 4k ultra-hd professional commercial food photography of {ingredients_used}, served in luxury glass on a premium rustic nature resort bar counter, cinematic light, photorealistic"
                encoded_prompt = urllib.parse.quote(photo_prompt)
                image_url = f"https://image.pollinations.ai/p/{encoded_prompt}?width=1200&height=900&seed=88&model=flux"
                st.image(image_url, caption=f"Premium 4K Visualization", use_container_width=True)
                
                st.markdown("---")
                
                # 📲 ह्वाट्सएप अर्डर अलर्ट
                st.write("### 📲 Dispatch Order to Bar Counter")
                whatsapp_message = f"🌿 *NEW DENWA RESORT ORDER!* 🌿\n\n🚪 *Location:* {selected_room}\n🍹 *Item:* {recipe_title}\n💰 *Base Price:* ₹{base_price}\n✨ *Est. Tax:* ₹{estimated_tax}\n💵 *Total Bill:* ₹{total_price}\n\n_Managed via Denwa AI Framework._"
                encoded_message = urllib.parse.quote(whatsapp_message)
                
                whatsapp_link = f"https://wa.me/918305020237?text={encoded_message}"
                
                st.markdown(f'''
                    <a href="{whatsapp_link}" target="_blank">
                        <button style="background-color: #25D366; color: white; font-weight: bold; font-size: 16px; border-radius: 8px; width: 100%; border: none; padding: 12px; cursor: pointer;">
                            🟢 Send Bill & Order Ticket to Bar (+918305020237)
                        </button>
                    </a>
                ''', unsafe_allow_html=True)
                
                # 💳 क्युआर कोड पेमेन्ट सेक्सन
                st.markdown("---")
                st.write("### 💳 Digital Quick Payment (QR Code)")
                st.info("पाहुनाहरूले बिल भुक्तानी गर्न यो क्युआर कोड स्क्यान गर्न सक्नुहुन्छ:")
                qr_image_url = "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=DenwaBackwaterEscape"
                st.image(qr_image_url, caption="Scan to Pay - Denwa Backwater Escape", width=250)
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.error("AI Configuration Error. Please contact support.")

st.markdown("---")
st.caption("© 2026 Denwa Backwater Escape | Digital AI Platform v4.0")
