from write import createCustomerReceipt, createRestockReceipt, updateInventory
from read import readInventory

items_list = []
database = readInventory()

''' Utility Functions '''
def setInventory(id, amount):
    """
    Sets/mutates the dictionary (NOT FILE!) some passed value.

    If required amount (with bonus) is available, directly reduce quantity from
    the inventory and update it.
    If not enough, user can choose to buy the entire stock (which includes free
    items) instead or cancel the order.

    Keyword arguments:
    id -- product id in the inventory database
    amount -- quantity for purchase, including bonus amount (expected amount)

    Returns:
    int -- actual quantity purchased, which may be less than requested amount
            if the stock was less than requested.
    """
    total_stock = database[id]["quantity"] #fetching quantity of items for a specific product
    if total_stock >= amount:
        database[id]["quantity"]-=amount
        updateInventory(database)
        return amount
    else:
        print("Apologies! We do not have enough stock.")
        if (total_stock != 0):
            #Alternative for out of stock sale
            flow = input("Would you like to purchase "+str(total_stock)+" (with free) only? (Y/N)")
            if (flow.upper() == "Y"):
                return setInventory(id,total_stock) #returning actual amount bought (exclusive of bonus)
            elif (flow.upper() == "N"):
                print("Please browse our other products.")
                return 0
            else:
                print("Invalid input.")
                return setInventory(id, amount)
        else:
            print("Please browse our other products")
            return 0
    
#display the stocks
def displayInventory():
    """ Displays all the data in database in a formatted manner """
    print("\n")
    #header columns
    print("-"*134)
    print("Item ID\t\t","Product Name\t\t","Company\t\t","Quantity\t\t","Cost Per Item\t\t","Origin Country\t\t")
    print("-"*134)
    #main content
    for item in database.items():
        tab_spacing = "\t\t" if len(item[1]["name"]) < 14 else "\t" #to fix formatting issues
        print(str(item[0])+"\t\t "+item[1]["name"]+tab_spacing+item[1]["brand"]+"\t\t "+str(item[1]["quantity"])+"\t\t\t "+str(item[1]["cost_price"]*2)+"\t\t\t"+item[1]["origin"])
    print("-"*134+"\n")
    
#helper function
def extraPolicy(num):
    """
    Returns how many bonus products are expected with the requested amount bought.

    Keyword argument:
    num -- the requested amount of products (without bonus)

    Returns:
    int -- returns no. of bonus products through division rule
    """
    #division rule: divisor*quotient+remainder=dividend; rearranging to find the quotient
    return (num - (num%3))/3

#Creating List of Items Bought:
def createCart(item_id, item_amount, bonus_amount):
    """
    Creates a list of purchased items containing minimum details

    Generates dictionary containing id, amount bought and bonus amount, and
    appends to the items_list which has a scope throughout this module for each
    product.
    The list contains the details which is accessed later to generate the receipt.

    Keyword arguments:
    item_id: id of the item getting bought
    item_amount: actual amount of item (without bonus)
    bonus_amount: additional amount of item (passed separately for easier accessing later)
    """
    cart_titles = ("id","amount_bought","bonus_amount")
    for item in database.items():
        if (item_id == item[0]):
            cart_dict = {} #temporary dictionary that stores the bought items before passing to create receipt  
            for title in cart_titles:
                if (title == "id"):
                    cart_dict[title] = item[0]
                elif (title == "amount_bought"):
                    cart_dict[title] = item_amount
                elif (title == "bonus_amount"):
                    cart_dict[title] = bonus_amount
            items_list.append(cart_dict)

''' ======================================================== '''

''' Buying Functions '''
#UI for customer buying looping
def selectedBuyingMode():
    """
    Main UI for customer buying process

    This collects name and phone of user, displays current inventory, and then
    runs a loop to allow user to buy products (through performBuying() function)
    until they want to exit.
    After ending the loop, a receipt is generated and cart is cleared for next
    customer.

    Buying Logic Flow:
    selectedBuyingMode() -> displayInventory() -> performBuying()
    -> createCart() -> createCustomerReceipt() -> readReceipt()
    """
    try:
        name = input("Please enter your name: ")
        phone = int(input("Please enter your contact number: "))

        if(name.replace(" ","") == "" or str(phone).replace(" ","") == ""):
            print("(!) *** Please enter valid inputs *** (!)")
            selectedBuyingMode()
        elif(len(str(phone).replace(" ",""))<9):
            print("(!) *** Please enter valid phone number *** (!)")
            selectedBuyingMode()
            
        print("="*134)
        print("Hello, "+name+"! How can we help you today?")
        displayInventory()
        flow = "Y" #so that it runs at least once first before checking
        while True:
            if (flow.upper() == "Y"):
                performBuying()
            elif (flow.upper() == "N"):
                print("Thank you for shopping with us!\n\n")
                createCustomerReceipt(items_list, name, phone)
                items_list.clear() #clearing for next customer
                break
            else:
                print("Invalid input!")
            flow = input("Would you like to continue buying (Y/N)? ")
            print()
            
    except (ValueError):
        print("(!) *** Please enter valid inputs *** (!)")
        selectedBuyingMode()

#UI for the user to sell
def performBuying():
    """
    Performs the main processing a singular order.

    Firstly, prompt to get the ID and quantity of the item to buy & validate.
    Secondly, calculate the bonus items amount based on item_amount using 
    extraPolicy() and store as expected_bonus.
    Thirdly, validate how much can actually be bought (if ordered amount +
    bonus amount exceeds stock, offer alternative) using setInventory().
    Finally, add the product to a cart using createCart() for next step.
    """
    try:
        item_id = int(input("Enter the ID of the item to buy: "))
        item_amount = int(input("Enter the amount of item to buy: "))

        if (item_amount <= 0 or item_id <= 0):
            print("(!) *** Amount must be a positive number. *** (!)")
            return
        
        #expected amounts (no exceptions)
        expected_bonus = extraPolicy(item_amount)
        total_expect=item_amount+expected_bonus

        #trying to deduct...
        deducted_amount = setInventory(item_id, total_expect) #returning actual amount deducted from inventory after validation
        if deducted_amount == 0:
            return
        
        #defensive:
        if(deducted_amount == total_expect):
            '''
            case 1 - the amount returned is equal to what is expected.
            this is necessary for larger than stock (with bonus) expected amount.
            In this case, no issues occur so we can directly pass it.
            '''
            actual_bought = item_amount
            bonus_amount = expected_bonus
        else:
            '''
            case 2 - the user takes whole stock, and now the total
            amount (item_amount+nbonus) would exceed what is in stock.
            So, subtracting the new bonus from deducted and pass the
            new bonus.
            '''
            actual_bought = deducted_amount-extraPolicy(deducted_amount)
            bonus_amount = extraPolicy(deducted_amount) #calculates extra based on how much is actually bought after accounting for higher than stock values    
        createCart(item_id, actual_bought, bonus_amount)
    except(KeyError):
        print("(!) *** ID not found in database! *** (!)")
    except(ValueError):
        print("(!) *** Please enter valid inputs. *** (!)")
    except(Exception):
        print("(!) *** Unknown exception occured *** (!)")

''' ========================================================== '''

''' Restocking Functions '''
#UI for purchasing from manufacture looping
def selectedRestockingMode():
    """
    Main UI for ordering from vendor for restocking

    This lets user select from a vendor, displays current inventory, and then
    runs a loop to allow user to restock products (through performRestocking()
    function) until they want to exit.
    After ending the loop, a receipt is generated and cart is cleared for next
    restock/order.
    
    Restocking Logic Flow:
    selectedRestockingMode() -> displayInventory() -> performRestocking()
        -> createCart() -> createRestockReceipt() -> readReceipt()
    """

    vendors = ("Foreveryng","NepalMART","Cosibella","Rishant")
    print("Welcome to Restocking Mode.")
    
    try:
        #selection of vendor
        for idx in range(len(vendors)):
            print(str(idx+1)+". "+vendors[idx])
        choice = int(input("Please select your vendor. "))
        selected_vendor = vendors[choice-1]
        displayInventory()
        flow = "Y"
        while True:
            if (flow.upper() == "Y"):
                performRestocking()
            elif (flow.upper() == "N"):
                print("Thank you!")
                createRestockReceipt(items_list, selected_vendor)
                items_list.clear();
                break;
            else:
                print("Invalid input!")
            flow = input("Would you like to continue restocking (Y/N)? ")

    except (IndexError):
        print("(!)***Please select a valid option***(!)")
        selectedRestockingMode()
    except (ValueError):
        print("(!)***Please enter a number***(!)")
        selectedRestockingMode()
    except (Exception):
        print("(!)***Unknown error occured***(!)")
        
def performRestocking():
    """
    Performs main process of restocking a single order.

    Prompts user to input id and amount of product to restock, with validation.
    Alters the inventory by adding amount, then passes the amount to the cart
    through createCart(), putting bonus as 0 as restock has no bonus feature.
    Passing 0 is necessary as the function expects these parameters.
    """
    try:
        item_id = int(input("Enter the ID of the item to restock: "))
        item_amount = int(input("Enter the amount of item to restock: "))

        #validation
        if (item_amount <= 0):
            print("(!) *** Amount must be a positive number. *** (!)")
            return
        
        bonus_amount = 0
        setInventory(item_id, -item_amount) #-ve sign to add to stock
        createCart(item_id, item_amount, bonus_amount)
        
    except(KeyError):
        print("(!) *** ID not found in database! *** (!)")
    except(ValueError):
        print("(!) *** Please enter valid inputs. *** (!)")
    except(Exception):
        print("(!) *** Unknown exception occured *** (!)")

