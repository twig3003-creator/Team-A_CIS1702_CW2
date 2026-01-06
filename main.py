import json
import os
import time

FILE_NAME = "inventory.json"


#clears the terminal screen 
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear") # why function for just this one line


#this loads the inventory or creates a new one if the file does not exist
def load_data():
    if not os.path.exists(FILE_NAME): # checks if the file exists
        print("File does not exist, creating new file.")
        with open(FILE_NAME, "w") as file: # creates file and automatically closes it when finished
            json.dump([], file, indent=4)
        return []

    try:
        with open(FILE_NAME, "r") as file:
            if os.path.getsize(FILE_NAME) == 0: # if file is empty, this creates a JSONDecodeError since it doesn't have any format
                print("File is empty. ")
                return []
            return json.load(file)
    except json.JSONDecodeError:
        print("Error: File does not meet the required JSON format.")
        return []


#save inventory to file
def save_data(data):
    data = sorted(data, key=lambda x: int(x["id"])) # lambda function sorts data in ascending numerical order by ID
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4) # overwrites existing data and replaces it with anything stored in 'data', which should be updated
    return data


#add a new inventory item
def add_item(data):
    while True: # force user to repeat loop unless the id is valid
        invalid_id = False
        item_id = input("ID: ").strip() # remove whitespace and blank characters

        if not item_id:
            print("ID should not be empty.")
            invalid_id = True

        #FIX: ensure ID is numeric to prevent save_data crash
        elif not item_id.isdigit(): 
            print("ID must be numeric.")
            invalid_id = True

        for item in data:
            if item["id"] == item_id:
                print("Item ID already exists.")
                invalid_id = True
                break

        if not invalid_id:
            break

    while True: # repeat until valid name
        name = input("Name: ").strip()
        if name:
            break
        print("Name should not be empty.")

    while True: # repeat until valid price
        try:
            price = round(float(input("Price: ")), 2) # rounds to 2 decimal places
            if price <= 0: # change to < 0: ? items could potentially be free
                print("Price must be greater than zero.")
            else:
                break
        except ValueError:
            print("Invalid input. Price must be a number.")

    while True: # repeat until valid quantity
        try:
            quantity = int(input("Quantity: "))
            if quantity < 0:
                print("Quantity must not be below zero.")
            else:
                break
        except ValueError:
            print("Invalid input. Quantity must be an integer.")

    confirm = input("Add item? (Y/N): ").upper()
    if confirm == "Y":
        data.append({
            "id": item_id,
            "name": name,
            "price": price,
            "quantity": quantity
        })
        print("Item added.")
        return save_data(data)

    print("Cancelled.")
    return data


#display all items in inventory
def view_items(data):
    if not data:
        print("No items found.")
        return

    print("--- Inventory ---")
    for item in data: # loop through all items in the inventory, print their contents in the correct format
        print(
            f"ID: {item['id']} | "
            f"Name: {item['name']} | "
            f"£{item['price']:.2f} | "
            f"Qty: {item['quantity']}"
        )


#update an existing item by ID
def update_item(data):
    item_id = input("Enter ID to update: ").strip()

    for item in data:
        if item["id"] == item_id: # checks the input against every item ID in the inventory
            print("Leave blank to skip update.")

            updated = False  #FIX: track whether changes occur

            name = input("New name: ").strip()
            if name: 
                item["name"] = name
                updated = True

            while True:
                price = input("New price: ").strip()
                if not price:
                    break
                try:
                    price = float(price)
                    if price > 0: # prevents negative prices --- change to >= 0? items could potentially be free
                        item["price"] = round(price, 2) # round to 2 decimal places
                        updated = True
                        break
                except ValueError:
                    pass
                print("Invalid price.")

            while True:
                quantity = input("New quantity: ").strip()
                if not quantity:
                    break
                try:
                    quantity = int(quantity)
                    if quantity >= 0:
                        item["quantity"] = quantity
                        updated = True
                        break
                except ValueError:
                    pass
                print("Invalid quantity.")

            #FIX: do not save if nothing changed
            if not updated:
                print("No changes made.")
                return data

            print("Item updated.")
            return save_data(data)

    print("ID not found.")
    return data


#search inventory by name or ID
def search_item(data):
    #FIX: loop until valid search option entered
    while True:
        option = input("Search by name or ID: ").lower().strip() #remove case sensitivity and any whitespaces
        if option in ["name", "id"]:
            break
        print("Invalid search option. Try again.")

    search = input(f"Enter {option}: ").lower().strip()
    found = False

    while not search:
        print(f"{option} cannot be blank.")
        search = input(f"Enter {option}: ").lower().strip()

    for item in data:
        if search in item[option].lower(): # loop through all items in the inventory and check if the input of the input category is equal to item's data
            print(
                f"ID: {item['id']} | "
                f"Name: {item['name']} | "
                f"£{item['price']:.2f} | "
                f"Qty: {item['quantity']}"
            )
            found = True

    if not found:
        print("Item not found.")


#delete a single item
def delete_item(data):
    item_id = input("Enter ID to delete: ").strip()

    for item in data:
        if item["id"] == item_id:
            confirm = input(f"Delete '{item['name']}'? (Y/N): ").upper()
            if confirm == "Y":
                data.remove(item)
                print("Item deleted.")
                return save_data(data)
            print("Cancelled.")
            return data

    print("ID not found.")
    return data


#report items with low stock
def low_stock_report(data):
    print("--- Low Stock Report (Below 5) ---")
    found = False

    for item in data:
        if item["quantity"] < 5:
            print(f"{item['name']} - Quantity: {item['quantity']}")
            found = True

    if not found:
        print("No low-stock items.")


#clear all items from inventory
def clear_all_items(data):
    if not data:
        print("Inventory is already empty.")
        return data

    confirm = input("Are you sure you want to clear ALL items? (Y/N): ").upper()
    if confirm == "Y":
        data.clear() # deletes all data
        print("All items cleared.")
        return save_data(data)

    print("Clear cancelled.")
    return data


#main menu loop
def main():
    data = load_data()
    time.sleep(3) # messages created by the load_data() function, which instantly get cleared by clear_screen()
                  # there needs to be time to read them
    while True:
        clear_screen()

        print("INVENTORY MANAGEMENT SYSTEM")
        print("===========================")
        print("1. Add Item")
        print("2. Update Item")
        print("3. View Stock")
        print("4. Search Item")
        print("5. Low Stock Report")
        print("6. Delete Item")
        print("7. Clear All Items")
        print("8. Save & Exit")
        print("===========================")

        option = input("Choose: ").strip()
        clear_screen()

        if option == "1":
            data = add_item(data)
        elif option == "2":
            data = update_item(data)
        elif option == "3":
            view_items(data)
        elif option == "4":
            search_item(data)
        elif option == "5":
            low_stock_report(data)
        elif option == "6":
            data = delete_item(data)
        elif option == "7":
            data = clear_all_items(data)
        elif option == "8":
            save_data(data)
            print("Data saved, Exiting.")
            break
        else:
            print("Invalid option.")

        input("\nPress Enter to continue...")


# ensures the program only runs when executed directly, so that it doesn't break any programs that this is imported into
if __name__ == "__main__":
    main()
