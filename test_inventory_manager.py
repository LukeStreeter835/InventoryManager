from collections import Counter

import pytest

from inventory_manager import load_inventory, save_inventory, find_item_based_on_name, confirm_removal, update_item_qty, display_entree, add_item, inventory_summary

@pytest.fixture
def demo_inventory():
    return [
        {"Name": "Rubber Ducks", "Category": "Toys", "Quantity": 500},
        {"Name": "Wallets", "Category": "Fashion", "Quantity": 34},
        {"Name": "Tires", "Category": "Automotive", "Quantity": 5},
        {"Name": "Rust Remover", "Category": "Automotive", "Quantity": 8}
    ]

############################ File Tests ############################

def test_load_inventory(tmp_path, demo_inventory):
    #Arrange
    test_file = tmp_path / "inventory.txt"
    test_file.write_text("Rubber Ducks | Toys | 500\nWallets | Fashion | 34\nTires | Automotive | 5\nRust Remover | Automotive | 8")

    #Act
    inventory = load_inventory(test_file)

    #Assert
    assert inventory == demo_inventory

def test_empty_inventory(tmp_path):
    #Arrange
    test_file = tmp_path / "inventory.txt"
    test_file.write_text("|||")
    expected_output = []

    #Act
    inventory = load_inventory(test_file)

    #Assert
    assert inventory == expected_output

def test_load_missing_file(tmp_path):
    #Arrange
    test_file = tmp_path / "DNE.txt"
    expected_outpu = []

    #Act
    inventory = load_inventory(test_file)

    #Assert
    assert inventory == []


def test_save_inventory(tmp_path, demo_inventory):
    #Arrange
    test_file = tmp_path / "inventory.txt"
    expected_text = "Rubber Ducks | Toys | 500\nWallets | Fashion | 34\nTires | Automotive | 5\nRust Remover | Automotive | 8\n"

    #Act
    save_inventory(demo_inventory, test_file)

    #Assert
    assert test_file.read_text() == expected_text

def test_save_empty_inventory(tmp_path):
    #Arrange
    test_file = tmp_path / "inventory.txt"
    expected_text = ""

    #Act
    save_inventory([], test_file)

    #Assert
    assert test_file.read_text() == expected_text

def test_save_load_inventory(tmp_path, demo_inventory):
    #Arrange
    test_file = tmp_path / "inventory.txt"

    #Act
    save_inventory(demo_inventory, test_file)
    inventory = load_inventory(test_file)

    #Assert
    assert inventory == demo_inventory

######################################## Search Tasks Test ####################################


@pytest.mark.parametrize(
        "looking_for, should_index, should_find",
        [
            ("Rubber Ducks", 0, [{"Name": "Rubber Ducks", "Category": "Toys", "Quantity": 500}]),
            ("Rubber", -1, [{"Name": "Rubber Ducks", "Category": "Toys", "Quantity": 500}]),
            ("R", -1, [{"Name": "Rubber Ducks", "Category": "Toys", "Quantity": 500},
                       {"Name": "Tires", "Category": "Automotive", "Quantity": 5}, 
                       {"Name": "Rust Remover", "Category": "Automotive", "Quantity": 8}]),
            ("Root Beer", -1, []),
            (" ", -1, [])
        ],
        ids= [
            "exact_item_name",
            "close_item_name",
            "more_than_one_close",
            "no_item_found",
            "no_input_given"
        ]
)
def test_search_inventory(demo_inventory, looking_for, should_index, should_find):
    #Arrange 

    #Act
    found_index, found_item = find_item_based_on_name(demo_inventory, looking_for)

    #Assert
    assert found_item == should_find
    assert found_index == should_index


#################################### Remove Items Tests ######################################
@pytest.mark.parametrize(
    "item_num, resulting_inventory",[
        (1, [{"Name": "Wallets", "Category": "Fashion", "Quantity": 34},
            {"Name": "Tires", "Category": "Automotive", "Quantity": 5},
            {"Name": "Rust Remover", "Category": "Automotive", "Quantity": 8}]),
        (3, [{"Name": "Rubber Ducks", "Category": "Toys", "Quantity": 500},
            {"Name": "Wallets", "Category": "Fashion", "Quantity": 34},
            {"Name": "Rust Remover", "Category": "Automotive", "Quantity": 8}]),
        (4, [{"Name": "Rubber Ducks", "Category": "Toys", "Quantity": 500},
            {"Name": "Wallets", "Category": "Fashion", "Quantity": 34},
            {"Name": "Tires", "Category": "Automotive", "Quantity": 5},
            {"Name": "Rust Remover", "Category": "Automotive", "Quantity": 8}]),
        (0, [{"Name": "Rubber Ducks", "Category": "Toys", "Quantity": 500},
            {"Name": "Wallets", "Category": "Fashion", "Quantity": 34},
            {"Name": "Tires", "Category": "Automotive", "Quantity": 5},
            {"Name": "Rust Remover", "Category": "Automotive", "Quantity": 8}]),
        (-1, [{"Name": "Rubber Ducks", "Category": "Toys", "Quantity": 500},
            {"Name": "Wallets", "Category": "Fashion", "Quantity": 34},
            {"Name": "Tires", "Category": "Automotive", "Quantity": 5},
            {"Name": "Rust Remover", "Category": "Automotive", "Quantity": 8}]),
        (5, [{"Name": "Rubber Ducks", "Category": "Toys", "Quantity": 500},
            {"Name": "Wallets", "Category": "Fashion", "Quantity": 34},
            {"Name": "Tires", "Category": "Automotive", "Quantity": 5},
            {"Name": "Rust Remover", "Category": "Automotive", "Quantity": 8}])
    ],
    ids= [
        "remove_first_item",
        "remove_middle_item",
        "remove_last_item",
        "remove_0_item",
        "remove_negative_item",
        "remove_larger_than_index_item"
    ]

)
def test_remove_item(demo_inventory, item_num, resulting_inventory):
    #Arrange
    confirm_choice = "y"

    #Act
    confirm_removal(demo_inventory, confirm_choice, item_num)

    #Assert
    assert demo_inventory == resulting_inventory

################################### Update Quantity Test #############################

@pytest.mark.parametrize(
    "new_qty, expected_output",
    [
        (72, {"Name": "Wallets", "Category": "Fashion", "Quantity": 72}),
        (0, {"Name": "Wallets", "Category": "Fashion", "Quantity": 0}),
        (-72, {"Name": "Wallets", "Category": "Fashion", "Quantity": 34})
    ],
    ids = [
        "valid_change",
        "zero_quantity",
        "negative_quantity"
    ]
)
def test_update_quantity(demo_inventory, new_qty, expected_output):
    #Arrange
    item_num = 2
    #Act
    update_item_qty(demo_inventory, item_num, new_qty)

    #Assert
    assert demo_inventory[item_num - 1] == expected_output

def test_update_quantity_invalid_item_num(demo_inventory):
    #Arrange
    item_num = 0
    expected_result = False
    
    #Act
    entree = display_entree(demo_inventory, item_num)

    #Assert
    entree = False


########################################## Add Item Validation Test ###################################

@pytest.mark.parametrize(
    "item_name, item_category, item_qty, expected_inventory",
    [
        ("Headphones", "Tech", 3, [{"Name": "Rubber Ducks", "Category": "Toys", "Quantity": 500},
            {"Name": "Wallets", "Category": "Fashion", "Quantity": 34},
            {"Name": "Tires", "Category": "Automotive", "Quantity": 5},
            {"Name": "Rust Remover", "Category": "Automotive", "Quantity": 8},
            {"Name": "Headphones", "Category": "Tech", "Quantity": 3}]),
        ("", "", 3, [{"Name": "Rubber Ducks", "Category": "Toys", "Quantity": 500},
            {"Name": "Wallets", "Category": "Fashion", "Quantity": 34},
            {"Name": "Tires", "Category": "Automotive", "Quantity": 5},
            {"Name": "Rust Remover", "Category": "Automotive", "Quantity": 8}]),
        ("|", "|", 3, [{"Name": "Rubber Ducks", "Category": "Toys", "Quantity": 500},
            {"Name": "Wallets", "Category": "Fashion", "Quantity": 34},
            {"Name": "Tires", "Category": "Automotive", "Quantity": 5},
            {"Name": "Rust Remover", "Category": "Automotive", "Quantity": 8}]),
        ("Headphones", "Tech", -1, [{"Name": "Rubber Ducks", "Category": "Toys", "Quantity": 500},
            {"Name": "Wallets", "Category": "Fashion", "Quantity": 34},
            {"Name": "Tires", "Category": "Automotive", "Quantity": 5},
            {"Name": "Rust Remover", "Category": "Automotive", "Quantity": 8}])
    ],
    ids = [
        "valid_item",
        "empty_item_name_and_category",
        "|_in_name_and_category",
        "negative_qty"
    ]
)
def test_add_item(demo_inventory, item_name, item_category, item_qty, expected_inventory):
    #Arrange

    #Act
    add_item(demo_inventory, item_name, item_category, item_qty)

    #Assert
    assert demo_inventory == expected_inventory

############################################## Inventory Summary Test ###################################

def test_inventory_summary(demo_inventory):
    #Arrange
    test_inventory = [{"Name": "Rubber Ducks", "Category": "Toys", "Quantity": 500},
            {"Name": "Wallets", "Category": "Fashion", "Quantity": 34},
            {"Name": "Tires", "Category": "Automotive", "Quantity": 5},
            {"Name": "Wallets", "Category": "Fashion", "Quantity": 20},
            {"Name": "Building Blocks", "Category": "toys", "Quantity": 4}]
    e_unique_entries = 4
    e_total_quantity = 563
    e_low_stock = 1
    e_cat_count = Counter({"toys": 2, "fashion": 2, "automotive": 1})
    
    #Act
    unique_entries, total_quantity, low_stock_items, category_count = inventory_summary(test_inventory)
    
    #Assert
    assert e_cat_count == category_count
    assert e_low_stock == low_stock_items
    assert e_total_quantity == total_quantity
    assert e_unique_entries == len(unique_entries)

