# Inventory Manager

Inventory Manager keeps a log of all the items in a companie's inventory.

## Current Features

-Loads preserved items from inventory text file
-Allows users to add items to the inventory
-Allows users to veiw items in inventory
-Will save all items added onto inventory text file
-Allows users to remove item from list and text file
-Allows users to update quantities of each item
-Allows users to search for an item based on its name
-Allows users to see a summary of current inventory

## Requirements

-Python 3

## Version Control

-This project uses git locallhy and github as an online repository. Please make sure when running or
working on the program that you are aware what version of the program you are on.

## Project Files

-`inventory_manager.py` - Main program that user use to access, view, and modify inventory
-`inventory.txt` - Text file used to preserved items added from inventory_manager
-`.gitignore` - Holds the files that git and git hub should ignore and not see
-`test_inventory_manager.py` - holds programs used for testing inventory_manager.py
-`AI_USEAGE.md` - holds log of how AI was used to help create the program
-`TESTING.md` - holds a log of what kind of testing was done for the program

## Running the Program

cd C:\Users\stree\OneDrive\Desktop\CPS310\HW_01 // Change directory to the correct filepath
python inventory_manager.py // run the program

## Inventory data format

```text
Data is stored in a specific way on the text file.
If you intend to add items directory to file, please note its formated like
"Name" | "Category" | "Quantity
```

## Testing Summary

-Briefly tested input validation for methods that use it
-tested item preservation in txt file
-tested logic

## Current Limitation

NOTE: Inventory manager cannot stack two same items in inventory text file