import cv2
from pyzbar.pyzbar import decode
import time
import os

# --- Main Product Database for "FreshMart" ---
def get_product_details(barcode_data):
    """
    This function contains the product database for our store, FreshMart.
    """
    # NOTE: Prices are in INR (₹)
    mock_products = {
        # === Food & Grocery Items ===
        "8903363011411": {
            "name": "FreshMart Premia Trail Mix",
            "price": 150.00,
            "discount_percent": 10,
            "details": {"Net Quantity": "100 g"},
            "ingredients": ["Cranberry", "Black Raisins", "Pumpkin Seeds", "Almonds", "Cashew Nuts"],
            "nutrition": {"calories": 450, "protein_g": 15},
            "allergens": ["Tree Nuts"]
        },
        "8906008815191": {
            "name": "Fortune Sushan Kala Chana",
            "price": 85.00,
            "discount_percent": 0,
            "details": {"Net Weight": "500 g"},
            "ingredients": ["Kala Chana"],
            "nutrition": {"calories": 364, "protein_g": 20},
            "allergens": []
        },
        "8904335600312": {
            "name": "Yoga Bar Crunchy Muesli",
            "price": 40.00,
            "discount_percent": 0,
            "details": {"Net Weight": "40 g"},
            "ingredients": ["Rolled Oats", "Ragi Flakes", "Almonds", "Flax Seeds", "Chia Seeds"],
            "nutrition": {"calories": 156, "protein_g": 4.6},
            "allergens": ["Oats", "Nuts", "Soy"]
        },
        "8901207048760": {
            "name": "Dabur Hajmola Imli",
            "price": 30.00,
            "discount_percent": 5,
            "details": {"Type": "Tasty Digestive Tablets"},
            "ingredients": ["Pippali", "Sunthi", "Nimbu Saar", "Imli Saar", "Samudra Lavana"],
            "nutrition": {"calories": 10, "protein_g": 0.1},
            "allergens": []
        },
        "8906021924436": {
            "name": "Royal Zahidi Dates",
            "price": 250.00,
            "discount_percent": 0,
            "details": {"Net Weight": "500 g", "Country of Origin": "Iraq"},
            "ingredients": ["Zahidi Dates"],
            "nutrition": {"calories": 282, "protein_g": 2.5},
            "allergens": ["May contain traces of nuts and seeds"]
        },
        "8902346012360": {
            "name": "Electral (ORS)",
            "price": 21.50,
            "discount_percent": 0,
            "details": {"Contents": "4.40 g", "Formula": "W.H.O."},
            "ingredients": ["Sodium Chloride", "Potassium Chloride", "Sodium Citrate", "Dextrose Anhydrous"],
            "allergens": []
        },
        
        # === General & Stationery Items ===
        "9780190135096": {"name": "Oxford Mini Dictionary", "price": 275.00, "discount_percent": 15, "details": {"Publisher": "Oxford University Press"}},
        "8906073789327": {"name": "DOMS A5 Poly Notebook", "price": 80.00, "discount_percent": 0, "details": {"Ruling": "Single Line", "Pages": "160"}},
        "8906128100320": {"name": "Minimalist Face Cleanser", "price": 299.00, "discount_percent": 0, "details": {"Net Content": "100 ml"}, "ingredients": ["Aqua", "Glycerin", "Cocamidopropyl Betaine"], "allergens": []},
        "1001972587": {"name": "TRU NOTE A4 College Book", "price": 55.00, "discount_percent": 0, "details": {"Ruling": "Unruled", "Pages": "140"}},
    }
    return mock_products.get(barcode_data, None)

def check_allergies_and_requirements(product_details, user_allergies):
    if not product_details or not user_allergies: return "Not applicable or no allergies entered."
    feedback = []
    product_allergens = [a.lower() for a in product_details.get("allergens", [])]
    product_ingredients = [i.lower() for i in product_details.get("ingredients", [])]
    for allergy in user_allergies:
        if allergy in product_allergens: feedback.append(f"WARNING: Contains allergen '{allergy}'.")
        elif product_ingredients and any(allergy in ingredient for ingredient in product_ingredients): feedback.append(f"WARNING: Ingredient list contains '{allergy}'.")
    return " ".join(feedback) if feedback else "Safe for you."

def display_summary(cart, total, item_limit):
    """Clears the console and displays a summary of the shopping cart."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*55)
    print("🛒  WELCOME TO FRESHMART - YOUR SMART SHOPPING ASSISTANT 🛒")
    print("="*55)
    if not cart:
        print("\nYour cart is empty. Start scanning to add items!")
    else:
        print("\n--- Your Cart ---")
        for i, item in enumerate(cart, 1):
            final_price = item['price'] * (1 - item['discount_percent'] / 100)
            discount_info = f"({item['discount_percent']}% off!)" if item['discount_percent'] > 0 else ""
            print(f"{i}. {item['name']:<30} ₹{final_price:<7.2f} {discount_info}")
        print("-"*55)
        print(f"{'TOTAL ITEMS:':<30} {len(cart)} / {item_limit}")
        print(f"{'TOTAL CART VALUE:':<30} ₹{total:.2f}")
    print("\nPoint camera at a new barcode...")

# --- Main Barcode Scanner Logic ---
def run_barcode_scanner():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Welcome to FreshMart! Let's get your preferences first.")
    user_allergies = [req.strip().lower() for req in input("Enter your allergies, separated by commas: ").split(',') if req.strip()]
    
    # --- NEW: Set Item Limit ---
    while True:
        try:
            item_limit_str = input("Set a maximum number of items for your cart (e.g., 5): ")
            item_limit = int(item_limit_str)
            if item_limit > 0: break
            else: print("Please enter a number greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    shopping_cart, cart_total = [], 0.0
    scanned_barcode_str, last_scanned_time = None, 0
    scan_cooldown = 4

    while len(shopping_cart) < item_limit:
        display_summary(shopping_cart, cart_total, item_limit)
        ret, frame = cap.read()
        if not ret: break
        cv2.imshow("FreshMart Scanner (Press 'q' to quit)", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

        barcodes = decode(frame)
        if not barcodes: continue

        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')
            if barcode_data != scanned_barcode_str or (time.time() - last_scanned_time > scan_cooldown):
                scanned_barcode_str, last_scanned_time = barcode_data, time.time()
                product_details = get_product_details(barcode_data)

                if product_details:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("\n--- ✅ Product Scanned! ---")
                    print(f"Name:       {product_details.get('name', 'N/A')}")
                    price, discount = product_details.get('price', 0.0), product_details.get('discount_percent', 0)
                    final_price = price * (1 - discount / 100)
                    print(f"Price:      ₹{price:.2f}")
                    if discount > 0: print(f"Discount:   {discount}% OFF! (Final Price: ₹{final_price:.2f})")
                    if 'nutrition' in product_details:
                        print("\n--- Nutrition Info ---")
                        print(f"Calories:   {product_details['nutrition'].get('calories', 'N/A')} kcal")
                        print(f"Protein:    {product_details['nutrition'].get('protein_g', 'N/A')} g")
                    print("\n--- Allergy Check ---")
                    print(f"Status:     {check_allergies_and_requirements(product_details, user_allergies)}")
                    print("-"*26)
                    
                    if input("Add this item to your cart? (y/n): ").lower() == 'y':
                        shopping_cart.append(product_details)
                        cart_total += final_price
                        print(f"'{product_details['name']}' added to cart!")
                        time.sleep(1)
                else:
                    print(f"\nProduct not found for barcode: {barcode_data}")
                    time.sleep(2)
                scanned_barcode_str = None
                # Break inner loop to re-display cart after a scan
                break 

    # --- Final Checkout and Bill ---
    cap.release()
    cv2.destroyAllWindows()
    print("\nThank you for shopping at FreshMart!")
    print("="*55)
    print("Final Bill".center(55))
    print("="*55)
    display_summary(shopping_cart, cart_total, item_limit)
    print("="*55)
    print("Your shopping session has ended.")

if __name__ == "__main__":
    run_barcode_scanner()