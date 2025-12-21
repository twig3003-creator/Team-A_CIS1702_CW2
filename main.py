import json
import os

#this loads the inventory / or you can start with a new one
def load_data():
    # changed code here, since it only worked with an existing inventory.json
    # kept old code in case this creatures bugs
    if os.path.exists("inventory.json") == True:
        pass
    else:
        print("File does not exist, creating new file.")
        with open("inventory.json", "a"):
            pass

    with open("inventory.json", "r") as file:
        try:
            return json.load(file)
        except:
            print("File empty.")
            return []
    
#     # old code
#     return []
    
#     if os.path.exists("inventory.json"):
#         with open("inventory.json", "r") as file:
#             try:
#                 return json.load(file)
#             except:
#                 print("file empty, starting new")
#                 return []
#     return []

#save inventory to file
def save_data(data):
    with open("inventory.json", "w") as file:
        data = sorted(data, key=lambda x: int(x["id"])) # when adding or updating items, sort them into numerical order by id
        json.dump(data, file, indent=4)
        return (data)

#you can add a new item heree
def add_item(data):
    
    while True:
        exists = False
        item_id = input("ID: ")
        for item in data:
            if item["id"] == item_id:
                print ("Item ID already exists, please try again.")
                exists = True
                break
        if exists == False:
            break

    name = input("Name: ")
    while True: # loop allows for reentering values
        try: # prevents invalid data types
            price = float(input("Price: "))
            break
        except:
            print ("Invalid input. Input value must be a float or integer.")
    while True:
        try:
            quantity = int(input("Quantity: "))
            break
        except:
            print("Invalid input. Input value must be an integer.")
    
    save_now = input("Save now? (Y/N): ").upper()
    
    if save_now == "Y":
        item = {"id": item_id, "name": name, "price": price, "quantity": quantity}
        data.append(item)
        print("Saved.")
        return(save_data(data)) # returns the data, since it gets sorted in sava_data() function
    else:
        print("Cancelled.")

#all items in inventory
def view_items(data):
    if not data:
        print("No items found.")
        return
    print("--- Inventory ---")
    for item in data:
        print(f"ID: {item['id']} / Name: {item['name']} / £{item['price']:.2f} / Qty: {item['quantity']}")

#update item
def update_item(data):
    item_id = input("Enter ID to update: ")
    for item in data:
        if item["id"] == item_id:
            print("Leave blank to skip update.")
            
            name = input("New name: ")
            if name == (""):
                pass
            else:
                item["name"] = name

            while True:
                try:
                    price = input("New price: ")
                    if price == (""): # normally would combine input and assignment ( item["price"] =input(float(price) ) but entering nothing makes this impossible
                        pass
                    else:
                        item["price"] = float(price)
                    break
                except:
                    print ("Invalid input. Input value must be a float or integer.")
            
            while True:
                try:
                    quantity = input("New quantity: ")
                    if quantity == (""):
                        pass
                    else:
                        item["quantity"] = integer(quantity)
                    break
                except:
                    print ("Invalid input. Input value must be an integer.")

            print("Item updated.")
            return(save_data(data))
    
    print("ID not found.")

#search by name
def search_item(data):
    search = input("Search name: ").lower()
    found = False
    for item in data:
        if search in item["name"].lower():
            print(f"ID: {item['id']} / Name: {item['name']} / £{item['price']:.2f} / Qty: {item['quantity']}")
            found = True
    if not found:
        print("Nothing found.")

#clear all
def clear_inventory(data):
    confirm = input("Clear all items? (Y/N): ").upper()
    if confirm == "Y": 
        data.clear()
        print("Inventory cleared.")
        return(save_data(data))
    else:
        print("Cancelled.")

#delete single item
def delete_item(data):
    item_id = input("Enter ID to delete: ")
    for item in data:
        if item["id"] == item_id:
            confirm = input(f"Are you sure you want to delete '{item['name']}'? (Y/N): ").upper()
            if confirm == "Y":
                data.remove(item)
                print("Item deleted.")
                return(save_data(data))
            else:
                print("Cancelled.")
                return
    print("ID not found.")

#low stock report
def low_stock_report(data):
    print("--- Low Stock Report (Quantity below 5) ---")
    found = False
    for item in data:
        if item["quantity"] < 5:
            print(f"{item['name']} - Quantity: {item['quantity']}")
            found = True
    if not found:
        print("No low-stock items.")

#menu
def main():
    data = load_data()

#all options you can add more if u like but these are just the basic ones for now
    while True:
        #os.system('cls' if os.name == 'nt' else 'clear') # what does this do?
        print("1. Add Item")
        print("2. View Items")
        print("3. Update Item")
        print("4. Search Item")
        print("5. Delete Item")
        print("6. Clear Inventory")
        print("7. Low Stock Report")
        print("8. Sava data") # not sure why this exists, since data is automatically saved?
        print("====================") #seperator makes it more visually better

        #if u want to add more options above make sure u change the options below too
        option = input("Choose: ")
        print ("====================")

        if option == "1":
            data = add_item(data)

        elif option == "2":
            view_items(data)

        elif option == "3":
            data = update_item(data)

        elif option == "4":
            search_item(data)

        elif option == "5":
            data = delete_item(data)

        elif option == "6":
            data = clear_inventory(data)

        elif option == "7":
            low_stock_report(data)

        elif option == "8":
            data = save_data(data)
            print("Saved.")

        else:
            print("Invalid option.") #if a option is entered like 9 it would fail
        print ("====================")
def get_total_value(data):
    """Calculates the total financial value of all stock."""
    total = 0
    for item in data:
        total += (item['price'] * item['quantity'])
    return total

def main():
    data = load_data()

    while True:
        print("\n1. Add Item")
        print("2. View Items")
        print("3. Update Item")
        print("4. Search Item")
        print("5. Delete Item")
        print("6. Clear Inventory")
        print("7. Low Stock Report")
        print("8. Save Data")
        print("9. View Total Inventory Value") # New addition
        print("0. EXIT") # New addition
        print("====================")

        option = input("Choose: ")
        print ("====================")

        if option == "1":
            data = add_item(data)
        elif option == "2":
            view_items(data)
        elif option == "3":
            data = update_item(data)
        elif option == "4":
            search_item(data)
        elif option == "5":
            data = delete_item(data)
        elif option == "6":
            data = clear_inventory(data)
        elif option == "7":
            low_stock_report(data)
        elif option == "8":
            data = save_data(data)
            print("Saved.")
        elif option == "9":
            val = get_total_value(data)
            print(f"Total Value of all Stock: £{val:.2f}")
        elif option == "0":
            print("Exiting.")
            break
        else:
            print("Invalid option.")
        print ("====================")

if __name__ == "__main__":
    main()