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

    return name, category, qty
    

def add_item(inventory, name, category, qty):
    """Will add a new item into the list of dictionaries"""

    #do not let names and categories with | in it go in list
    if "|" in name:
            name = ""
    if "|" in category:
        category = ""
    
    #if qty is not a number, then deafault to -1
    if valid_int(qty) == False:
        qty = -1
    else:
        qty = int(qty)
    
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
                if(valid_int(qty)):
                    qty = int(qty)
                else:
                    qty = ""

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

def display_entree(inventory, user_choice):
    """Preforms the logic to get a specific item from the list"""
    #Make sure input is a number
    if valid_int(user_choice):
        user_choice = int(user_choice)

        #Make sure input is in bounds of list
        if user_choice > 0 and user_choice <= len(inventory):
            return inventory[user_choice - 1]
        
        else:
            return False
        
    else:
        return False

def update_item_qty(inventory, item_num, new_qty):
    """Will take the new qty, validate it, and then change the file accordingly"""

    #make sure new qty input is actually a number and is non-negative
    if valid_int(new_qty) and int(new_qty) >= 0:
        new_qty = int(new_qty)
        #update the qty of item
        inventory[item_num - 1]["Quantity"] = new_qty

    else:
        return False
    

def update_quantity(inventory):
    """Allows the ability to change quantities of a certain item in the list of dictionaries"""
    #display inventory so user can see selection
    view_inventory(inventory)

    #take user input to select the right dictionary
    choice = input("What inventory item do you want? (please select using number)\n")
    print("============================")

    #get the item correlated to the number and display it to the user
    current_item = display_entree(inventory, choice)
    if current_item != False:
        print(current_item)
        print("============================")

        #Ask for new qty
        new_qty = input("What would you like the new quantity to be?\n")

        #update the item qty
        is_valid_qty = update_item_qty(inventory, int(choice), new_qty)

        #show error message if item qty input was invalid, else display the successful entree change to user
        if is_valid_qty is False:
            print("The quantity input was not a valid number, log was not changed." \
            " If you want to change the quantity, please enter a digit that is non-negative")
        else:
            print("Quantity has changed.")

    #if the user's choice is not a valid item in the list, tell the user
    else:
        print("The input you gave was not a number in the list, no change in the log." \
        " For selecting an entree, make sure you are selecting its position on the list.")

def confirm_removal(inventory, choice, item_num):
    if(item_num >= 1 and item_num < len(inventory)):
        output = ""
        if choice.strip().lower() == "y":
            inventory.pop(item_num - 1)
            output = "Succsessfully removed item."
        elif choice.strip().lower() == "n":
            output = "Did not remove item."
        else:
            output = "Input was not valid, did not remove item. Next time, make sure to confirm with \"y\" \n" \
            "and back out with \"n\"."

        return output


def remove_item(inventory):
    """Rmove an item from list based on index position"""
    #display list so user can see selection
    view_inventory(inventory)

    #take user input to get dictionary
    choice = input("Which item would you like to remove? (please select using number)\n")
    print("============================")

    #get the the entree based on user input
    curr_entree = display_entree(inventory, choice)

    if curr_entree != False:

        #Show the entree and confirm if they want it removed
        should_remove = input(f"Would you like {curr_entree} removed? (y/n)\n")

        #validate input and remove item, and display deletion based on user input
        print(confirm_removal(inventory, should_remove, int(choice)))

    #if the entree input was invalid, tell the user
    else:
        print("Input recived was invalid. Please make sure you are selecting your input by order number in the list.")


def find_item_based_on_name(inventory, item_name):
    """Will take a item name and find it or similar matches in the list"""
    
    item_index = -1
    partial_item = []

    #make sure item name was left blank
    if(item_name.strip() != ""):
        #look through entire list of items
        for i in range(len(inventory)):
                #See if there are partial matches
                if(item_name.lower() in inventory[i]["Name"].lower()):
                    #add to a list of items 
                    partial_item.append(inventory[i])
                    #see if there is a 1-1 match
                    if inventory[i]["Name"].lower() == item_name.lower():
                        #hold onto index
                        item_index = i

    return item_index, partial_item

def search_inventory(inventory):
    """look through a given list of dictionaries and find matching names"""
    #get user input
    find_item = input("Enter item name you wish to search for: \n")
    print("============================")

    item_index, partial_item = find_item_based_on_name(inventory, find_item)

    #if 1-1 match, then show user exact list location and details
    if item_index != -1:
        print(f"Found item at position #{item_index + 1}: {inventory[item_index]}")
    #else if there were close matches, show user close matches
    elif len(partial_item) != 0:
        print(f"Could not find {find_item} exactly, here are some similar matches: ")
        for x in partial_item:
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
    category_count = Counter(item["Category"].lower() for item in inventory)
    # print(f"====================\n{category_count}\n========================")

    return unique_entries, total_quantity, low_stock_items, category_count

def print_summary(unique_entries, total_quantity, low_stock_items, category_count):
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
            #get user input for name, category, and qty
            name, category, qty = get_add_item()
            #put input into logic function
            add_item(inventory, name, category, qty)
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
            unique_entries, total_quantity, low_stock_items, category_count = inventory_summary(inventory)
            print_summary(unique_entries, total_quantity, low_stock_items, category_count)
        elif choice == "7":
            break
        else:
            print("Please enter a number 1-7")

if __name__ == "__main__":
    main()