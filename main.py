import datetime

#initializing data collection
database = {}
detail_titles = ("name","brand","quantity","cost_price","origin")
items_list = []
#reading from the stockpile file
last_id = 1 #to track latest id
fp = open("stockpile.txt","r")
line = fp.readline()
while line:
    #logic to split the different fields
    details = line.replace("\n","").split(",")
    idx = 0
    product_dict = {}
    #adding values into inner dictionary
    for title in detail_titles:
        if title in ("quantity","cost_price"): #typecast for integer operations
            product_dict[title] = int(details[idx])
        else:
            product_dict[title] =  details[idx]
        idx += 1
    #using id for indexing, then adding inner dictionary to the main dictionary through iterations
    database[last_id] = product_dict
    last_id += 1
    line = fp.readline()
fp.close()

#basic utility functions   
def setInventory(id, amount):
    """ sets/mutates the dictionary (NOT FILE!) some passed value
        for inventory management """
    total_stock = database[id]["quantity"] #fetching quantity of items for a specific product
    if total_stock >= amount:
        database[id]["quantity"]-=amount
        updateInventory()
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

def updateInventory():
    fp = open("stockpile.txt","w")
    for item in database.values():
        line = item["name"]+","+item["brand"]+", "+str(int(item["quantity"]))+", "+str(int(item["cost_price"]))+","+item["origin"]+"\n"
        fp.write(line)
    fp.close()
    
#helper function
def extraPolicy(num):
    """ policy check; returns number of extra after taking in the number of bought """
    #division rule: divisor*quotient+remainder=dividend; rearranging to find the quotient
    return (num - (num%3))/3   

''' Selection Functions '''
#UI for customer buying looping
def selectedBuyingMode():
    """ selectedBuyingMode() -> displayInventory() -> performBuying() -> createCustomerReceipt() -> readReceipt() """
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
                performBuying(name,phone)
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
def performBuying(name,phone):
    """ buying logic- takes id and amount as user input and calls next functions as previously defined """
    try:
        item_id = int(input("Enter the ID of the item to buy: ")) #TODO: input validation! (non exist, negative number)
        item_amount = int(input("Enter the amount of item to buy: "))

        if (item_amount <= 0):
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
        actual_bought = deducted_amount-extraPolicy(deducted_amount)
        bonus_amount = extraPolicy(actual_bought) #calculates extra based on how much is actually bought after accounting for higher than stock values
        createCart(item_id, actual_bought, bonus_amount)

    except(KeyError):
        print("(!) *** ID not found in database! *** (!)")
    except(ValueError):
        print("(!) *** Please enter valid inputs. *** (!)")
    except(Exception):
        print("(!) *** Unknown exception occured *** (!)")
        
    

#Creating List of Items Bought:
def createCart(item_id, item_amount, bonus_amount):
    cart_dict = {} #temporary dictionary that stores the bought items before passing to create receipt    
    cart_titles = ("id","amount_bought","bonus_amount")
    for item in database.items():
        if (item_id == item[0]):
            for title in cart_titles:
                if (title == "id"):
                    cart_dict[title] = item[0]
                elif (title == "amount_bought"):
                    cart_dict[title] = item_amount
                elif (title == "bonus_amount"):
                    cart_dict[title] = bonus_amount
            items_list.append(cart_dict)

''' Perform Functions '''
def performRestocking():
    """ resstocking logic- takes id and amount of items as user input and calls next functions as previously defined """
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
        
    
    
#Creating a final receipt
def createCustomerReceipt(items_list, name, phone):

    #getting a time for this transaction (to avoid file duplication
    #getting current date
    now = datetime.datetime.now()
    day = str(now.day)
    month = str(now.month)
    year = str(now.year)
    minute = str(now.minute)
    sec = str(now.second)

    second_name = str(phone)+"-"+minute+sec #creating a string to pass with name while creating file name
    
    fp = open(name+str(second_name)+".txt","w")
    left_indent = "\t\t|"
    
    #invoice header
    fp.write(left_indent+"="*100+"|\n")
    tab_spacing="\t\t\t\t"
    fp.write(left_indent+tab_spacing+"\t      WeCare Store"+" "*43+"|\n")
    fp.write(left_indent+tab_spacing+"\t     WeCare Pvt. Ltd."+" "*40+"|\n")
    fp.write(left_indent+tab_spacing+"\t Address: Baneshwor, Kathmandu"+" "*31+"|\n")
    fp.write(left_indent+"="*100+"|\n")
    
    invoice_num = 1 #TODO: dynamic naming

    #field inputs
    invoice_date = day+"-"+month+"-"+year
    customer_name = name
    customer_phone = str(phone)

    #tracking constants
    item_no = 0
    total_amount = 0
    no_of_bonus_items = 0

    #indent calculation for the border of customer phone row
    phone_length = len(customer_phone)
    phone_spacing = " "*(100-16-phone_length)+"|"
    
    fp.write(left_indent+"Invoice number: "+str(invoice_num)+"\t\t\t\t\t\t\t      Date Issued: "+invoice_date+"  |\n")
    fp.write(left_indent+"Customer Phone: "+customer_phone+phone_spacing+"\n")
    
    #header columns
    fp.write(left_indent+"-"*100+"|\n")
    fp.write(left_indent+"Item ID\t"+"Product Name\t\t"+"Brand\t\t"+"Quantity\t"+"Rate\t\t"+"Gross\t     |\n")
    fp.write(left_indent+"-"*100+"|\n")
    
    #main content
    for item in items_list:
        #required fields
        item_no += 1

        #getting the details from cart
        item_id = item["id"]
        item_amount = item["amount_bought"]
        bonus_amount = item["bonus_amount"]

        #fetching other details using primary key
        item_name = database[item_id]["name"]
        item_brand = database[item_id]["brand"]
        item_rate = database[item_id]["cost_price"]

        #setting other costants
        selling_price = item_rate*2 #must be double according to our question
        item_gross = selling_price * item_amount
        total_amount += item_gross
        no_of_bonus_items += bonus_amount
        
        #spacing fix:
        concat_of_amounts = str(item_amount)+str(bonus_amount)
        tab_spacing = "\t\t" if len(concat_of_amounts)+1 < 8 else "\t" #to fix formatting issues
        tab_spacing2 = "\t\t" if len(str(selling_price)) < 5 else "\t"
        if len(str(item_gross)) < 8:
            tab_spacing3 = "\t"
        else:
            tab_spacing3 = ""
            
        #writing the actual line:
        full_line = str(item_no)+"\t\t"+item_name+"\t\t"+item_brand+"\t"+str(item_amount)+"+"+str(bonus_amount)+tab_spacing+str(selling_price)+tab_spacing2+str(item_gross)
        
        #write operation for the line
        fp.write(left_indent+full_line+tab_spacing3+"     |\n")
        
    fp.write(left_indent+"-"*100+"|")
    fp.write("\n")
    if len(str(total_amount)) < 7:
        tab_spacing = "\t"
    elif len(str(total_amount)) < 8:
        tab_spacing = "\t"
    else:
        tab_spacing = ""
    fp.write(left_indent+"You have received: "+str(int(no_of_bonus_items))+" free items!"+"\t\t\t\t\t  Total Amount: "+str(total_amount)+tab_spacing+"     |")
    fp.write("\n")
    fp.write(left_indent+"="*100+"|")
    fp.close()
    readReceipt(name, second_name)

#UI for purchasing from manufacture looping
def selectedRestockingMode():
    """ selectedRestockingMode() -> performRestocking() -> createRestockReceipt -> readRestockReceipt() """
    displayInventory()
    flow = "Y"
    while True:
        if (flow.upper() == "Y"):
            performRestocking()
        elif (flow.upper() == "N"):
            print("Thank you!")
            createRestockReceipt(items_list)
            items_list.clear();
            break;
        else:
            print("Invalid input!")
        flow = input("Would you like to continue restocking (Y/N)? ")

    
#Creating Restocking Receipt:
def createRestockReceipt(items_list):

    #initializing the date and time
    now = datetime.datetime.now()
    day = now.day
    month = now.month
    year = now.year
    hr = now.hour
    minute = now.minute
    sec = now.second
    
    receipt_date = str(year)+str(month)+str(day)
    receipt_time = str(hr)+str(minute)+str(sec)
    
    fp = open(receipt_date+receipt_time+".txt","w")
    left_indent = "\t\t|"
    #invoice header
    fp.write(left_indent+"="*100+"|\n")
    tab_spacing="\t\t\t\t"
    fp.write(left_indent+tab_spacing+"\t      Hrishav Suppliers"+" "*38+"|\n")
    fp.write(left_indent+tab_spacing+"\t     Unilever Pvt. Ltd."+" "*38+"|\n")
    fp.write(left_indent+tab_spacing+"\t Address: Baneshwor, Kathmandu"+" "*31+"|\n")
    fp.write(left_indent+"="*100+"|\n")
    
    invoice_num = 1 #TODO: dynamic naming

    #getting current date
    now = datetime.datetime.now()
    day = str(now.day)
    month = str(now.month)
    year = str(now.year)

    #field inputs
    invoice_date = day+"-"+month+"-"+year
    customer_name = "WeCare Pvt. Ltd."  
    customer_phone = "9840259002" 
    item_no = 0
    total_amount = 0

    #indent calculation for the border of customer phone row
    phone_length = len(customer_phone)
    phone_spacing = " "*(100-16-phone_length)+"|"
    
    fp.write(left_indent+"Invoice number: "+str(invoice_num)+"\t\t\t\t\t\t\t      Date Issued: "+invoice_date+"  |\n")
    fp.write(left_indent+"Customer Phone: "+customer_phone+phone_spacing+"\n")
    
    #header columns
    fp.write(left_indent+"-"*100+"|\n")
    fp.write(left_indent+"Item ID\t"+"Product Name\t\t"+"Brand\t\t"+"Quantity\t"+"Rate\t\t"+"Gross\t     |\n")
    fp.write(left_indent+"-"*100+"|\n")
    
    #main content
    for item in items_list:
        #required fields
        item_no += 1

        #extracts id of the item in cart
        item_id = item["id"]
        
        #fetches other details of the cart from the database using the primary key
        item_name = database[item_id]["name"] 
        item_brand = database[item_id]["brand"]
        item_rate = database[item_id]["cost_price"]
        
        #extract other details from cart
        item_amount = item["amount_bought"]
        bonus_amount = item["bonus_amount"]

        #setting up the constants
        selling_price = item_rate #cost will not be double here
        item_gross = selling_price * item_amount
        total_amount += item_gross
        
        #spacing fix:
        tab_spacing = "\t\t" if len(str(item_amount)) < 4 else "\t" #to fix formatting issues
        tab_spacing2 = "\t\t" if len(str(selling_price)) < 5 else "\t"
        tab_spacing3 = "\t\t" if len(str(item_brand)) < 9 else "\t"
        if len(str(item_gross)) < 8:
            tab_spacing4 = "\t"
        else:
            tab_spacing4 = ""
            
        #writing the actual line:
        full_line = str(item_no)+"\t\t"+item_name+"\t       "+item_brand+tab_spacing3+str(item_amount)+tab_spacing+str(selling_price)+tab_spacing2+str(item_gross)
        
        #write operation for the line
        fp.write(left_indent+full_line+tab_spacing4+"     |\n")
        
    fp.write(left_indent+"-"*100+"|")
    fp.write("\n")

    #dynamic calculating spacing required for footer part
    length_of_item_amount = len(str(total_amount))
    required_spacing1 = " "*(11-length_of_item_amount)

    length_of_vat_amount = len(str(total_amount*0.13))
    required_spacing2 = " "*(13-length_of_vat_amount)

    length_of_grand_total = len(str(total_amount+total_amount*0.13))
    required_spacing3 = " "*(13-length_of_grand_total)
    
    if len(str(total_amount+total_amount*0.13)) > 7:
        tab_spacing2 = "     "
    else:
        tab_spacing2 = "\t"

    #writing the footer lines
    fp.write(left_indent+"\t\t\t\t\t\t\t\t\t  Total Amount: "+str(float(total_amount))+required_spacing1+"|\n")
    fp.write(left_indent+"\t\t\t\t\t\t\t\t\t  VAT (13%)   : "+str(total_amount*0.13)+required_spacing2+"|\n")
    fp.write(left_indent+"\t\t\t\t\t\t\t\t\t  Grand Total : "+str(total_amount+total_amount*0.13)+required_spacing3+"|\n")
    fp.write(left_indent+"="*100+"|")
    #test: print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t**")
    fp.close()
    readReceipt(receipt_date, receipt_time)

#Reading Customer Receipt:
def readReceipt(first, second):
    """ displays whole receipt from the file using same logic as displayInventory() """
    print("\t\tRECEIPT")
    path = first+str(second)+".txt"
    fp = open(path,"r")
    line = fp.readline()
    while line:
        print(line,end="")
        line = fp.readline()
    print("\n\nReceipt created successfully!")
    fp.close()
    

'''main menu function:'''
def mainMenu():
    """ always returns to this landing menu where user can choose their mode. """
    print("Welcome to WeCare!")
    print("Health and Happiness is Our Priority")
    print("Please select your mode.\n")

    try:
        mode = int(input(" 1. Buying Products\n 2. Restocking Items\n 3. Display Inventory\n 4. Exit\n>>"))
        print("="*50)
        if (mode == 1):
            selectedBuyingMode()
            print("="*50)
            mainMenu()
        elif (mode == 2):
            selectedRestockingMode()
            print("="*50)
            mainMenu()
        elif (mode == 3):
            displayInventory()
            print("="*50)
            mainMenu()
        elif (mode == 4):
            print("See you again~")
        else:
            print("Invalid Selection.")
            mainMenu()
            
    except(ValueError):
        print("(!) *** Please select correct option. *** (!)")
        print("="*47)
        mainMenu()
    '''except(Exception):
        print("(!) *** Unknown error occured *** (!)")
        print("="*47)
        mainMenu()'''

#driver code
mainMenu()
