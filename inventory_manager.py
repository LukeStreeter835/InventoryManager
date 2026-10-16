"""A command-line inventory manager for CPS 310.

Author: Luke Streeter
Course: CPS 310
"""

#File name for where inventory will be perserved
INVENTORY_FILE = "inventory.txt"


def view_inventory(inventory):
    i = 1
    for x in inventory:
        print(f"{i}. {x}")
        i+=1

    print("============================")

def add_item(name, category, qty, inventory):
    """Will add a new item into the list of dictionaries"""

    #add new key values to dictionary
    tempDictionary = {
        "Name": name,
        "Category": category,
        "Quantity": qty
    }
    inventory.append(tempDictionary)

    print("Item succsesfully added to inventory")
    print()

def load_inventory(filename):
    """Will load inventory items from inventory.txt"""
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
    #display inventory so user can see selection
    view_inventory(inventory)

    #take user input to select the right dictionary
    choice = int(input("What inventory item do you want? (please select using number)\n"))
    print("============================")

    #display dictionary so veiwer can verify its correct 
    print(inventory[choice - 1])
    print("============================")

    #ask user to change qty
    qtychange = input("What would you like the new qunatity to be?\n")

    #change qty
    inventory[choice - 1]["Quantity"] = qtychange

def remove_item(inventory):
    #display list so user can see selection
    view_inventory(inventory)

    #take user input to get dictionary
    choice = int(input("Which item would you like to remove? (please select using number)\n"))
    print("============================")

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
            add_item("Headphones", "Tech", 1, inventory)
            save_inventory(inventory, INVENTORY_FILE)
        elif choice == "3":
            update_quantity(inventory)
            save_inventory(inventory, INVENTORY_FILE)
        elif choice == "4":
            remove_item(inventory)
            save_inventory(inventory, INVENTORY_FILE)
        elif choice == "7":
            break
        else:
            print("Please enter 1 or 2")

if __name__ == "__main__":
    main()