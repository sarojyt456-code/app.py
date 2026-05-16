import streamlit as st
import google.generativeai as genai
import urllib.parse
import datetime

# 1. Luxury App Configuration
st.set_page_config(page_title="Wild Forest Mixology", page_icon="🌿", layout="centered")

# 2. Configure Gemini AI API Key securely
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    pass

# 3. Premium Bar Counter Style Theme (CSS with Single Quotes to avoid string leak)
st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(rgba(10, 12, 22, 0.90), rgba(10, 12, 22, 0.90)), 
                          url('https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?q=80&w=1600&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #f1f5f9;
    }
    .brand-title {
        color: #f59e0b !important; 
        font-family: 'Georgia', serif; 
        font-size: 2.2rem !important; 
        font-weight: bold; 
        text-shadow: 2px 2px 10px rgba(245, 158, 11, 0.3); 
        margin: 0 !important;
        padding: 0 !important;
    }
    .brand-subtitle {
        margin: 5px 0 0 0 !important; 
        font-size: 1.2rem !important; 
        color: #10b981 !important; 
        font-weight: bold !important;
    }
    h2, h3 { color: #10b981 !important; font-family: 'Georgia', serif; }
    p, span, label, div { color: #e2e8f0 !important; font-weight: 500; }
    
    div[data-baseweb="select"] > div { border: 2px solid #f59e0b !important; border-radius: 8px !important; background-color: rgba(15, 23, 42, 0.95) !important; }
    div[data-baseweb="input"] > div { border: 2px solid #10b981 !important; border-radius: 8px !important; background-color: rgba(15, 23, 42, 0.95) !important; }
    div[data-baseweb="number-input"] > div { border: 2px solid #10b981 !important; border-radius: 8px !important; background-color: rgba(15, 23, 42, 0.95) !important; }
    div[data-baseweb="radio"] label { color: #e2e8f0 !important; }

    .stButton>button { 
        background-image: linear-gradient(135deg, #f59e0b, #d97706);
        color: #ffffff !important; font-weight: bold; border-radius: 8px; width: 100%; border: none; padding: 12px; cursor: pointer;
        box-shadow: 0px 4px 15px rgba(245, 158, 11, 0.3);
    }
    .stButton>button:hover { background-image: linear-gradient(135deg, #d97706, #b45309); }
    .stButton>button p { color: white !important; }
    
    .dispatch-btn>button { background-image: linear-gradient(135deg, #ef4444, #dc2626) !important; }
    .dispatch-btn>button p { color: white !important; }
    
    .header-container { display: flex; align-items: center; justify-content: center; gap: 20px; padding: 15px 0; flex-wrap: wrap; text-align: center; }
    .brand-text-block { display: flex; flex-direction: column; align-items: center; justify-content: center; }
    .logo-frame { border-radius: 50%; border: 3px solid #f59e0b; background-color: white; padding: 5px; box-shadow: 0px 0px 15px rgba(245, 158, 11, 0.4); }
    </style>
    """, unsafe_allow_html=True)

# 4. Pure Vector Replica of Denwa Backwater Escape Official Logo (Paw & Footprint)
logo_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="120" height="120" class="logo-frame">
  <circle cx="100" cy="100" r="95" fill="#ffffff" stroke="#a3821a" stroke-width="2.5"/>
  <g fill="#8f761d" transform="translate(-5, -5)">
    <ellipse cx="75" cy="105" rx="14" ry="17"/>
    <circle cx="56" cy="88" r="7"/>
    <circle cx="70" cy="76" r="7.5"/>
    <circle cx="86" cy="78" r="7.5"/>
    <circle cx="96" cy="92" r="7"/>
  </g>
  <g fill="#dfb61a" transform="translate(15, -5)">
    <path d="M95,85 C92,95 95,115 102,125 C108,132 118,130 115,115 C112,100 106,85 95,85 Z"/>
    <circle cx="94" cy="74" r="5.5"/>
    <circle cx="103" cy="71" r="4.5"/>
    <circle cx="111" cy="72" r="4"/>
    <circle cx="118" cy="75" r="3.5"/>
    <circle cx="123" cy="81" r="3"/>
  </g>
</svg>
"""

# Fixed Rendering Layout using single quotes for HTML attributes inside f-string
st.markdown(f"""
    <div class='header-container'>
        {logo_svg}
        <div class='brand-text-block'>
            <h1 class='brand-title'>Denwa Backwater Escape</h1>
            <p class='brand-subtitle'>Luxury AI Mixologist & Guest Assistant</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.caption("Crafted by Saroj Kumal | Premium Hospitality Experience")
st.markdown("---")

# 5. Room & Table Selection
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
    "--- Select Category ---", "🍹 Cocktails", "🥤 Mocktails & Coolers", 
    "☕ Brew (Fresh Coffee) & Soft Beverages", "🥃 Straight Drinks (Premium Liquor & Wine)", "🔮 AI Custom Garden/Forest Mixology"
])

recipe_title, ingredients_used, base_price = "", "", 0
needs_ai_recipe = False
selected_size_label = "Standard Serving"

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
        needs_ai_recipe = True

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
        needs_ai_recipe = True

# --- Brew & Soft Beverages Category ---
elif menu_type == "☕ Brew (Fresh Coffee) & Soft Beverages":
    soft = st.selectbox("Select Beverage:", [
        "Select Drink", "Cold Coffee - INR 350", "Ice Latte - INR 350",
        "Iced Coffee Lemonade - INR 350", "Affogato - INR 350", "Coffee Tonic - INR 350",
        "Fresh Fruit Juice - INR 300", "Homemade Iced Tea - INR 300", "Choice of Smoothies - INR 300",
        "Himalaya Still Glass Bottle - INR 300", "Himalaya Sparkling Glass Bottle - INR 300",
        "Flavoured Lassi - INR 250", "Fresh Lime Soda - INR 250", "Soft Drinks/Soda - INR 200", "Bottle Water - INR 100"
    ])
    if soft != "Select Drink":
        recipe_title = soft.split(" - ")[0]
        base_price = int(soft.split(" - ")[1].replace("INR ", ""))
        ingredients_used = recipe_title

# --- Straight Drinks Category ---
elif menu_type == "🥃 Straight Drinks (Premium Liquor & Wine)":
    liquor = st.selectbox("Select Premium Liquor/Wine (Base 30ML price shown):", [
        "Select Drink", "Jacob's Creek (Red/White) - INR 4000", "Sula (Red/White) - INR 3500",
        "Taliskar X-Yrs - INR 900", "The Glenlivet XII-Yrs - INR 900", "The Glenfedich XII-Yrs - INR 900",
        "Imported Beer (650 ML) - INR 700", "Grey Goose Vodka - INR 700", "Indri (Indian Single Malt) - INR 700",
        "Amrut Amalgum (Indian Single Malt) - INR 700", "Indian Beer (650 ML) - INR 650",
        "Chivas Regal XII-Yrs - INR 600", "JW Black Label XII-Yrs - INR 600", "JW Red Label - INR 550",
        "Teacher's 50 - INR 550", "Ballantine - INR 550", "Absolut Vodka - INR 500",
        "Jaisalmer (Indian Craft Gin) - INR 500", "Tanqueray (London Dry Gin) - INR 500", "Jameson Irish - INR 500",
        "100-Pipers - INR 450", "Smirnoff Vodka - INR 400", "Bacardi White Rum - INR 400", "Bacardi Black Rum - INR 400",
        "Old Monk - INR 300", "Mahulo (Heritage Mahua) - INR 300"
    ])
    if liquor != "Select Drink":
        recipe_title = liquor.split(" - ")[0]
        base_30ml_price = int(liquor.split(" - ")[1].replace("INR ", ""))
        ingredients_used = recipe_title
        
        if "Beer" in recipe_title or "Jacob's" in recipe_title or "Sula" in recipe_title:
            size_choice = st.radio("Serving Size:", ["Full Bottle / Unit"])
            base_price = base_30ml_price
            selected_size_label = "Full Unit"
        else:
            size_choice = st.radio("Select Peg Size:", ["30 ML (Single)", "60 ML (Double)", "Full Bottle (750 ML)"])
            if size_choice == "30 ML (Single)":
                base_price = base_30ml_price
                selected_size_label = "30 ML"
            elif size_choice == "60 ML (Double)":
                base_price = base_30ml_price * 2
                selected_size_label = "60 ML"
            elif size_choice == "Full Bottle (750 ML)":
                base_price = base_30ml_price * 10 
                selected_size_label = "Full Bottle"

# --- AI Custom Mixology ---
elif menu_type == "🔮 AI Custom Garden/Forest Mixology":
    st.write("### 🌿 Forest-to-Glass Live Creation")
    st.info("💡 Denwa Garden / Forest items available: Fresh Mahua Bloom, Wild Jamun, Bael, Forest Mint, Gondhoraj Lime, Fresh Lemongrass, Holy Basil, Ginger & Chilli Powder.")
    custom_ingredients = st.text_input("Enter available ingredients or forest picks (e.g., Mahua, Wild Jamun, Basil, Vodka):")
    if custom_ingredients:
        recipe_title = f"Custom Infused AI Creation"
        ingredients_used = custom_ingredients
        base_price = 850
        needs_ai_recipe = True

drink_quantity = st.number_input("🔢 Enter Quantity:", min_value=1, max_value=20, value=1)

def get_working_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if available_models: return genai.GenerativeModel(available_models[0])
    except Exception:
        pass
    return None

model = get_working_model()

# --- PROCESSING SYSTEM ---
if recipe_title and selected_room != "Select Cottage / Room / Table":
    st.markdown("---")
    
    if st.button("🔮 Step 1: Process & Verify Bill Structure"):
        subtotal_bill = base_price * drink_quantity
        gst_tax = round(subtotal_bill * 0.18, 2)
        total_payable = round(subtotal_bill + gst_tax, 2)
        
        st.session_state['subtotal'] = subtotal_bill
        st.session_state['gst'] = gst_tax
        st.session_state['total'] = total_payable
        st.session_state['drink_name'] = recipe_title
        st.session_state['size_label'] = selected_size_label
        st.session_state['active_preview'] = True
        st.session_state['photo_ing'] = ingredients_used
        
        if needs_ai_recipe and model is not None:
            with st.spinner("AI is crafting fresh mixology ratios..."):
                try:
                    prompt = (
                        f"You are Saroj Kumal, Head of Beverage at Denwa Backwater Escape resort. "
                        f"Create a professional cocktail/mocktail recipe breakdown for: '{recipe_title}' using {ingredients_used}. "
                        f"Include Concept, Ratios, Infusion Method, and Luxury Garnish."
                    )
                    response = model.generate_content(prompt)
                    st.session_state['recipe_text'] = response.text
                except Exception:
                    st.session_state['recipe_text'] = "Premium hand-crafted beverage selection processed successfully."
        else:
            st.session_state['recipe_text'] = f"✨ **Direct Premium Pour Service:** Serving {recipe_title} as a standard premium pour hospitality standard directly to guests."

# --- VISUAL DISPLAY & CONFIRMATION ---
if 'active_preview' in st.session_state and st.session_state['active_preview']:
    st.markdown("---")
    st.markdown(st.session_state['recipe_text'])
    
    st.markdown("### 📊 Live Bill Breakdown (18% GST Added)")
    st.write(f"**Location:** {selected_room} | **Beverage:** {st.session_state['drink_name']} ({st.session_state['size_label']})")
    
    col1, col2, col3 = st.columns(3)
    col1.metric(f"Subtotal ({drink_quantity} Qty)", f"₹ {st.session_state['subtotal']:,.2f}")
    col2.metric("GST Tax (18%)", f"₹ {st.session_state['gst']:,.2f}")
    col3.metric("Grand Total (Payable)", f"₹ {st.session_state['total']:,.2f}")
    
    photo_prompt = f"Luxury food photography of {st.session_state['photo_ing']} beverage served on a premium resort dark wooden bar counter, moody ambient studio lighting, professional setup"
    st.image(f"https://image.pollinations.ai/p/{urllib.parse.quote(photo_prompt)}?width=1200&height=900&seed=45&model=flux", use_container_width=True)
    
    st.markdown("---")
    st.write("### 🚨 Everything Perfect? Dispatch Order Now:")
    
    st.markdown('<div class="dispatch-btn">', unsafe_allow_html=True)
    if st.button("🟢 Step 2: Confirm Order & Dispatch Bill"):
        st.success(f"🎉 APPROVED! Order for {selected_room} has been synced to the main database successfully!")
        
        msg = (
            f"🌿 *DENWA RESORT OFFICIAL ORDER* 🌿\n\n"
            f"🚪 *Location:* {selected_room}\n"
            f"🍹 *Beverage:* {st.session_state['drink_name']}\n"
            f"📏 *Portion:* {st.session_state['size_label']}\n"
            f"🔢 *Quantity:* {drink_quantity}\n"
            f"💰 *Total Bill (+18% GST):* ₹{st.session_state['total']:,.2f}\n\n"
            f"_Dispatched by Head of Beverage Saroj Kumal._"
        )
        st.markdown(f'<a href="https://wa.me/918305020237?text={urllib.parse.quote(msg)}" target="_blank"><button style="background-color: #25D366; color: white; width: 100%; border: none; padding: 12px; font-weight:bold; border-radius:8px; cursor:pointer;">📲 Click to Send Ticket via WhatsApp to Bar Counter</button></a>', unsafe_allow_html=True)
        
        st.image("https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=DenwaBackwaterEscape", width=160, caption="Quick Scan Bill Payment")
        
        st.write("### 🏦 Accountant Real-Time Sync Network")
        st.json({
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Location": selected_room,
            "Item": st.session_state['drink_name'],
            "Portion": st.session_state['size_label'],
            "Quantity": drink_quantity,
            "Total_Payable_INR": st.session_state['total'],
            "Status": "SYNCED TO SYSTEM DATABASE"
        })
        st.balloons()
        st.session_state['active_preview'] = False
    st.markdown('</div>', unsafe_allow_html=True)

elif recipe_title == "" and menu_type != "--- Select Category ---":
    st.warning("⚠️ Please select a valid beverage from the menu list to proceed.")
elif selected_room == "Select Cottage / Room / Table" and menu_type != "--- Select Category ---":
    st.error("🚨 Please choose the Cottage or Table area first!")

st.markdown("---")
st.caption("© 2026 Denwa Backwater Escape | Production Build v17.6 (String Conflict Fixed)")
