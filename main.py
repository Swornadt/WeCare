from operations import selectedBuyingMode, selectedRestockingMode, displayInventory

def mainMenu():
    """ Always returns to this landing menu where user can choose their mode. """
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
    except(Exception):
        print("(!) *** Unknown error occured *** (!)")
        print("="*47)
        mainMenu()
        
#driver code
mainMenu()
