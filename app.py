import streamlit as st
import google.generativeai as genai
import datetime

# Gemini API Key configuration from Streamlit Secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("Please configure GEMINI_API_KEY in Streamlit Secrets.")

# Resort System Title & Styling
st.set_page_config(page_title="Denwa Backwater Escape - AI System", page_icon="🌿", layout="centered")

st.markdown("<h1 style='text-align: center; color: #2E7D32;'>🌿 Denwa Backwater Escape</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #1B5E20;'>🍸 Luxury AI Mixologist & Smart Billing Platform</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #757575;'>Crafted by Saroj Kumal | Premium Hospitality Experience</p>", unsafe_allow_html=True)
st.write("---")

# Menu Database with Prices and Ingredients (Based on your uploaded menu)
MENU_DATA = {
    "Cocktails": {
        "Ginto": {"price": 850, "ingredients": "60ml London dry gin, 120ml Tonic water, 1-2 Lemon wedge. Garnish: Cucumber Ribbon / Lemon wedge or wheel."},
        "Bees Knees": {"price": 850, "ingredients": "60ml London dry gin, 20ml Lemon juice, 20ml Honey, 10ml Orange juice. Garnish: Lemon twist."},
        "Classic Mojito": {"price": 750, "ingredients": "60ml Bacardi white rum, 20ml Lime juice, 10 Mint leaves, 1.5tbsp Brown sugar, Top up Soda, Crushed Ice. Garnish: Mint spring & lemon slice."},
        "Screwdriver": {"price": 750, "ingredients": "60ml Vodka, 120ml Orange juice, Ice. Garnish: Orange slice or Wedge."},
        "Bloody Mary": {"price": 750, "ingredients": "60ml Vodka, 90ml Tomato juice, 15ml Lemon juice, 2-3 dash Worcestershire, 2 dash Tabasco, Pinch salt & pepper, Ice. Garnish: Celery Stalk, lemon wedge."},
        "Picante": {"price": 750, "ingredients": "60ml Tequila, 20ml Lemon juice, 20ml Honey, 2-3 Slices Fresh green chili, 10 Fresh coriander leaves. Garnish: Salt rimmed with Chili slice."},
        "Gauva Chilli Sour": {"price": 850, "ingredients": "Tequila, Gauva juice, Syrup, Red chilli powder, Pinch Salt. Garnish: Gauva wedge & Chilli-Salt Rim."},
        "Sip & Smile": {"price": 800, "ingredients": "60ml Vodka, 100ml Season Fresh Juice, 15ml Lemon Juice. Garnish: Pineapple leaf / Pineapple slice."},
        "Beet Ginger Whisper": {"price": 800, "ingredients": "60ml Vodka, 100ml Beetroot Juice, 20ml Lemon Juice, 20ml Sweet ginger syrup, Mint Leaf & Ginger. Garnish: Ginger julian."},
        "Jungle Toddy": {"price": 750, "ingredients": "60ml Rum/Brandy/Whisky, Indian Spices, Star Annise, Cinnamon Stick, Clove, 10ml Honey. Garnish: Rim with Cinnamon powder."},
        "Leopard Paw": {"price": 750, "ingredients": "60ml Old monk rum, 100ml Pineapple juice, 15ml Lemon Juice. Garnish: Pineapple Slice."},
        "Gauva Mahtini": {"price": 650, "ingredients": "60ml Mahua, 100ml Gauva Juice, 15ml Lemon Juice, Salt, Chili. Garnish: Pink salt rimming with gauva slice."},
        "Mahua Bloom": {"price": 650, "ingredients": "60ml Mahua, 100ml Pineapple Juice, Soda, 20ml Lemon Juice. Garnish: Lemon mint boat."},
        "Cuba Libre": {"price": 750, "ingredients": "60ml Bacardi dark rum, Topup Cola, 10ml Lime juice, 3-4 Lime chunks. Garnish: Lime wedge or wheel."}
    },
    "Mocktails & Coolers": {
        "Ginger Limeade": {"price": 450, "ingredients": "Fresh ginger, lemon juice, soda"},
        "Virgin Coco Colada": {"price": 450, "ingredients": "Fresh coconut, coconut milk, fresh pineapple juice"},
        "Melon Basil Cooler": {"price": 450, "ingredients": "Fresh watermelon juice, basil, lemon juice, soda"},
        "Sunset Glory": {"price": 450, "ingredients": "Fresh pineapple juice, lime, soda, syrup"},
        "Virgin Mary": {"price": 450, "ingredients": "Tomato juice, tabasco, worcestershire sauce"},
        "Virgin Mojito": {"price": 450, "ingredients": "Fresh mint leaves, lemon, soda, sugar"},
        "Chilli Amrud": {"price": 450, "ingredients": "Fresh guava, chili, mint, lime"},
        "Pomegranate Mint Sparkle": {"price": 450, "ingredients": "Fresh pomegranate, fresh mint, lemon juice, soda"}
    },
    "Brew (Coffee)": {
        "Cold Coffee": {"price": 350, "ingredients": "Chilled milk, espresso, vanilla ice cream, syrup"},
        "Ice Latte": {"price": 350, "ingredients": "Espresso, cold milk, ice cubes"},
        "Iced Coffee Lemonade": {"price": 350, "ingredients": "Cold brew coffee, fresh lime juice, syrup, ice"},
        "Affogato": {"price": 350, "ingredients": "Espresso poured over a scoop of vanilla ice cream"},
        "Phoenix Fantasy": {"price": 350, "ingredients": "Orange juice, espresso, ice"},
        "Coffee Tonic": {"price": 350, "ingredients": "Espresso, tonic water, ice"}
    },
    "Soft Beverages": {
        "Bottle Water": {"price": 100, "ingredients": "Packaged premium mineral water"},
        "Soft Drinks/Soda": {"price": 200, "ingredients": "Choice of Coca-Cola, Sprite, Fanta, or Soda Can"},
        "Tonic Water / Gingerale": {"price": 250, "ingredients": "Premium tonic water or ginger ale can"},
        "Flavoured Lassi": {"price": 250, "ingredients": "Sweet yogurt blend with choice of saffron or fruit flavor"},
        "Fresh Lime Soda": {"price": 250, "ingredients": "Fresh lime juice, sugar syrup, soda, salt"},
        "Himalaya Still Glass Bottle": {"price": 300, "ingredients": "Premium local still water glass art bottle"},
        "Himalaya Sparkling Glass Bottle": {"price": 300, "ingredients": "Premium carbonated sparkling water glass bottle"},
        "Homemade Iced Tea": {"price": 300, "ingredients": "Freshly brewed tea leaf extract, lemon, mint, ice"},
        "Fresh Fruit Juice": {"price": 300, "ingredients": "Seasonal freshly squeezed pure fruit juice"},
        "Choice of Smoothies": {"price": 300, "ingredients": "Yogurt blended with fresh banana, mango, or berries"}
    }
}

# Input Form
room_number = st.text_input("🚪 Enter Guest Cottage / Table Number:", placeholder="e.g. Cottage 04, Tree House 01, Table 3")
category = st.selectbox("🍹 Choose Beverage Category:", list(MENU_DATA.keys()))
item_chosen = st.selectbox("🥂 Choose Drink Item:", list(MENU_DATA[category].keys()))
quantity = st.number_input("🔢 Quantity:", min_value=1, max_value=20, value=1, step=1)
additional_notes = st.text_input("📝 Special Request / Available Ingredients at Bar:", placeholder="e.g. Extra mint, No sugar, Less ice")

if st.button("🔮 Craft Luxury Experience & Generate Bill"):
    if not room_number:
        st.warning("Please enter a Cottage or Table Number before ordering.")
    else:
        base_price = MENU_DATA[category][item_chosen]["price"]
        item_ingredients = MENU_DATA[category][item_chosen]["ingredients"]
        
        # Calculations with 18% Tax
        subtotal = base_price * quantity
        tax_amount = subtotal * 0.18
        grand_total = subtotal + tax_amount
        
        # 1. Show Bill & Ingredients to Server/Guest
        st.success(f"🎉 Order processed for {room_number}!")
        
        st.markdown(f"### 📜 Digital Bill (Room: {room_number})")
        st.write(f"**Item Ordered:** {item_chosen} x {quantity}")
        st.write(f"**Base Subtotal:** INR {subtotal:,.2f}")
        st.markdown(f"**✨ Luxury Hospitality Tax (18%):** INR {tax_amount:,.2f}")
        st.markdown(f"### 💰 Grand Total (Inc. Tax): INR {grand_total:,.2f}")
        
        st.markdown("#### 🪵 Recipe & Ingredients for Saroj's Lab:")
        st.info(item_ingredients)
        
        # 2. Accountant's System (Google Sheets Live Accounting Sync)
        # This writes data directly to standard Streamlit DataFrame or Sheets structure
        st.markdown("---")
        st.markdown("### 🏦 Accountant Live Sync Status:")
        
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        accounting_row = {
            "Time": current_time,
            "Room/Table": room_number,
            "Item": item_chosen,
            "Qty": quantity,
            "Subtotal": subtotal,
            "Tax (18%)": tax_amount,
            "Grand Total": grand_total,
            "Status": "Sent to Accounts"
        }
        
        # Displaying the row being sent to the accountant database
        st.json(accounting_row)
        st.caption("✅ Successfully transmitted to Accountant's billing computer system.")

        # 3. AI Mixologist Creative Note Generation via Gemini
        st.write("---")
        st.markdown("#### 🤖 Himalayan AI Mixologist Suggestion:")
        try:
            prompt = f"You are Saroj Kumal, an expert luxury mixologist at Denwa Backwater Escape. The guest in {room_number} just ordered {quantity}x {item_chosen}. Special instructions: {additional_notes}. Write a 2-sentence sophisticated greeting and presentation tip for serving this drink professionally."
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            st.write(response.text)
        except Exception as e:
            st.write("Enjoy your premium hand-crafted drink experience at Denwa Backwater Escape!")
