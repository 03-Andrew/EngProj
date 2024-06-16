from Items import Material, MaterialList
from colorama import Fore, Style
import datetime

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

material_list = MaterialList()
material_list.read_materials()
all_materials = material_list.get_all_materials()
all_categories = material_list.get_all_categories()

services = ["Equipment Rental Services for tools and machinery ", "Building Material Delivery Services"]

equipments = [["Electric Drill", 200], ["Angle Grinder", 200], ["Circular Saw", 300],
              ["Jigsaw", 600], ["Impact Wrench", 200], ["Rotary Hammer", 200], ["Power Sander", 450],
              ["Heat Gun", 300]]


def print_title():
    print(r'''
     ______       _ _     ____  ___          _            
     | ___ \     (_) |   | |  \/  |         | |           
     | |_/ /_   _ _| | __| | .  . | __ _ ___| |_ ___ _ __ 
     | ___ \ | | | | |/ _` | |\/| |/ _` / __| __/ _ \ '__|
     | |_/ / |_| | | | (_| | |  | | (_| \__ \ ||  __/ |   
     \____/ \__,_|_|_|\__,_\_|  |_/\__,_|___/\__\___|_|
    
                  By: Name1, Name2, Name3
                      Group no. [A161]
     ╭────────────────────────────────────────────────────╮
     │                   Description                      │    
     │ Welcome to BuildMaster, your one-stop shop for all │
     │      your construction and renovation needs.       │    
     │                       ....                         │                    
     ╰────────────────────────────────────────────────────╯
    ''')


def print_start_page():
    print("\n\t" + "─" * 55)
    print("\tSelect an option: \n\t[1] Browse Products [2] Browse Services [3] Exit")

    while True:
        choice = input("\tPlease enter you choice: ")
        if choice == '1':
            show_categories()
            break
        elif choice == '2':
            show_services()
            break
        elif choice == '3':
            bye_page()
            break
        else:
            print("\tinvalid choice")


def show_categories():
    i = 1
    print("\n\t" + "─" * 55)  # Separator line
    print("\tSelect a category")
    for category in all_categories:
        print(f"\t{Fore.CYAN}[{i}]  {Style.RESET_ALL}{category:<25}")
        i += 1

    while True:
        choice = input("\tEnter your choice [Enter 'b' to go back]:")
        if choice == "b":
            print_start_page()
            return
        elif not choice.isdigit():
            print("Choice is not a digit")
            continue
        elif int(choice) < 0 or int(choice) > len(all_categories):
            print("Invalid choice")
            continue

        browse_items(all_categories[int(choice) - 1])
        break


def show_services():
    print("\n\t" + "─" * 55)  # Separator line
    print("\tAvailable Services")
    i = 1
    for service in services:
        print("\t" + Fore.CYAN + "[{}]".format(i) + Style.RESET_ALL + "{:>3}".format(service))
        i += 1

    while True:
        choice = input("\tChoose a service: ")
        if not choice.isdigit():
            print("\tInvalid choice. Enter a digit")
            continue
        elif choice == "b":
            print_start_page()
            return
        elif choice == "1":
            equipment_rental()
            return
        elif choice == "2":
            print(1)
        else:
            print("\tChoice out of range.")
            continue


def equipment_rental():
    print("\n\tAvailable Equipment for rent")
    print("\t" + "─" * 55)  # Separator line
    print("\t" + Fore.BLUE + "{:<3}".format("") + Style.RESET_ALL + " " +
          Fore.BLUE + "{:<25}".format("Name") + Style.RESET_ALL + " " + Fore.BLUE +
          "{:<10}".format("Price/Day"))
    i = 1
    for tool in equipments:
        print("\t" + Fore.CYAN + "{:<3}".format(i) + Style.RESET_ALL +
              " {:<25} {:<10}".format(tool[0], tool[1]))
        i += 1
    print("\t" + "─" * 55)  # Separator line

    rent_item_page()


def rent_item_page():
    rented_items = []
    total_cost = 0
    while True:
        choice = input("\t(Enter 'd' to finish or 'b' to go back)\n\tEnter item to rent: ")
        if choice.lower() == 'b':
            print_start_page()
            return
        if choice.lower() == 'd':
            if not rented_items:
                print("\tNo items selected")
                print_start_page()
                return
            break
        try:
            choice_index = int(choice) - 1
            if choice_index < 0 or choice_index >= len(equipments):
                print("\tInvalid item number. Please enter a valid item number.")
                continue
            rented_item = equipments[choice_index]
            days = int(input("\tRent for how many days: "))
            price_per_day = float(rented_item[1])
            total_cost += price_per_day * days
            rented_items.append((rented_item[0], price_per_day, days))

        except ValueError:
            print("\tInvalid input. Please enter a number.")

    print("\tRented Items:")
    payment_page2(rented_items, total_cost)


def browse_items(category):
    print("\n\t" + "─" * 55)  # Separator line
    print(f"\t{category}")
    print("\t" + "─" * 55)  # Separator line
    print("\t" + Fore.BLUE + "{:<3}".format("") + Style.RESET_ALL + " " +
          Fore.BLUE + "{:<25}".format("Name") + Style.RESET_ALL + " " + Fore.BLUE +
          "{:<10}".format("Price") + Style.RESET_ALL + " " + Fore.BLUE + "{:<10}".format("Sold per") + Fore.BLUE
          + "{:<10}".format("Stock") + Style.RESET_ALL)
    print("\t" + "─" * 55)  # Separator line
    filtered_materials = [material for material in all_materials.values() if material.category == category]
    i = 1
    for material in filtered_materials:
        print("\t" + Fore.CYAN + "{:<3}".format(i) + Style.RESET_ALL +
              " {:<25} {:<10} {:<10} {:<10}".format(material.name, material.price, material.measurement,
                                                    material.stock))
        i += 1
    print("\t" + "─" * 55)
    browse_items_input(filtered_materials)


def get_valid_quantity(selected_material):
    while True:
        try:
            quantity = int(input("\tEnter quantity: "))
            if quantity <= 0:
                print("\tInvalid quantity. Please enter a positive integer.")
            elif quantity > selected_material.stock:
                print(
                    f"\tNot enough stock available for {selected_material.name}. Available stock: {selected_material.stock}")
            else:
                return quantity
        except ValueError:
            print("\tInvalid input. Enter a valid integer.")


def purchase_items(selected_material, items_purchased):
    quantity = get_valid_quantity(selected_material)
    sub_total = selected_material.price * quantity
    print("\tPurchased {} {} for Php{}.".format(quantity, selected_material.name, sub_total))
    items_purchased.append([selected_material, quantity, sub_total])


def browse_items_input(filtered_materials):
    items_purchased = []
    print("\n\t[Enter 'd' to finish shopping or 'c' to cancel orders]")
    while True:
        choice = input("\n\tEnter Item ID : ")
        if choice.lower() == "d":
            if items_purchased:
                payment_page(items_purchased)
            else:
                print("\tNo items purchased.")
                print_start_page()
            break
        elif choice.lower() == "c":
            if confirm_cancellation():
                print("\tOrder Cancelled")
                print_start_page()
                return
        elif not choice.isdigit():
            print("\tInvalid input. Enter a digit")
        elif int(choice) < 0 or int(choice) >= len(filtered_materials):
            print("\tInvalid Item ID. Please try again.")
        else:
            selected_material = filtered_materials[int(choice) - 1]
            print(f"\tAvailable stock for {selected_material.name}: {selected_material.stock}")
            purchase_items(selected_material, items_purchased)


def payment_page(items_purchased):
    print("\t" + "─" * 55)
    total_amount, change = 0, 0
    for item in items_purchased:
        material, quantity, subtotal = item
        total_amount += subtotal
        print("\t{:<10} {:<20} {:<10} Php{:>7.2f}".format(material.id, material.name, quantity, subtotal))
        # Deduct the sold items from stock
        material_list.sell_items(material.id, quantity)
    print("\t" + "─" * 55)
    print("\t{:<43} Php{:>7.2f}".format("Total", total_amount))
    print("\t" + "─" * 55)

    while True:
        try:
            payment_amount = float(input("\tEnter payment amount: "))
            if payment_amount < total_amount:
                print("\tPayment amount is less than the total amount. Please try again.")
                continue
            change = payment_amount - total_amount
            print("\n\t" + "─" * 55)
            print("\tPayment accepted. Your change is Php{:.2f}".format(change))
            print("\tReceipt Generated")
            break
        except ValueError:
            print("\tInvalid input. Please enter a valid amount.")

    print("\t" + "─" * 55)  # Separator line
    generate_receipt(items_purchased, total_amount, payment_amount, change, "p")
    ask_for_another_transaction()


def payment_page2(items_purchased, total_cost):
    print("\t" + "─" * 55)
    total_amount, change = total_cost, 0
    for item in items_purchased:
        item_name, price_per_day, days = item
        item_total = price_per_day * days
        print("\t{:<15} {:>10} days {:>12} Php{:>7.2f}".format(item_name, days, " ", item_total))
    print("\t" + "─" * 55)
    print("\t{:<43}  Php{:>7.2f}".format("Total", total_amount))
    print("\t" + "─" * 55)

    while True:
        try:
            payment_amount = float(input("\tEnter payment amount: "))
            if payment_amount < total_amount:
                print("\tPayment amount is less than the total amount. Please try again.")
                continue
            change = payment_amount - total_amount
            print("\n\t" + "─" * 55)
            print("\tPayment accepted. Your change is Php{:.2f}".format(change))
            print("\tReceipt Generated")
            break
        except ValueError:
            print("\tInvalid input. Please enter a valid amount.")

    print("\t" + "─" * 55)  # Separator line
    generate_receipt(items_purchased, total_amount, payment_amount, change, "s")
    ask_for_another_transaction()


def generate_receipt(items_purchased, total_amount, payment_amount, change, type_t, days=0):
    current_datetime = datetime.datetime.now().strftime(DATE_FORMAT)
    receipt_template = f"""
    --------------------------------------------------------
                            RECEIPT
    --------------------------------------------------------
    BuldMaster
    123 Street Mapua Davao
    {current_datetime} """

    if type_t == "p":
        receipt_template += """
    --------------------------------------------------------
    Item ID     Name               Quantity    Subtotal
    --------------------------------------------------------"""
        for item in items_purchased:
            material, quantity, subtotal = item
            receipt_template += "\n    {:<10} {:<20} {:<10} Php{:>7.2f}".format(material.id, material.name, quantity,
                                                                                subtotal)
    else:
        receipt_template += """     
    --------------------------------------------------------
    Name      Days                          price   Subtotal
    --------------------------------------------------------"""
        for item in items_purchased:
            receipt_template += "\n    {:<20} {:<10} Php{:>7.2f} Php{:7.2f}".format(item[0], days, item[1], item[1]*days)

    receipt_template += f"""
    --------------------------------------------------------
    Total                                      Php{total_amount:>7.2f}
    Payment                                    Php{payment_amount:>7.2f}
    Change                                     Php{change:>7.2f}
    --------------------------------------------------------"""

    # print(receipt_template)
    with open("Receipt.txt", 'w') as file:
        file.write(receipt_template)


def confirm_cancellation():
    while True:
        choice = input("\tAre you sure you want to cancel your order? (y/n) ").strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("\tInvalid input. Please enter 'y' for yes or 'n' for no.")


def ask_for_another_transaction():
    while True:
        choice = input("\tMake another transaction? (y/n): ").lower()
        if choice == "y":
            print_start_page()
            break
        elif choice == "n":
            bye_page()
            break
        else:
            print("\tInvalid input. Please enter 'y' or 'n'.")


def bye_page():
    print("\n\tThank you for shopping. Bye!")


print_title()
print_start_page()
