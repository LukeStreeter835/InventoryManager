"""A command-line inventory manager for CPS 310.

Author: Luke Streeter
Course: CPS 310
"""

#Summary method uses import
from collections import Counter

#File name for where inventory will be perserved
INVENTORY_FILE = "inventory.txt"

def valid_int(str):
    """Takes a string and checks to see if its an interger"""
    try:
        int(str)
        return True
    except(ValueError, TypeError):
        return False

def view_inventory(inventory):
    """Shows whole list of dictionaries in console"""
    i = 1
    for x in inventory:
        print(f"{i}. {x}")
        i+=1

    print("============================")

def get_add_item():
    """Will get name, cat, and qty from user input"""
    #get user input
    name = input("What is the name of the item you would like to add?\n")
    category = input("What is the category of the item you would like to add?\n")
    qty = input("What is the quantity of the item you would like to add?\n")

    #if theres a | in the name or category, then make it an empty string
    if "|" in name:
        name = ""
    if "|" in category:
        category = ""

    #if qty is not a number, then deafault to -1
    if valid_int(qty) == False:
        qty = -1
    else:
        qty = int(qty)

    return name, category, qty
    

def add_item(inventory):
    """Will add a new item into the list of dictionaries"""

    #TODO: change add method to have input verification (especially for qty)
    #get user input for name, category, and qty
    name, category, qty = get_add_item()
    #make sure inputs are valid
    if name != "" and category != "" and qty >= 0:

        #add new key values to dictionary
        tempDictionary = {
            "Name": name,
            "Category": category,
            "Quantity": qty
        }
        inventory.append(tempDictionary)

        print("Item succsesfully added to inventory\n")

    else:
        print("Unable to add item due to one or more invalid inputs")

def load_inventory(filename):
    """Will load inventory items from text file"""
    inventory = []

    try:
        with open(filename, "r") as file:
            for line in file:
                #file format per line is: "name | category | quantity"
                #split the line into three seperate parts 
                name, category, qty = line.split("|", 2)

                #strip values of spaces
                name = name.strip()
                category = category.strip()
                qty = qty.strip()
                #convert qty to an interger
                qty = int(qty)

                #if one of the key's values are empty, then dont add it into list
                if(name != "" and category != "" and qty != ""):
                    inventory.append({"Name": name, "Category": category, "Quantity": qty})

    #return nothing if the program could not find the file
    except FileNotFoundError:
        return []

    #return new inventory value
    return inventory

def save_inventory(inventory, filename):
    """Save all inventory items to text file."""

    with open(filename, "w") as file:
        
        for i in range(len(inventory)):
            #file format: "name | category | quantity"
            #hold a temporary dictionary to pull name, cat, and qty from
            tempDic = inventory[i]
            name = tempDic["Name"]
            category = tempDic["Category"]
            quantity = tempDic["Quantity"]

            #Then write the name, cat, and qty formatted properly into the file
            file.write(f"{name} | {category} | {quantity}\n")

def update_quantity(inventory):
    """Allows the ability to change quantities of a certain item in the list of dictionaries"""
    #display inventory so user can see selection
    view_inventory(inventory)

    #take user input to select the right dictionary
    choice = input("What inventory item do you want? (please select using number)\n")
    print("============================")

    #make sure input was actually an int
    if valid_int(choice):
        choice = int(choice)

        #make sure number is also in range of list size
        if choice > 0 and choice <= len(inventory):
            #display dictionary so veiwer can verify its correct 
            print(inventory[choice - 1])
            print("============================")

            #ask user to change qty
            qtychange = input("What would you like the new qunatity to be?\n")

            #make sure input a int and that said int is non-negative
            if valid_int(qtychange) and int(qtychange) >= 0:
                #change qty
                inventory[choice - 1]["Quantity"] = int(qtychange)
            else:
                print("input was not valid, please enter a non-negative number")

        else:
            print(f"Input was out of range, please insert a number from 1 to {len(inventory)}")

    else:
        print("input was not valid, please enter a number")


def remove_item(inventory):
    """Rmove an item from list based on index position"""
    #display list so user can see selection
    view_inventory(inventory)

    #take user input to get dictionary
    choice = input("Which item would you like to remove? (please select using number)\n")
    print("============================")

    #validate input, make sure its an interger
    if valid_int(choice):
        choice = int(choice)

        #Make sure input is in range of list
        if choice > 0 and choice <= len(inventory):
            #display dictionary so user can verify its correct 
            shouldremove = input(f"Would you like {inventory[choice - 1]} removed? (y/n)\n")
            print("============================")

            #Validate input
            if shouldremove == "y":
                removeditem = inventory.pop(choice - 1)
                print(f"Successfully removed {removeditem}")
            elif shouldremove == "n":
                print(f"Did not remove {inventory[choice - 1]}")
            else:
                print("Please give a valid input. (y for yes or n for no)")

            print("============================")

        else:
            print("Input was out of range of list")

    else:
        print("Input was invalid, please enter a number")

def search_inventory(inventory):
    """look through a given list of dictionaries and find matching names"""
    #get user input
    finditem = input("Enter item name you wish to search for: \n")
    print("============================")
    partialitem = []
    itemindex = -1

    
    for i in range(len(inventory)):
        #See if there are partial matches
        if(finditem.lower() in inventory[i]["Name"].lower()):
            #add to a list of items 
            partialitem.append(inventory[i])
            #see if there is a 1-1 match
            if inventory[i]["Name"].lower() == finditem.lower():
                #hold onto index
                itemindex = i

    #if 1-1 match, then show user exact list location and details
    if itemindex != -1:
        print(f"Found item at position #{itemindex + 1}: {inventory[itemindex]}")
    #else if there were close matches, show user close matches
    elif len(partialitem) != 0:
        print(f"Could not find {finditem} exactly, here are some similar matches: ")
        for x in partialitem:
            print(x)
    else:
        print("No matches were found, sorry!")

    print("============================")

def inventory_summary(inventory):
    """Gives overview of entire inventory"""
    total_quantity = 0
    unique_entries = []
    #unique_entries_num = 0
    isUnique = True
    low_stock_items = 0
    category_qty = []

    

    for item in inventory:
        #accumulate total quantities
        total_quantity += int(item["Quantity"])
        
        #count up low stock items (if quantity < 5)
        if(int(item["Quantity"]) < 5):
            low_stock_items += 1

        #Count up number of unique items based on names
        #look through a list of all uniqe names already found
        for name in unique_entries:
            #if name of the item is already in the list, then break out of loop
            if(name == item["Name"]):
                isUnique = False
                break
            else:
                isUnique = True

        #if item was found to be unique after loop, then add to the unique list
        if isUnique:
            unique_entries.append(item["Name"])

    #count all the items in each category
    category_count = Counter(item["Category"] for item in inventory)

    #print the summary
    print("Inventory Summary:")
    print(f"Unique Items: {len(unique_entries)}")
    print(f"Total Quantity: {total_quantity}")
    print(f"Low-stock Items: {low_stock_items}\n")

    print("Items by Category: ")
    for category, count in category_count.items():
        print(f"{category}: {count}")

def display_menu():
    """Display menu selection"""
    print("1. View Inventory")
    print("2. Add an Item")
    print("3. Update an Item Quantity")
    print("4. Remove an Item")
    print("5. Search Inventory")
    print("6. View Inventory Summary")
    print("7. Exit")

def main():
    inventory = load_inventory(INVENTORY_FILE)

    while True:
        display_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            view_inventory(inventory)
        elif choice == "2":
            add_item(inventory)
            save_inventory(inventory, INVENTORY_FILE)
        elif choice == "3":
            update_quantity(inventory)
            save_inventory(inventory, INVENTORY_FILE)
        elif choice == "4":
            remove_item(inventory)
            save_inventory(inventory, INVENTORY_FILE)
        elif choice == "5":
            search_inventory(inventory)
        elif choice == "6":
            inventory_summary(inventory)
        elif choice == "7":
            break
        else:
            print("Please enter a number 1-7")

if __name__ == "__main__":
    main()