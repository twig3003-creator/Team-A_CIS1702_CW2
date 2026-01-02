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
        exit() # end program since nothing can be done after this



#save inventory to file
def save_data(data):
    with open("inventory.json", "w") as file: # automatically closes the file when done
        data = sorted(data, key=lambda x: int(x["id"])) # when adding or updating items, sort them into numerical order by id
        json.dump(data, file, indent=4) # put data into file with correct format
        return (data) # return data, since it was changed by the lambda function which sorted it



#you can add a new item here
def add_item(data):
    while True: # repeat this loop until a valid, unused ID is submitted
        invalid_id = False
        item_id = input("ID: ")
        
        if len(item_id.strip()) == 0: # removes any spaces and checks length, so you can't just enter a space
            print("ID should not be empty")
            invalid_id = True
        
        for item in data:
            if item["id"] == item_id:
                print ("Item ID already exists, please try again.")
                invalid_id = True
                break
        
        if invalid_id == False:
            break

    while True:
        name = input("Name: ")
        if len(name.strip()) == 0:
            print ("Name should not be empty.")
        else:
            break
    
    while True: # loop allows for reentering values
        try: # prevents invalid data types
            price = round(float(input("Price: ")), 2)
            break
        except ValueError:
            print ("Invalid input. Input value must be a float or integer.")
    
    while True:
        try:
            quantity = int(input("Quantity: "))
            break
        except ValueError:
            print("Invalid input. Input value must be an integer.")

    # originally was "Save?", didn't make sense to keep it as such since the data should already get saved or be saved manually
    # everything is same, just changed print statements and swapped the if requirements
    save_now = input("Cancel? (Y/N): ").upper()
    
    if save_now == "N":
        item = {"id": item_id, "name": name, "price": price, "quantity": quantity}
        data.append(item)
        print("Item added.")
        return(save_data(data)) # returns the data, since it gets sorted in sava_data() function
    else:
        print("Cancelled.")



#all items in inventory
def view_items(data):
    if not data:
        print("No items found.")
    else:
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
            if len(name.strip()) == 0:
                pass
            else:
                item["name"] = name

            while True:
                try:
                    price = input("New price: ")
                    if len(price.strip()) == 0: # normally would combine input and assignment ( item["price"] = input(float(price) ) but entering nothing generates an error
                        pass
                    else:
                        item["price"] = float(price)
                    break
                except ValueError:
                    print ("Invalid input. Input value must be a float or integer.")
            
            while True:
                try:
                    quantity = input("New quantity: ")
                    if len(quantity.strip()) == 0:
                        pass
                    else:
                        item["quantity"] = int(quantity)
                    break
                except ValueError:
                    print ("Invalid input. Input value must be an integer.")

            print("Item updated.")
            return(save_data(data))
    
    print("ID not found.")



#search by name name or ID
def search_item(data):
    while True: # keep giving inputs until valid name or id is entered
        option = input("Search by name or ID? ")
        
        if option.lower() != "name" and option.lower() != "id": # make sure it's valid input
            print ("Input not recognized, try again.")
        else:
            search = input(f"Enter {option}: ").lower()
            found = False
       
            if option.lower() == "name":
                for item in data: # compare against every item in the data
                    if search in item["name"].lower():
                        print(f"ID: {item['id']} / Name: {item['name']} / £{item['price']:.2f} / Qty: {item['quantity']}")
                        found = True
                        break
                break
    
            elif option.lower() == "id":
                for item in data:
                    if search in item["id"].lower():
                        print(f"ID: {item['id']} / Name: {item['name']} / £{item['price']:.2f} / Qty: {item['quantity']}")
                        found = True
                        break
                break
            
    if found == False:
        print ("Item was not found.")
                


#clear all
def clear_inventory(data):
    confirm = input("Clear all items? (Y/N): ").upper()
    if confirm == "Y": 
        data.clear() # deletes every item in data
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
                return (data)
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
def generate_report(data):
    total_items = len(data) #counts the number of unique items
    total_value = sum(item['price'] * item['quantity'] for item in data) #total financial value of all stock
    low_stock_items = [item for item in data if item['quantity'] < 5] #items with quantity below 5

    print("----- Inventory Report -----")
    print(f"Total unique items: {total_items}")
    print(f"Total inventory value: £{total_value:.2f}")
    low_stock_report(data)



#menu
def main():
    os.system('cls' if os.name == 'nt' else 'clear') # clears the terminal
    data = load_data()
    
    while True: # let user choose options multiple times
        print("1. Add Item") # we could make this into 1 print statement using \n for new lines
        print("2. View Items")
        print("3. Update Item")
        print("4. Search Item")
        print("5. Delete Item")
        print("6. Clear Inventory")
        print("7. Low Stock Report")
        print("8. Generate Report") 
        print("9. Save data") # not sure why this exists, since data is automatically saved?
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
            generate_report(data)

        elif option == "9":
            data = save_data(data)
            print("Saved.")
        
        elif option == "10": # allows user to exit program by breaking out of main loop
            print("Exiting program.")
            break
            
        else:
            print("Invalid option.") # if an invaldi option is entered, let them enter a new option
        print ("====================")

if __name__ == "__main__": # makes it so the program doesn't run when it's imported, stopping it from breaking or interrupting other programs
    main()
