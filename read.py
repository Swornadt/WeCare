
#Reading data from stockpile
def readInventory():
    """
    Reads inventory from "stockpile.txt" and store in dictionary

    Each line contains single product details, and the values are extracted and
    stored in respective keys of a dictionary for each product.

    Returns:
    dict -- a master dictionary, containing a collection of dictionaries each
    having an integer as key and value being a dictionary consisting of data
    of each product.
    """
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
    return database

#Reading Customer Receipt:
def readReceipt(first, second):
    """
    Displays whole receipt of recently saved customer or restocking from a text file.

    Creates a filename by concatenation of first and second arguments, which is
    name and phone+time for customer, and date and time for restock.
    Prints the entire receipt, including headers and other data
    """
    print("\t\tRECEIPT")
    path = first+str(second)+".txt"
    fp = open(path,"r")
    line = fp.readline()
    while line:
        print(line,end="")
        line = fp.readline()
    print("\n\nReceipt created successfully!")
    fp.close()
    
