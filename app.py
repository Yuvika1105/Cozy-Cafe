# app.py
from flask import Flask, render_template, request, jsonify
import os

# Create a Flask web application instance
app = Flask(__name__)

# --- Helper Function: Load Menu from menu.txt ---
# This function is adapted from your original main.py
def load_menu():
    """
    Loads the menu from a specified text file.
    Expected format: ItemName,Price (one item per line)
    Returns a dictionary with item names (Title Case) as keys and prices as values.
    """
    # Use the absolute path to ensure Flask finds the file
    menu_filepath = os.path.join(os.path.dirname(__file__), 'menu.txt')
    menu_data = {}
    try:
        with open(menu_filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    item, price_str = line.split(',')
                    menu_data[item.strip().title()] = int(price_str.strip())
                except ValueError:
                    print(f"Warning: Skipping malformed line in menu file: '{line}'")
    except FileNotFoundError:
        print(f"\nError: Menu file '{menu_filepath}' not found.")
        print("Please create 'menu.txt' in the same directory as 'app.py' with items like 'Pizza,50'.")
        return None
    except Exception as e:
        print(f"\nAn unexpected error occurred while loading menu: {e}")
        return None
    return menu_data

# --- Flask Routes (API Endpoints) ---

@app.route('/')
def index():
    """
    Renders the main HTML page for the kiosk.
    This is the first page the user sees.
    """
    return render_template('index.html')

@app.route('/api/menu', methods=['GET'])
def get_menu():
    """
    API endpoint that returns the menu as a JSON object.
    The frontend JavaScript will call this to display the menu.
    """
    menu_data = load_menu()
    if menu_data is None:
        return jsonify({'error': 'Menu not found'}), 500
    return jsonify(menu_data)

@app.route('/api/order', methods=['POST'])
def place_order():
    """
    API endpoint that receives an order from the frontend.
    It calculates the total and prints it to the server's console.
    """
    data = request.json
    order_items = data.get('items', [])
    menu_data = load_menu()
    total_cost = 0

    # Basic validation and total calculation
    for item_data in order_items:
        item_name = item_data.get('item', '').strip().title()
        quantity = item_data.get('quantity')
        
        if item_name in menu_data and isinstance(quantity, int) and quantity > 0:
            total_cost += quantity * menu_data[item_name]
        else:
            return jsonify({'status': 'error', 'message': f'Invalid item or quantity for {item_name}'}), 400

    print(f"Order Received! Total cost: Rs.{total_cost:.2f}")

    response = {
        'status': 'success',
        'message': 'Order processed!',
        'total_amount': total_cost
    }
    return jsonify(response)

# --- Main Execution Block ---
# This block runs the Flask server when the file is executed
if __name__ == '__main__':
    app.run(debug=True)
