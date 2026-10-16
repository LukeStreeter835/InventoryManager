"""A command-line inventory manager for CPS 310.

Author: Luke Streeter
Course: CPS 310
"""

#File name for where inventory will be perserved
INVENTORY_FILE = "inventory.txt"


def view_inventory(inventory):
    for x in inventory:
        print(x)
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
        elif choice == "7":
            break
        else:
            print("Please enter 1 or 2")

if __name__ == "__main__":
    main()