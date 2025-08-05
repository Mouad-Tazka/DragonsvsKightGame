Ming_Dynasty = {'shrimp egg roll': 1.95, 'bbq wings': 7.95,
                'hunan pork': 10.25,
                'sweet and sour chicken': 12.95,
                'chicken with broccoli': 12.95}

Bodos = {'bagel': 1.00, 'deluxe bagel': 2.00,
         'coffee': 1.50, 'water': 1.00}

all_cville_resturants = {'Ming Dynasty': Ming_Dynasty,
                         'Bodos': Bodos}

def add_menu (menu, item_name, item_price):
    menu[item_name] = item_price

def calculate_order (dict, list, tip = 0.18):
    raw_cost = 0
    order_avaliable = True
    for item in list:
        if item in dict:
            raw_cost += dict[item]
        else:
            order_avaliable = False
    if order_avaliable == True:
        total_price = raw_cost + (raw_cost * tip) + (raw_cost * 0.06)
        return round(total_price, 2)
    if order_avaliable == False:
        print("Sorry, you cannot order that item")

def print_the_menu(dict):
    for item in dict:
        menu_print = print (item, '-', dict.get(item))
    return menu_print
print (print_the_menu (Ming_Dynasty))

def place_mega_order (mega_menu, order):
    raw_price = 0
    for rest_ord in order:
        order_list = order[rest_ord]
        menu = mega_menu[rest_ord]
        for item in order_list:
            total_price += menu[item]
    total_price = raw_price + (raw_price*0.18) + (raw_price*0.06)
    return round(total_price, 2)

