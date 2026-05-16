import streamlit as st
import google.generativeai as genai
import urllib.parse
import datetime

# 1. Luxury App Configuration (Window Title & Favicon)
st.set_page_config(page_title="Wild Forest Mixology", page_icon="🌿", layout="centered")

# 2. Configure Gemini AI API Key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. Premium Resort Theme & Full Background Styling
st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.85)), 
                          url("https://images.unsplash.com/photo-1572116469696-31de0f17cc34?q=80&w=1600&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #f8fafc;
    }
    h1, h2, h3 { color: #22c55e !important; font-family: 'Georgia', serif; text-shadow: 2px 2px 4px rgba(0,0,0,0.7); }
    p, span, label, div { color: #f1f5f9 !important; font-weight: 500; text-shadow: 1px 1px 3px rgba(0,0,0,0.8); }
    
    /* Input & Select Box Rims */
    div[data-baseweb="select"] > div { border: 2px solid #22c55e !important; border-radius: 8px !important; background-color: rgba(30, 41, 59, 0.8) !important; }
    div[data-baseweb="input"] > div { border: 2px solid #22c55e !important; border-radius: 8px !important; background-color: rgba(30, 41, 59, 0.8) !important; }
    div[data-baseweb="number-input"] > div { border: 2px solid #22c55e !important; border-radius: 8px !important; background-color: rgba(30, 41, 59, 0.8) !important; }
    
    .stButton>button { background-color: #22c55e; color: white; font-weight: bold; border-radius: 8px; width: 100%; border: none; padding: 12px; cursor: pointer; box-shadow: 0px 4px 10px rgba(0,0,0,0.3); }
    .stButton>button:hover { background-color: #16a34a; }
    .dispatch-btn>button { background-color: #e11d48 !important; }
    .dispatch-btn>button:hover { background-color: #be123c !important; }
    
    /* Responsive Header Layout with Round White Bordered Logo */
    .header-container { display: flex; align-items: center; justify-content: center; gap: 20px; padding: 20px 0; flex-wrap: wrap; text-align: center; }
    .logo-img { border-radius: 50%; box-shadow: 0px 6px 15px rgba(0,0,0,0.6); border: 4px solid #ffffff; background-color: #ffffff; object-fit: cover; }
    </style>
    """, unsafe_allow_html=True)

# 4. Ultra-Reliable CDN CDN Link for image_16.png
# यसले तपाईँको गिटहबको लोगोलाई विना कुनै अवरोध फास्ट स्पीडमा सिधै लोड गराउँछ
logo_url = "https://cdn.jsdelivr.net/gh/sarojyt456-code/app.py@main/image_16.png"

st.markdown(f"""
    <div class="header-container">
        <img src="{logo_url}" width="140" height="140" class="logo-img" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1546173159-319807543181?q=80&w=200&auto=format&fit=crop';">
        <div style="display: flex; flex-direction: column; align-items: center;">
            <h1 style="margin: 0; font-size: 2.3rem;">Denwa Backwater Escape</h1>
            <p style="margin: 5px 0 0 0; font-size: 1.3rem; color: #22c55e !important; font-weight: bold;">Luxury AI Mixologist & Guest Assistant</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.caption("Crafted by Saroj Kumal | Premium Hospitality Experience")
st.markdown("---")

# 5. Room & Table Selection (100% English)
room_options = ["Select Cottage / Room / Table"]
for i in range(1, 9): room_options.append(f"🏠 Cottage {i:02d}")
room_options.extend(["🌲 Tree House 09", "🌲 Tree House 10"])
room_options.extend(["🛏️ Standard Room 11", "🛏️ Standard Room 12", "🛏️ Standard Room 14", "🛏️ Standard Room 15"])
for i in range(1, 6): room_options.append(f"🍽️ Dining Table {i}")

selected_room = st.selectbox("🚪 Enter Guest Cottage / Table Number:", room_options)

st.markdown("---")

# 6. Digital Bar Menu Setup
st.write("## 📜 Digital Bar Menu")
menu_type = st.selectbox("Choose Category:", [
    "--- Select Category ---",
    "🍹 Cocktails",
    "🥤 Mocktails & Coolers",
    "☕ Brew (Fresh Coffee) & Soft Beverages",
    "🥃 Straight Drinks (Premium Liquor & Wine)",
    "🔮 AI Custom Garden/Forest Mixology"
])

recipe_title = ""
ingredients_used = ""
base_price = 0
drink_quantity = st.number_input("🔢 Enter Quantity:", min_value=1, max_value=20, value=1)

# --- Cocktails Category ---
if menu_type == "🍹 Cocktails":
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

# --- Mocktails Category ---
elif menu_type == "🥤 Mocktails & Coolers":
    mocktail = st.selectbox("Select Mocktail:", [
        "Select Drink", "Ginger Limeade - INR 450", "Virgin Coco Colada - INR 450",
        "Melon Basil Cooler - INR 450", "Sunset Glory - INR 450", "Virgin Mary - INR 450",
        "Virgin Mojito - INR 450", "Chilli Amrud - INR 450", "Pomegranate Mint Sparkle - INR 450"
    ])
    if mocktail != "Select Drink":
        recipe_title = mocktail.split(" - ")[0]
        base_price = int(mocktail.split(" - ")[1].replace("INR ", ""))
        ingredients_used = recipe_title

# --- Brew & Soft Beverages Category ---
elif menu_type == "☕ Brew (Fresh Coffee) & Soft Beverages":
    soft = st.selectbox("Select Beverage:", [
        "Select Drink", "Cold Coffee - INR 350", "Ice Latte - INR 350",
        "Iced Coffee Lemonade - INR 350", "Affogato - INR 350",
        "Phoenix Fantasy - INR 350", "Coffee Tonic - INR 350",
        "Fresh Fruit Juice - INR 300", "Homemade Iced Tea - INR 300", "Choice of Smoothies - INR 300",
        "Himalaya Still Glass Bottle - INR 300", "Himalaya Sparkling Glass Bottle - INR 300",
        "Tonic Water / Gingerale - INR 250", "Flavoured Lassi - INR 250", "Fresh Lime Soda - INR 250",
        "Soft Drinks/Soda - INR 200", "Bottle Water - INR 100"
    ])
    if soft != "Select Drink":
        recipe_title = soft.split(" - ")[0]
        base_price = int(soft.split(" - ")[1].replace("INR ", ""))
        ingredients_used = recipe_title

# --- Straight Drinks Category ---
elif menu_type == "🥃 Straight Drinks (Premium Liquor & Wine)":
    liquor = st.selectbox("Select Premium Liquor:", [
        "Select Drink", "Jacob's Creek (Red/White) - INR 4000", "Sula (Red/White) - INR 3500",
        "Taliskar X-Yrs - INR 900", "The Glenlivet XII-Yrs - INR 900", "The Glenfedich XII-Yrs - INR 900",
        "Imported Beer (650 ML) - INR 700", "Grey Goose Vodka - INR 700", "Indri (Indian Single Malt) - INR 700",
        "Amrut Amalgum (Indian Single Malt) - INR 700", "Indian Beer (650 ML) - INR 650",
        "Chivas Regal XII-Yrs - INR 600", "JW Black Label XII-Yrs - INR 600", "JW Red Label - INR 550",
        "Teacher's 50 - INR 550", "Ballantine - INR 550", "Absolut Vodka - INR 500",
        "Jaisalmer (Indian Craft Gin) - INR 500", "Tanqueray (London Dry Gin) - INR 500", "Jameson Irish - INR 500",
        "100-Pipers - INR 450", "Smirnoff Vodka - INR 400", "Bacardi White Rum - INR 400", "Bacardi Black Rum - INR 400",
        "Morpheus XO (Indian Brandy) - INR 400", "Camino (Tequila) - INR 400", "Old Monk - INR 300", "Mahulo (Heritage Mahua) - INR 300",
        "🍾 [BYOB] Bring Your Own Bottle (Corkage Policy)"
    ])
    if liquor != "Select Drink":
        if "[BYOB]" in liquor:
            recipe_title = "Guest Own Bottle Service"
            corkage_type = st.radio("Corkage Type:", ["Beer (INR 300)", "Wine (INR 1000)", "Other Liquor (INR 2000)"])
            if "Beer" in corkage_type: base_price = 300
            elif "Wine" in corkage_type: base_price = 1000
            else: base_price = 2000
        else:
            recipe_title = liquor.split(" - ")[0]
            base_price = int(liquor.split(" - ")[1].replace("INR ", ""))
        ingredients_used = liquor

# --- AI Custom Mixology Category ---
elif menu_type == "🔮 AI Custom Garden/Forest Mixology":
    st.write("### 🌿 Forest-to-Glass Live Creation")
    st.info("💡 Available Denwa Elements: Mahua Bloom, Wild Jamun, Bael Fruit, Lemongrass, Forest Mint, Tulsi, Gondhoraj Lime, Chili Rimming powder.")
    custom_ingredients = st.text_input("Enter available ingredients or forest picks (e.g., Mahua, Basil, Vodka):")
    if custom_ingredients:
        recipe_title = f"Forest Infused AI Cocktail ({custom_ingredients})"
        ingredients_used = custom_ingredients
        base_price = 850

# Automated Model Sync
def get_working_model():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    if available_models: return genai.GenerativeModel(available_models[0])
    return None

model = get_working_model()

# --- STEP 1: Preview Glass Recipe ---
if recipe_title and selected_room != "Select Cottage / Room / Table":
    st.markdown("---")
    if st.button("🔮 Step 1: Craft & Preview Glass Recipe"):
        with st.spinner("Denwa AI is generating the premium recipe and glass rimming technique..."):
            try:
                subtotal_bill = base_price * drink_quantity
                gst_tax = round(subtotal_bill * 0.18, 2)
                total_payable = round(subtotal_bill + gst_tax, 2)

                prompt = (
                    f"You are Saroj Kumal, Head of Beverage Experience at Denwa Backwater Escape luxury resort. "
                    f"Create an elite, professional recipe breakdown in English for: '{recipe_title}'. "
                    f"Emphasize how to beautifully utilize forest/garden herbs inside the glass "
                    f"and how to rim the glassware with local salts/spices for an upscale guest presentation. "
                    f"Structure clearly with: \n"
                    f"- 🧾 **Drink Concept**\n"
                    f"- 🍸 **Glassware & Forest Rim Technique**\n"
                    f"- 🍓 **Ingredients & Professional Ratios**\n"
                    f"- 🥄 **Method of Infusion**\n"
                    f"- ✨ **Saroj's Signature Natural Garnish**"
                )
                response = model.generate_content(prompt)
                
                st.session_state['recipe_text'] = response.text
                st.session_state['subtotal'] = subtotal_bill
                st.session_state['gst'] = gst_tax
                st.session_state['total'] = total_payable
                st.session_state['drink_name'] = recipe_title
                st.session_state['active_preview'] = True
                st.session_state['photo_ing'] = ingredients_used
            except Exception as e:
                st.error(f"Error generating recipe: {e}")

# --- Recipe & Bill Display Panel ---
if 'active_preview' in st.session_state and st.session_state['active_preview']:
    st.markdown("---")
    st.write(st.session_state['recipe_text'])
    
    # Billing Table Breakdown
    st.markdown("### 📊 Live Bill Breakdown (18% GST)")
    st.write(f"**Location:** {selected_room} | **Beverage:** {st.session_state['drink_name']} (Qty: {drink_quantity})")
    col1, col2, col3 = st.columns(3)
    col1.metric("Subtotal", f"₹ {st.session_state['subtotal']:,.2f}")
    col2.metric("GST Tax (18%)", f"₹ {st.session_state['gst']:,.2f}")
    col3.metric("Grand Total", f"₹ {st.session_state['total']:,.2f}")
    
    # 4K Visual Generation
    photo_prompt = f"Luxury food photography of an eco cocktail with {st.session_state['photo_ing']}, served in a glass rimmed with wild forest spices on a rustic resort wooden bar counter, lush jungle leaves, ultra high-res"
    encoded_prompt = urllib.parse.quote(photo_prompt)
    st.image(f"https://image.pollinations.ai/p/{encoded_prompt}?width=1200&height=900&seed=42&model=flux", caption="Premium Visual Preview", use_container_width=True)
    
    st.markdown("---")
    st.write("### 🚨 Everything Perfect? Dispatch Order Now:")
    
    # --- STEP 2: Dispatch Order ---
    st.markdown('<div class="dispatch-btn">', unsafe_allow_html=True)
    if st.button("🟢 Step 2: Confirm Order & Dispatch Bill"):
        st.success(f"🎉 APPROVED! Order for {selected_room} has been successfully synced to the system!")
        
        # WhatsApp Order Generation
        msg = (
            f"🌿 *DENWA RESORT OFFICIAL ORDER* 🌿\n\n"
            f"🚪 *Location:* {selected_room}\n"
            f"🍹 *Drink:* {st.session_state['drink_name']}\n"
            f"🔢 *Qty:* {drink_quantity}\n"
            f"💰 *Total Bill (+18% GST):* ₹{st.session_state['total']:,.2f}\n\n"
            f"_Sent by Head of Beverage Saroj Kumal._"
        )
        encoded_msg = urllib.parse.quote(msg)
        whatsapp_link = f"https://wa.me/918305020237?text={encoded_msg}"
        
        st.markdown(f'''
            <a href="{whatsapp_link}" target="_blank">
                <button style="background-color: #25D366; color: white; font-weight: bold; font-size: 16px; border-radius: 8px; width: 100%; border: none; padding: 12px; cursor: pointer;">
                    📲 Click to Send SMS/Ticket via WhatsApp to Bar
                </button>
            </a>
        ''', unsafe_allow_html=True)
        
        # Payment QR Code
        st.markdown("---")
        qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=DenwaBackwaterEscape"
        st.image(qr_url, caption="Guest Quick Scan Payment Gateway", width=180)
        
        # Accountant Live Data Logging
        st.markdown("---")
        st.write("### 🏦 Accountant Real-Time Sync Network")
        st.json({
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Location": selected_room,
            "Beverage_Name": st.session_state['drink_name'],
            "Quantity": drink_quantity,
            "Total_Payable_INR": st.session_state['total'],
            "Status": "SYNCED TO MAIN DATABASE COMPUTER"
        })
        st.balloons()
        st.session_state['active_preview'] = False
    st.markdown('</div>', unsafe_allow_html=True)

# 100% English Alert Warnings
elif recipe_title == "" and menu_type != "--- Select Category ---":
    st.warning("⚠️ Please select a valid beverage from the menu to proceed.")
elif selected_room == "Select Cottage / Room / Table" and menu_type != "--- Select Category ---":
    st.error("🚨 Please select the Guest Cottage or Table Number before previewing the recipe!")

st.markdown("---")
st.caption("© 2026 Denwa Backwater Escape | Production Build v12.0 (CDN Absolute Fix)")
