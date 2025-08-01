import os
MENU_FILE = "C:\Coding\projects\menu.txt"

def load_menu(filepath):
    """
    Loads the menu from a specified text file.
    Expected format: ItemName,Price (one item per line)
    Returns a dictionary with item names (Title Case) as keys and prices as values.
    """
    menu_data = {}
    try:
        with open(filepath, 'r') as f:
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
        print(f"\nError: Menu file '{filepath}' not found.")
        print("Please create 'menu.txt' in the same directory as 'main.py' with items like 'Pizza,50'.")
        return None # Indicate failure to load menu
    except Exception as e:
        print(f"\nAn unexpected error occurred while loading menu: {e}")
        return None
    return menu_data

def display_menu(menu):
    print("\n--- Our Menu ---")
    if not menu:
        print("Menu is empty. Please add items to 'menu.txt'.")
        return
    for item, price in menu.items():
        print(f"{item:<15} : Rs.{price:>5.2f}") 
    print("----------------")

def display_current_order(customer_order):
    if not customer_order:
        print("\nYour cart is empty.")
        return

    print("\n--- Your Current Order ---")
    total_items_cost = 0
    print(f"{'Item':<15} {'Qty':<5} {'Price':<10} {'Subtotal':<10}")
    print("-" * 50)
    for entry in customer_order:
        item = entry['item']
        quantity = entry['quantity']
        price = entry['price']
        subtotal = quantity * price
        total_items_cost += subtotal
        print(f"{item:<15} {quantity:<5} Rs.{price:<7.2f} Rs.{subtotal:<7.2f}")
    print("-" * 50)
    print(f"{'Total Cost':<30} Rs.{total_items_cost:<7.2f}")
    print("--------------------------")
    return total_items_cost

def process_order(menu):
    customer_order = []
    ordering = True

    while ordering:
        display_menu(menu)
        item_input = input("\nEnter the item name you want to order (or 'done' to finish): ").strip().title()

        if item_input == 'Done':
            ordering = False
            continue

        if item_input in menu:
            try:
                quantity_input = input(f"How many {item_input}s would you like? ")
                quantity = int(quantity_input)
                if quantity <= 0:
                    print("Quantity must be a positive number. Please try again.")
                    continue
                
                item_price = menu[item_input]
                customer_order.append({'item': item_input, 'quantity': quantity, 'price': item_price})
                print(f"{quantity} x {item_input} added to your order.")
                
                add_more = input("Add more items? (Yes/No): ").strip().title()
                if add_more == "No":
                    ordering = False

            except ValueError:
                print("Invalid quantity. Please enter a whole number.")
        else:
            print("Sorry, that item is not on our menu. Please check the spelling or type 'done'.")
    
    return customer_order

def checkout(customer_order):
    if not customer_order:
        print("\nNo items in your order. Nothing to checkout.")
        return

    grand_total = display_current_order(customer_order)
    
    print(f"\nYour Grand Total is: Rs.{grand_total:.2f}")

    while True:
        try:
            amount_paid_str = input("Enter amount paid by customer: Rs.")
            amount_paid = float(amount_paid_str)

            if amount_paid < grand_total:
                print(f"Amount paid is less than total. Please pay Rs.{grand_total - amount_paid:.2f} more.")
            else:
                change = amount_paid - grand_total
                print(f"\nAmount Paid: Rs.{amount_paid:.2f}")
                print(f"Your Change: Rs.{change:.2f}")
                print("\nThank you for your order! Enjoy your meal!")
                break
        except ValueError:
            print("Invalid amount. Please enter a numerical value.")
        except Exception as e:
            print(f"An error occurred during payment: {e}")

def main():
    print("Welcome to the Simple Restaurant Order Kiosk!")

    menu = load_menu(MENU_FILE)
    if menu is None:
        print("Exiting program due to menu loading error.")
        return

    customer_order = process_order(menu)
    
    if customer_order:
        checkout(customer_order)
    else:
        print("\nNo items were ordered. Goodbye!")


if __name__ == "__main__":
    main()