from read import readInventory, readReceipt
import datetime

database = readInventory()
#Creating a final receipt
def createCustomerReceipt(items_list, name, phone):
    """
    Creates a properly formatted receipt for customer in a text file.

    Receipt includes details of customer, product details with costs and
    final price calculated, and also the number of bonus items received.
    The file name is set using name, phone number and current time for
    avoiding duplication.

    Key arguments:
    items_list -- A list containing dictionaries. Here, each element is a
                    dictionary containing id, amount_bought and bonus_amount
                    as set by createCart().
    name -- string having name of customer and used for filename and display.
    phone -- contact number of customer and used for filename and display.
    """
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

#Creating Restocking Receipt:
def createRestockReceipt(items_list, selected_vendor):
    """
    Creates a properly formatted receipt for restocking inventory in a text file.

    Receipt includes details of vendor, product details with costs and
    total price calculated alongside VAT, and the grand total price.
    The file name is set using current date and time for avoiding duplication.

    Key arguments:
    items_list -- A list containing dictionaries. Here, each element is a
                    dictionary containing id, amount_bought (quantity for restocking)
                    and bonus_amount (not used, but needed by the function)
                    as set by createCart().
    selected_vendor -- The name of vendor, which is used for displaying on receipt header.
    """
    database = readInventory()
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
    fp.write(left_indent+tab_spacing+"\t      "+selected_vendor+" Suppliers"+" "*38+"|\n")
    fp.write(left_indent+tab_spacing+"\t     "+selected_vendor+" Pvt. Ltd."+" "*38+"|\n")
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
