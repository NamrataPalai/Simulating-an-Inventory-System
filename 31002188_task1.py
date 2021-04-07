"""Simulation of the stocking level of Cantilever Umbrella, inside an inventory management system in an Australian firm"""

"""Task 1 gives the end stock and revenue after one year with variation in the daily distribution and RRP of the product through
 peak season,normal season(end of peak season),financial year start & global financial crisis that occurs every 9 years & sustains for 
 2 following years. Defective item stock and RRP also fluctuates every month and contributes to calculation of end stock & revenue."""

"""Function reads data from file AU_INV_START.txt & stores it in dictionary input_dict"""
def read_data():
    input_file = open("AU_INV_START.txt","r")
    input_dict = {}
    input_values = input_file.read().split('\n')
    input_dict['start_year'] = int(input_values[0])
    input_dict['start_stock'] = int(input_values[1])
    input_dict['start_revenue'] = float(input_values[2])
    input_file.close()
    return (input_dict)

"""Function writes end year, end stock and end revenue for one simulation year into AU_INV_END.txt"""
def write_data(output_dict):
    output_file = open("AU_INV_END.txt","w+")
    
    output_file.write(str(output_dict['end_year'])+"\n")
    output_file.write(str(output_dict['end_stock'])+"\n")
    output_file.write(str(output_dict['end_revenue']))

    output_file.close()
    return ()

"""Function updates the stock by removing defective items & calculates revenue accordingly while maintaining the stock value more than 400"""
def cal_everyday_stock_revenue(Def_Item, RRP_Def_Item, Quantity, RRP, Stock, Revenue):

    Stock = Stock - Quantity # distribution quantity is negated from available supply to distributors on daily basis

    # For defective items in any given month more than distribution quantity
    if (Def_Item > Quantity):
        Def_Item = round(Def_Item - Quantity)
        Revenue = round(Revenue + RRP_Def_Item * Quantity,2)

    # For defective items in any given month less than distribution quantity
    elif (Def_Item < Quantity and Def_Item != 0):
        Remaining = round(Quantity - Def_Item)
        Revenue = round(Revenue + (RRP_Def_Item * Def_Item) + (RRP * Remaining),2)
        #when no defective item is left to be distributed
        Def_Item = 0

    # For no defective items in any given month
    elif (Def_Item == 0):
        Revenue = round(Revenue + (RRP * Quantity),2)

    #Restock when the available supply is negated to 400 or below 400
    if (Stock <= 400):
        Stock = Stock + 600

    return (Stock,Revenue,Def_Item)

"""Recursive Function calculates the daily distribution and retail recommended price(RRP) from initial year to the input year"""
def cal_quantity_RRP(in_Year, Quantity, RRP, start_Year, count_Years):

#Global Financial Crisis occurs every 9 years & sustains for 2 more years

    # check if 9th year, calculate Quantity & RRP
    if (count_Years == 9):
        Quantity = round(Quantity - (Quantity * 20/100))
        RRP = round(RRP + (RRP * 10/100), 2)
    # check if (9+1)th year, calculate Quantity & RRP
    elif (count_Years == 10):
        Quantity = round(Quantity - (Quantity * 10/100))
        RRP = round(RRP + (RRP * 5/100), 2)
    # check if (9+2)th year, calculate Quantity & RRP
    elif (count_Years == 11):
        Quantity = round(Quantity - (Quantity * 5/100))
        RRP = round(RRP + (RRP * 3/100), 2)
        count_Years = 0


    # Calculate Quantity & RRP after peak season is over
    Quantity = round(Quantity * 100/135)
    RRP = round(RRP * 100/120, 2)
    
    # Calculate Quantity & RRP when financial year begins
    Quantity = round(Quantity + (Quantity * 10/100))
    RRP = round(RRP + (RRP * 5/100), 2)

    # Calculate Quantity & RRP when Peak Season starts
    Quantity = round(Quantity + (Quantity * 35/100))
    RRP = round(RRP + (RRP * 20/100), 2)

    # Calculate Quantity, RRP, count_Years for all years until initial year is equal to start(input) year
    if (in_Year == start_Year):
        return (Quantity, RRP, count_Years)
    else:
        return (cal_quantity_RRP(in_Year+1,Quantity,RRP,start_Year,count_Years+1))

"""Function to calculate quantity of defective item & its RRP for any given month """
def cal_DI_RRPDI(Quantity,RRP,days):
    DI = round(Quantity*days * 5/100)
    RRPDI = round(RRP*80/100,2)
    return (DI,RRPDI)

"""Function to check iF any given year is a leap year"""
def leap_year(year):
    # Finding if the Next Year is Leap Year or not
    if (year % 400 == 0):
        return 29
    elif (year % 100 == 0):
        return 28
    elif (year % 4 == 0):
        return 29
    else:
        return 28

"""Function calculates the end stock and revenue for one simulation year"""
def cal_stock_revenue(input_dict):
    ini_Quantity = 36
    ini_Year = 2000
    ini_RRP = 705
    year_Count = 0
    Revenue = 0
    Stock = input_dict['start_stock']
    next_Year = input_dict['start_year'] + 1

    # Dictionary initialised to store end stock and revenue
    output_dict = {}

    # List of all the days a month comprises of in a given year
    months = [31,leap_year(next_Year),31,30,31,30,31,31,30,31,30,31]

    # Calculate Quantity & RRP for end of the start(input) year right from the Initial year(2000)
    ini_Quantity,ini_RRP,year_Count = cal_quantity_RRP(ini_Year,ini_Quantity,ini_RRP,input_dict['start_year'],year_Count)


    # Finding the Defetive Items(DI) and Defective Items RRP(RRPDI) for end of the start(input year)
    RRPDI = round((4/5*ini_RRP),2)
    DI = round((31/20)*ini_Quantity)


    # Calculating crisis situation for next Year
    # check if next year is 9th year
    if (year_Count == 8):
        ini_Quantity = round(ini_Quantity - ini_Quantity*20/100)
        ini_RRP = round(ini_RRP + ini_RRP*10/100,2)

    # Check if next year is (9+1)th year
    elif (year_Count == 9):
        ini_Quantity = round(ini_Quantity - ini_Quantity*10/100)
        ini_RRP = round(ini_RRP + ini_RRP*5/100,2)

    # Check if next year is (9+2)th year
    elif (year_Count == 10):
        ini_Quantity = round(ini_Quantity - ini_Quantity*5/100)
        ini_RRP = round(ini_RRP + ini_RRP*3/100,2)

    # Calculating the Stock and Revenue in each month in a year
    for index,month in enumerate(months):

        # Calculation for each each day in a given month
        for i in range(month):

            # Function call to calculate
            Stock,Revenue,DI = cal_everyday_stock_revenue(DI,RRPDI,ini_Quantity,ini_RRP,Stock,Revenue)
            
        # Function call to calculate defective item quantity & its RRP for given month
        DI,RRPDI = cal_DI_RRPDI(ini_Quantity,ini_RRP,month)

        #Calculate the daily distribution quantity and RRP for next month if next month is a peak season start, peak season end, financial year start respectively

        # February is the end of peak season, from March normal season commences
        if(index == 1):
            ini_Quantity = round(ini_Quantity * 100/135)
            ini_RRP = round(ini_RRP *100/120,2)

        # June is the end of normal season, from July financial commences
        elif (index == 5):
            ini_Quantity = round(ini_Quantity + ini_Quantity*10/100)
            ini_RRP = round(ini_RRP + (ini_RRP*5/100),2)
        # from November peak season commences
        elif (index == 9):
            ini_Quantity = round(ini_Quantity + ini_Quantity*35/100)
            ini_RRP = round(ini_RRP + (ini_RRP*20/100),2)
    
    output_dict['end_year'] = next_Year
    output_dict['end_stock'] = Stock
    output_dict['end_revenue'] = round(Revenue,2)
    return output_dict

#function call to read input year, stock & revenue & save into input dictionary
input_dict = read_data()

#function called & calculated end stock,revenue is saved in output dictionary
output_dict = cal_stock_revenue(input_dict)

#function call to write end stock & revenue into output file
write_data(output_dict)