from Items import Material, MaterialList
from colorama import Fore, Style
import datetime

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

material_list = MaterialList()
material_list.read_materials()
all_materials = material_list.get_all_materials()


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
    print("\tSelect an option: \n\t[1] Browse Products [2] Browse Services [3] Exit")

    while True:
        choice = input("\tPlease enter you choice: ")
        if choice == '1':
            browse_items()
            break
        elif choice == '2':
            print("\tChoice 2")
            break
        elif choice == '3':
            bye_page()
            break
        else:
            print("\tinvalid choice")


def browse_items():
    print("\t" + "─" * 55)  # Separator line
    print("\t" + Fore.BLUE + "{:<3}".format("") + Style.RESET_ALL + " " +
          Fore.BLUE + "{:<25}".format("Name") + Style.RESET_ALL + " " + Fore.BLUE +
          "{:<10}".format("Price") + Style.RESET_ALL + " " + Fore.BLUE + "{:<10}".format("Sold per") + Style.RESET_ALL)
    print("\t" + "─" * 55)  # Separator line
    for material in all_materials.values():
        print("\t" + Fore.CYAN + "{:<3}".format(material.id) + Style.RESET_ALL +
              " {:<25} {:<10} {:<10}".format(material.name, material.price, material.measurement))
    print("\t" + "─" * 55)
    browse_items_input()


def browse_items_input():
    items_purchased = []
    while True:
        choice = input("\n\tEnter Item ID [Enter -1 to go back]: ")
        if choice == "-1":
            print_start_page()
            break
        elif choice not in all_materials:
            print("\tInvalid Item ID. Please try again.")
            continue
        else:
            quantity = int(input("\tEnter quantity: "))
            if quantity <= 0:
                print("\tInvalid quantity. Please enter a positive integer.")
                continue
            else:
                selected_material = all_materials[choice]
                sub_total = selected_material.price * quantity
                print("\tPurchased {} {} for Php{}.".format(quantity, selected_material.name, sub_total))
                items_purchased.append([selected_material, quantity, sub_total])

            while True:
                more_items = input("\tBuy more items? (y/n): ").lower()
                if more_items not in ('y', 'n'):
                    print("\tInvalid input. Please enter 'y' or 'n'.")
                    continue
                else:
                    break

            if more_items == 'n':
                payment_page(items_purchased)
                break

def payment_page(items_purchased):
    print("\t" + "─" * 55)
    total_amount = 0
    for item in items_purchased:
        material, quantity, subtotal = item
        total_amount += subtotal
        print("\t{:<10} {:<20} {:<10} Php{:>7.2f}".format(material.id, material.name, quantity, subtotal))
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
            print("\tPayment accepted. Your change is Php{:.2f}".format(change))
            break
        except ValueError:
            print("\tInvalid input. Please enter a valid amount.")

    generate_receipt(items_purchased, total_amount, payment_amount, change)
    ask_for_another_transaction()


def generate_receipt(items_purchased, total_amount, payment_amount, change):
    current_datetime = datetime.datetime.now().strftime(DATE_FORMAT)
    receipt_template = f"""
    --------------------------------------------------------
                            RECEIPT
    --------------------------------------------------------
    BuldMaster
    123 Street Mapua Davao
    {current_datetime}
    --------------------------------------------------------
    Item ID     Name               Quantity    Subtotal
    --------------------------------------------------------"""
    for item in items_purchased:
        material, quantity, subtotal = item
        receipt_template += "\n    {:<10} {:<20} {:<10} Php{:>7.2f}".format(material.id, material.name, quantity, subtotal)

    receipt_template += f"""
    --------------------------------------------------------
    Total                                      Php{total_amount:>7.2f}
    Payment                                    Php{payment_amount:>7.2f}
    Change                                     Php{change:>7.2f}
    --------------------------------------------------------"""

    print(receipt_template)
    with open("Receipt.txt", 'w') as file:
        file.write(receipt_template)


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
