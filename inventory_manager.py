"""A command-line inventory manager for CPS 310.

Author: Luke Streeter
Course: CPS 310
"""

#File name for where inventory will be perserved
INVENTORY_FILE = "inventory.txt"

def load_inventory():
    """Will load inventory items from inventory.txt"""
    return

def view_inventory(inventory):
    for x in inventory:
        print(x)
        print("============================")

def add_item(name, category, qty, inventory):
    """Will add a new item into the list of dictionaries"""

    tempDictionary = {
        "Name": name,
        "Category": category,
        "Quantity": qty
    }
    inventory.append(tempDictionary)

    print("Item succsesfully added to inventory")
    print()

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
    inventory = []
    inventory.append(load_inventory())

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