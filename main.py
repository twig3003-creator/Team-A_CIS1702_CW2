import json
import os

#this loads the inventory / or you can start with a new one
def load_data():
    # changed code here, since it only worked with an existing inventory.json
    # kept old code in case this creates bugs
    if os.path.exists("inventory.json") == True: # checks if file exists
        pass
    else:
        print("File does not exist, creating new file.")
        with open("inventory.json", "a"): # creates file
            pass # continue to next part
    
    try:
        with open("inventory.json", "r") as file:
            if os.path.getsize("inventory.json") == 0: # checks if file has a size of 0, or is empty
                print("File empty. ")
                return [] # this would return a JSONDecodeError if the file was returned through json.load() since, as it's empty, it doesn't have the correct json format
            else:
                return json.load(file)
    except ValueError: # ValueError contains JSONDecodeError - when file is not formatted correctly
        print ("Error: File does not meet the required format")
        exit() #end program since nothing can be done after this
    
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
    with open("inventory.json", "w") as file: # automatically closes the file when done
        data = sorted(data, key=lambda x: int(x["id"])) # when adding or updating items, sort them into numerical order by id
        json.dump(data, file, indent=4) # put data into file with correct format
        return (data) # return data, since it was changed by the lambda function which sorted it

#you can add a new item here
def add_item(data):
    while True: # repeat this loop until a valid, unused ID is submitted
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

    # why are we giving this option?
    # the user already has the option to manually save in the main program
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
    for item in data: # go through every item in the data
        print(f"ID: {item['id']} / Name: {item['name']} / £{item['price']:.2f} / Qty: {item['quantity']}")

#update item
def update_item(data):
    item_id = input("Enter ID to update: ")
    for item in data: # loops through all items in data
        if item["id"] == item_id: # selects the corresponding item
            print("Leave blank to skip update.")
            
            name = input("New name: ")
            if name == (""):
                pass
            else:
                item["name"] = name

            while True:
                try:
                    price = input("New price: ")
                    if price == (""): # normally would combine input and assignment ( item["price"] = input(float(price) ) but entering nothing generates an error
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
                        item["quantity"] = int(quantity)
                    break
                except:
                    print ("Invalid input. Input value must be an integer.")

            print("Item updated.")
            return(save_data(data))
    
    print("ID not found.")

#search by name
def search_item(data):
    search = input("Search name: ").lower() # makes sure that the search doesn't fail because of inconsistent cases
    found = False
    for item in data: # compare against every item in the data
        if search in item["name"].lower():
            print(f"ID: {item['id']} / Name: {item['name']} / £{item['price']:.2f} / Qty: {item['quantity']}")
            found = True
    if not found:
        print("Item not found.")

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

#Generate report
def generate_report(inventory):
    total_items = len(inventory)#counts the number of unique items
    total_value = sum(item['price'] * item['quantity'] for item in inventory)#total financial value of all stock
    low_stock_items = [item for item in inventory if item['quantity'] < 5]#items with quantity below 5

    print("----- Inventory Report -----")
    print(f"Total unique items: {total_items}")
    print(f"Total inventory value: £{total_value:.2f}")
    print("Low stock items (Quantity below 5):")
    if low_stock_items:
        for item in low_stock_items:
            print(f"- {item['name']} (Qty: {item['quantity']})")#lists low stock items
    else:
        print("None")
    print("----------------------------")

#menu
def main():
    data = load_data()

    while True: # let user choose options multiple times
        #os.system('cls' if os.name == 'nt' else 'clear') # what does this do? it keeps missing with print statements and doesn't seem to serve a purpose
        print("1. Add Item")
        print("2. View Items")
        print("3. Update Item")
        print("4. Search Item")
        print("5. Delete Item")
        print("6. Clear Inventory")
        print("7. Low Stock Report")
        print("8. Save data") # not sure why this exists, since data is automatically saved?
        print("9. Generate Report") 
        print("10. Exit")
        print("====================") #seperator makes it visually better

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
        
        elif option == "9":
            generate_report(data)
        
        elif option == "10": # allows user to exit program by breaking out of main loop
            print("Exiting program.")
            break
            
        else:
            print("Invalid option.") # if an invaldi option is entered, let them enter a new option
        print ("====================")

if __name__ == "__main__": # makes it so the program doesn't run when it's imported, stopping it from breaking or interrupting other programs
    main()
