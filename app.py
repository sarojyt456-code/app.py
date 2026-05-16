import streamlit as st
import google.generativeai as genai
import urllib.parse
import datetime

# १. एपको लक्जरी सेटिङ
st.set_page_config(page_title="Wild Forest Mixology", page_icon="🌿", layout="centered")

# २. जेमिनी एआई चाबी कन्फिगर
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ३. प्रिमियम रिसोर्ट थिम डिजाइन
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    h1, h2, h3 { color: #22c55e !important; font-family: 'Georgia', serif; }
    .stButton>button { background-color: #22c55e; color: white; font-weight: bold; border-radius: 8px; width: 100%; border: none; padding: 12px; cursor: pointer; }
    .stButton>button:hover { background-color: #16a34a; }
    .dispatch-btn>button { background-color: #e11d48 !important; }
    .dispatch-btn>button:hover { background-color: #be123c !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 Denwa Backwater Escape")
st.markdown("### 🍸 Denwa Forest-to-Glass Luxury AI Assistant")
st.caption("Designed by Saroj Kumal | Head of Beverage Experience")

st.markdown("---")

# ४. कोठा र टेबलको आधिकारिक लिस्ट
room_options = ["Select Cottage / Room / Table"]
for i in range(1, 9): room_options.append(f"🏠 Cottage {i:02d}")
room_options.extend(["🌲 Tree House 09", "🌲 Tree House 10"])
room_options.extend(["🛏️ Standard Room 11", "🛏️ Standard Room 12", "🛏️ Standard Room 14", "🛏️ Standard Room 15"])
for i in range(1, 6): room_options.append(f"🍽️ Dining Table {i}")

selected_room = st.selectbox("🚪 Select Guest Location / Room:", room_options)

st.markdown("---")

# ५. सर्भिस मोड (मेनुका क्याटगोरीहरू)
st.write("## 📜 Digital Bar & Beverage Menu")
menu_type = st.selectbox("Choose Category:", [
    "--- Select Category ---",
    "🍹 Denwa House Cocktails",
    "🥤 Mocktails & Coolers",
    "☕ Fresh Brew & Soft Drinks",
    "🥃 Straight Drinks (Premium Liquor & Wine)",
    "🔮 AI Custom Cocktail/Mocktail Generator"
])

recipe_title = ""
ingredients_used = ""
base_price = 0
is_corkage = False
drink_quantity = st.number_input("🔢 Enter Quantity:", min_value=1, max_value=20, value=1)

# --- ककटेल मेनु ---
if menu_type == "🍹 Denwa House Cocktails":
    cocktail = st.selectbox("Select Cocktail:", [
        "Select Drink", "Gauva Chilli Sour - INR 850", "Ginto - INR 850", "Bees Knees - INR 850",
        "Sip & Smile - INR 800", "Beet Ginger Whisper - INR 800", "Classic Mojito - INR 750",
        "Screwdriver - INR 750", "Jungle Toddy - INR 750", "Leopard Paw - INR 750",
        "Bloody Mary - INR 750", "Picante - INR 750", "Cuba Libre - INR 750",
        "Gauva Martini - INR 650", "Mahua Bloom - INR 650"
    ])
    if cocktail != "Select Drink":
        recipe_title = cocktail.split(" - ")[0]
        base_price = int(cocktail.split(" - ")[1].replace("INR ", ""))
        ingredients_used = recipe_title

# --- मकटेल मेनु ---
elif menu_type == "🥤 Mocktails & Coolers":
    mocktail = st.selectbox("Select Mocktail / Cooler:", [
        "Select Drink", "Ginger Limeade - INR 450", "Virgin Coco Colada - INR 450",
        "Melon Basil Cooler - INR 450", "Sunset Glory - INR 450", "Virgin Mary - INR 450",
        "Virgin Mojito - INR 450", "Chilli Amrud - INR 450", "Pomegranate Mint Sparkle - INR 450"
    ])
    if mocktail != "Select Drink":
        recipe_title = mocktail.split(" - ")[0]
        base_price = int(mocktail.split(" - ")[1].replace("INR ", ""))
        ingredients_used = recipe_title

# --- कफी र सफ्ट ड्रिंक्स ---
elif menu_type == "☕ Fresh Brew & Soft Drinks":
    soft = st.selectbox("Select Beverage:", [
        "Select Drink", "Fresh Brew: Cold Coffee - INR 350", "Fresh Brew: Ice Latte - INR 350",
        "Fresh Brew: Iced Coffee Lemonade - INR 350", "Fresh Brew: Affogato - INR 350",
        "Fresh Brew: Phoenix Fantasy - INR 350", "Fresh Brew: Coffee Tonic - INR 350",
        "Fresh Fruit Juice - INR 300", "Homemade Iced Tea - INR 300", "Choice of Smoothies - INR 300",
        "Himalayan Sparkling Water - INR 300", "Tonic Water / Gingerale - INR 250",
        "Flavoured Lassi - INR 250", "Fresh Lime Soda - INR 250", "Himalaya Still Mineral Water - INR 250",
        "Soft Drinks / Soda - INR 200", "Bottled Water - INR 100"
    ])
    if soft != "Select Drink":
        recipe_title = soft.split(" - ")[0]
        base_price = int(soft.split(" - ")[1].replace("INR ", ""))
        ingredients_used = recipe_title

# --- हार्ड ड्रिंक्स र वाइन मेनु ---
elif menu_type == "🥃 Straight Drinks (Premium Liquor & Wine)":
    liquor = st.selectbox("Select Premium Liquor / Wine:", [
        "Select Drink", "Jacob's Creek (Red/White Bottle) - INR 4000", "Sula (Red/White Bottle) - INR 3500",
        "Taliskar X-Yrs - INR 900", "The Glenlivet XII-Yrs - INR 900", "The Glenfedich XII-Yrs - INR 900",
        "Imported Beer (650 ML) - INR 700", "Grey Goose Vodka - INR 700", "Indri (Indian Single Malt) - INR 700",
        "Amrut Amalgum (Indian Single Malt) - INR 700", "Indian Beer (650 ML) - INR 650",
        "Chivas Regal XII-Yrs - INR 600", "JW Black Label XII-Yrs - INR 600", "Bombay Sapphire (Gin) - INR 600",
        "JW Red Label - INR 555", "Teacher's 50 - INR 555", "Ballantine - INR 555", "Absolut Vodka - INR 500",
        "Jaisalmer (Indian Craft Gin) - INR 500", "Tanqueray (London Dry Gin) - INR 500", "Jameson Irish - INR 500",
        "100-Pipers - INR 450", "Smirnoff Vodka - INR 400", "Bacardi White Rum - INR 400", "Bacardi Black Rum - INR 400",
        "Morpheus XO (Brandy) - INR 400", "Camino (Tequila) - INR 400", "Old Monk - INR 300", "Mahulo (Heritage Mahua) - INR 300",
        "🍾 [BYOB] Bring Your Own Bottle (Corkage Charge)"
    ])
    if liquor != "Select Drink":
        if "[BYOB]" in liquor:
            recipe_title = "Guest Own Bottle Service (Corkage)"
            corkage_type = st.radio("Select Bottle Type for Corkage:", ["Beer (INR 300)", "Wine (INR 1000)", "Other Liquor (INR 2000)"])
            if "Beer" in corkage_type: base_price = 300
            elif "Wine" in corkage_type: base_price = 1000
            else: base_price = 2000
            is_corkage = True
        else:
            recipe_title = liquor.split(" - ")[0]
            base_price = int(liquor.split(" - ")[1].replace("INR ", ""))
        ingredients_used = recipe_title

# --- एआई कस्टम र वन-गार्डेन जेनेरेटर ---
elif menu_type == "🔮 AI Custom Cocktail/Mocktail Generator":
    st.write("### 🍓 Denwa Garden & Forest Fresh Infusion")
    st.info("💡 Denwa Garden / Forest items available: Fresh Mahua Bloom, Wild Jamun, Bael (Stone Apple), Forest Mint, Gondhoraj Lime, Fresh Lemongrass, Holy Basil (Tulsi), Ginger & Chilli Powder for Glass Rimming.")
    custom_ingredients = st.text_input("Enter available ingredients or forest picks (e.g., Mahua, Wild Jamun, Basil, Vodka):")
    if custom_ingredients:
        recipe_title = f"Forest Infused AI Creation with {custom_ingredients}"
        ingredients_used = custom_ingredients
        base_price = 850

# ६. एआई प्रोसेसिङ फङ्सन
def get_working_model():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    if available_models: return genai.GenerativeModel(available_models[0])
    return None

model = get_working_model()

# --- बटन १: पहिले रेसिपी र बिल ड्रफ्ट हेर्ने ---
if recipe_title and selected_room != "Select Cottage / Room / Table":
    st.markdown("---")
    if st.button("🔮 Step 1: Generate Recipe & Preview Details"):
        with st.spinner("Denwa एआईले प्रिमियम रेसिपी र बिलको विवरण तयार पार्दैछ..."):
            try:
                # ट्याक्स र हिसाब स्क्रिनमा मात्र देखाउने
                subtotal_bill = base_price * drink_quantity
                gst_tax = round(subtotal_bill * 0.18, 2)
                total_payable = round(subtotal_bill + gst_tax, 2)

                # रेसिपी जेनेरेसन
                prompt = (
                    f"You are Saroj Kumal, the elite professional Mixologist at Denwa Backwater Escape Luxury Resort. "
                    f"Provide an incredibly detailed, high-end hospitality breakdown for the beverage: '{recipe_title}'. "
                    f"Incorporate elements of the luxury natural resort setting (Denwa Garden and nearby Forest areas). "
                    f"Your response must include these exact sections styled beautifully with bullet points:\n"
                    f"- 🧾 ** Drink Name & Eco-Luxury Concept**\n"
                    f"- 🍸 ** Recommended Glassware & Forest Rimming Technique**\n"
                    f"- 🍓 ** Accurate Ingredients & Measurements**\n"
                    f"- 🥄 ** Mixing Method & Wilderness Infusion Technique**\n"
                    f"- 👅 ** Taste & Aroma Profile**\n"
                    f"- ✨ ** Saroj's Signature Natural Garnishing & Serving Style**"
                )
                response = model.generate_content(prompt)
                
                # सेसन स्टेटमा डेटा सेभ गर्ने ताकि अर्को बटन थिच्दा नउडोस्
                st.session_state['recipe_output'] = response.text
                st.session_state['subtotal'] = subtotal_bill
                st.session_state['gst'] = gst_tax
                st.session_state['total'] = total_payable
                st.session_state['ingredients'] = ingredients_used
                st.session_state['item_name'] = recipe_title
                st.session_state['ready_to_order'] = True
                
            except Exception as e:
                st.error(f"Error: {e}")

# --- रेसिपी र बिलको प्रिभ्यु डिस्प्ले गर्ने ---
if 'ready_to_order' in st.session_state and st.session_state['ready_to_order']:
    st.markdown("---")
    st.write(st.session_state['recipe_output'])
    
    # बिलको प्रिभ्यु बक्स
    st.markdown("### 📊 Draft Bill Preview (18% GST)")
    st.write(f"**Location:** {selected_room} | **Item:** {st.session_state['item_name']} x {drink_quantity}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Subtotal", f"₹ {st.session_state['subtotal']:,.2f}")
    col2.metric("GST (18% Fixed)", f"₹ {st.session_state['gst']:,.2f}")
    col3.metric("Grand Total", f"₹ {st.session_state['total']:,.2f}")
    
    # ४K फोटो प्रिभ्यु
    photo_prompt = f"A high-end 4k ultra-hd professional food photography of an eco-luxury forest cocktail with {st.session_state['ingredients']}, served in an artisan rustic glass rimmed with wild spices, premium resort wooden bar counter, cinematic lighting"
    encoded_prompt = urllib.parse.quote(photo_prompt)
    image_url = f"https://image.pollinations.ai/p/{encoded_prompt}?width=1200&height=900&seed=101&model=flux"
    st.image(image_url, caption=f"Premium 4K Presentation Visual", use_container_width=True)
    
    st.markdown("---")
    st.write("### 🚨 Everything Correct? Dispatch Now:")
    
    # --- बटन २: अब मात्र एकाउन्टेन्ट र बारमा अर्डर पठाउने ---
    st.markdown('<div class="dispatch-btn">', unsafe_allow_html=True)
    if st.button("🟢 Step 2: Confirm Order & Send Bill to Accountant"):
        st.success(f"🎉 SUCCESS! Order officially sent to Accountant Computer & Bar for {selected_room}!")
        
        # 📲 ह्वाट्सएप लिंक जेनरेट
        whatsapp_message = (
                    f"🌿 *NEW CONFIRMED DENWA RESORT ORDER* 🌿\n\n"
                    f"🚪 *Room/Table:* {selected_room}\n"
                    f"🍹 *Item:* {st.session_state['item_name']}\n"
                    f"🔢 *Quantity:* {drink_quantity}\n"
                    f"💰 *Subtotal:* ₹{st.session_state['subtotal']:,.2f}\n"
                    f"✨ *GST (18%):* ₹{st.session_state['gst']:,.2f}\n"
                    f"💵 *Grand Total:* ₹{st.session_state['total']:,.2f}\n\n"
                    f"_Dispatched via Saroj's Smart AI Framework._"
                )
        encoded_message = urllib.parse.quote(whatsapp_message)
        whatsapp_link = f"https://wa.me/918305020237?text={encoded_message}"
        
        st.markdown(f'''
            <a href="{whatsapp_link}" target="_blank">
                <button style="background-color: #25D366; color: white; font-weight: bold; font-size: 16px; border-radius: 8px; width: 100%; border: none; padding: 12px; cursor: pointer;">
                    📲 Open WhatsApp Ticket to Bar (+918305020237)
                </button>
            </a>
        ''', unsafe_allow_html=True)
        
        # क्युआर कोड पेमेन्ट
        st.markdown("---")
        st.write("### 💳 Quick QR Payment")
        qr_image_url = "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=DenwaBackwaterEscape"
        st.image(qr_image_url, caption="Scan to Pay", width=200)
        
        # 🏦 एकाउन्टेन्टको लाइभ डेटा सिङ्क (एकाउन्टेन्ट स्क्रिन अलर्ट)
        st.markdown("---")
        st.write("### 🏦 Accountant Real-Time Sync Status")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        accounting_data = {
            "Timestamp": current_time,
            "Location": selected_room,
            "Beverage Name": st.session_state['item_name'],
            "Quantity": drink_quantity,
            "Subtotal (INR)": st.session_state['subtotal'],
            "GST Tax (18%)": st.session_state['gst'],
            "Grand Total (INR)": st.session_state['total'],
            "Accounting Status": "LIVE DISPATCHED TO ACCOUNTANT COMPUTER"
        }
        st.json(accounting_data)
        st.balloons()
        
        # अर्डर पठाइसकेपछि स्टेट क्लियर गर्ने ताकि दोहोर्‍याएर नजाओस्
        st.session_state['ready_to_order'] = False
    st.markdown('</div>', unsafe_allow_html=True)

elif recipe_title == "" and menu_type != "--- Select Category ---":
    st.warning("⚠️ अर्डर सुरु गर्न कृपया पहिले मेनुबाट कुनै एउटा पेय पदार्थ छान्नुहोस्।")
elif selected_room == "Select Cottage / Room / Table" and menu_type != "--- Select Category ---":
    st.error("🚨 कृपया अर्डर र रेसिपी हेर्नु अघि पाहुनाको कटेज, रुम वा टेबल नम्बर सेलेक्ट गर्नुहोस्!")

st.markdown("---")
st.caption("© 2026 Denwa Backwater Escape | Digital AI Platform v6.5 (Sequence Fixed)")
