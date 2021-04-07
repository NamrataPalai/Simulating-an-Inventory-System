"""Simulation of the stocking level of Cantilever Umbrella, inside an inventory management system in an Australian firm"""

"""Task 2 gives the end stock and revenue for a given period with variation in the daily distribution and RRP of the product through
 peak season,normal season(end of peak season),financial year start & global financial crisis that occurs every 9 years & sustains for 
 2 following years. Defective item stock and RRP also fluctuates every month and contributes to calculation of end stock & revenue.
 Note: Herein the period has been defaulted to 3 years. """

#last modified: 3rd may

"""Function reads data from file AU_INV_START.txt & stores it in dictionary input_dict"""
def read_data():
    input_file = open("AU_INV_START.txt","r")
    input_dict = {}
    input_values = input_file.read().split('\n')
    input_dict['start_year'] = input_values[0]
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

    # distribution quantity is negated from available supply to distributors on daily basis
    Stock = Stock - Quantity

    # For defective items in any given month more than distribution quantity
    if (Def_Item > Quantity):
        Def_Item = round(Def_Item - Quantity)
        Revenue = round(Revenue + RRP_Def_Item * Quantity,2)

    # For defective items in any given month less than distribution quantity
    elif (Def_Item < Quantity and Def_Item != 0):
        Remaining = round(Quantity - Def_Item)
        Revenue = round(Revenue + (RRP_Def_Item * Def_Item) + (RRP * Remaining),2)
        # when no defective item is left to be distributed
        Def_Item = 0

    # For no defective items in any given month
    elif (Def_Item == 0):
        Revenue = round(Revenue + (RRP * Quantity),2)

    # Restock when the available supply is negated to 400 or below 400
    if (Stock <= 400):
        Stock = Stock + 600

    return (Stock,Revenue,Def_Item)

"""Recursive Function calculates the daily distribution and retail recommended price(RRP) from initial year to the input year"""
def cal_quantity_RRP(in_Year, Quantity, RRP, start_Year, count_Years, CRF):

    # Crisis Recur Frequency(CRF) is defaulted to 9 for global financial crisis

    # check if year in CRF, calculate Quantity & RRP
    if (count_Years == CRF):
        Quantity = round(Quantity - (Quantity * 20/100))
        RRP = round(RRP + (RRP * 10/100), 2)

    # check if year in CRF+1, calculate Quantity & RRP
    elif (count_Years == CRF+1):
        Quantity = round(Quantity - (Quantity * 10/100))
        RRP = round(RRP + (RRP * 5/100), 2)

    # check if year in CRF+2, calculate Quantity & RRP
    elif (count_Years == CRF+2):
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

    # Calculate Quantity, RRP, count_Years for all years until your initial year is equal to the previous year of the start(input) year
    if (in_Year == start_Year - 1):
        return (Quantity, RRP, count_Years)
    else:
        return (cal_quantity_RRP(in_Year+1,Quantity,RRP,start_Year,count_Years+1,CRF))

"""Function to calculate quantity of defective item & its RRP for any given month """
def cal_DI_RRPDI(Quantity,RRP,days,PER_DEF):
    DI = round(Quantity*days * PER_DEF/100)
    RRPDI = round(RRP*80/100,2)
    return (DI,RRPDI)

"""Function to check id any given year is a leap year"""""
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

"""Function to calculate Quantity of distribution & RRP for start month of the given input date"""
def cal_extra_month(quantiy,RRP,start_month):

    # calculate for normal season commencement
    if start_month > 2:
        quantiy = round(quantiy * 100/135)
        RRP = round(RRP * 100/120, 2)
    # calculate for financial year start
    if start_month > 6:
        quantiy = round(quantiy + quantiy * 10/100)
        RRP = round(RRP + RRP * 5/100, 2)

    # calculate for peak season commencement
    if start_month > 10:
        quantiy = round(quantiy + quantiy * 35/100)
        RRP = round(RRP + RRP * 20/100, 2)
    return (quantiy, RRP)

"""Function calculates the end stock and revenue for the given value of NO_YEAR_SIM which is defaulted to 3"""
def cal_stock_revenue(input_dict):
    PER_DEF = 5
    NO_YEAR_SIM = 3
    CRISIS_RECUR_FREQUENCY = 9
    ini_Quantity = 36
    ini_Year = 2000
    ini_RRP = 705
    year_Count = 0
    Revenue = 0
    Stock = input_dict['start_stock']

    #start year in input dictionary is split into 3 parts

    # first 4 places alligned to year
    start_Year = int(input_dict['start_year'][:4])

    # 2 places after year are alligned to month
    start_Month = int(input_dict['start_year'][4:6])

    # 2 places after month are alligned to day
    start_Day = int(input_dict['start_year'][6:])
    next_Year = start_Year

    # Dictionary initialised to store end stock and revenue
    output_dict = {}

    # Calculate Quantity & RRP for end of the start(input) year right from the Initial year(2000)
    if (start_Year > ini_Year):
        ini_Quantity,ini_RRP,year_Count = cal_quantity_RRP(ini_Year,ini_Quantity,ini_RRP,start_Year,year_Count,CRISIS_RECUR_FREQUENCY)


    # Calculating crisis situation for next Year

    # check if next year is in CRF
    if (year_Count == CRISIS_RECUR_FREQUENCY - 1):
        ini_Quantity = round(ini_Quantity - ini_Quantity*20/100)
        ini_RRP = round(ini_RRP + ini_RRP*10/100,2)

    # check if next year in CRF+1, calculate Quantity & RRP
    elif (year_Count == CRISIS_RECUR_FREQUENCY):
        ini_Quantity = round(ini_Quantity - ini_Quantity*10/100)
        ini_RRP = round(ini_RRP + ini_RRP*5/100,2)

    # check if next year in CRF+2, calculate Quantity & RRP
    elif (year_Count == CRISIS_RECUR_FREQUENCY + 1):
        ini_Quantity = round(ini_Quantity - ini_Quantity*5/100)
        ini_RRP = round(ini_RRP + ini_RRP*3/100,2)
        year_Count = 0
    year_Count += 1

    # Calculating extra months
    ini_Quantity, ini_RRP = cal_extra_month(ini_Quantity, ini_RRP, start_Month)

    # List of all the days a month comprises of in a given year
    months = [31, leap_year(next_Year), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Finding the Defective Items(DI) and Defective Items RRP(RRPDI) for month before the start month mentioned in input
    RRPDI = round((4/5*ini_RRP),2)
    DI = round((months[(start_Month - 2 + 12)%12]/20)*ini_Quantity)

    #traversing through each simulation cycle in a given NO_YEAR_SIM
    for x in range(NO_YEAR_SIM):

        #this will be satisfied for the first simulation cycle for any specified input to generate lists as per the shift
        x += 1
        months = [31,leap_year(next_Year),31,30,31,30,31,31,30,31,30,31]
        next_Year = next_Year + 1
        shift = start_Month - 1

       # this is to generate 3 lists for 3 simulation years wherein it arranges the months in the list to begin with desired month fed in the iput
        months = months[shift:] + months[:shift]


        #this is the for the simulation cycles post first simulation cycles
        if x != 1:

            #Calculating crisis situation for next Year

            # check if year iN CRF, calculate quantity & RRP
            if (year_Count == CRISIS_RECUR_FREQUENCY):
                ini_Quantity = round(ini_Quantity - ini_Quantity*20/100)
                ini_RRP = round(ini_RRP + ini_RRP*10/100,2)

            # check if year is (CRF+1)th year, calculate quantity & RRP
            elif (year_Count == CRISIS_RECUR_FREQUENCY + 1):
                ini_Quantity = round(ini_Quantity - ini_Quantity*10/100)
                ini_RRP = round(ini_RRP + ini_RRP*5/100,2)

            # check if year is (CRF+2)th year, calculate quantity & RRP
            elif (year_Count == CRISIS_RECUR_FREQUENCY + 2):
                ini_Quantity = round(ini_Quantity - ini_Quantity*5/100)
                ini_RRP = round(ini_RRP + ini_RRP*3/100,2)
                year_Count = 0
            year_Count += 1
        
        # Calculating the Stock and Revenue in each month
        for index, month in enumerate(months):
            #this is to find the number of days of the month specified in the input to be taken into consideration for further calculation
            if x == 1 and index == 0:
                month = month - start_Day + 1 #since date is specified , taking the days post the start day into consideration for calculation

            #calculate the quantity distribution & revenue on daily basis on th above found days of the month specified in input
            for i in range(month):
                #print (Stock, "  " , Revenue, "  ", DI)
                Stock,Revenue,DI = cal_everyday_stock_revenue(DI,RRPDI,ini_Quantity,ini_RRP,Stock,Revenue)

            #Calculate defective item quantity & RRP
            DI,RRPDI = cal_DI_RRPDI(ini_Quantity,ini_RRP,month,PER_DEF)
            #print (month, " : Stock : ", Stock, " Revenue : ", round(Revenue,2), " DI : ", DI, " RRPDI : ", RRPDI)

            #this is to specify the months with desired season commencement as the lists have been altered for every simulation year
            change = 12 - shift

            # indexing the altered list for calculating quantity & RRP for the months after peak season ends
            if (index == (1 + change)%12):
                ini_Quantity = round(ini_Quantity*100/135)
                ini_RRP = round(ini_RRP*100/120,2)

            # indexing the altered list for calculating quantity & RRP for the months post financial year commencement
            elif (index == (5 + change)%12):
                ini_Quantity = round(ini_Quantity + ini_Quantity*10/100)
                ini_RRP = round(ini_RRP + (ini_RRP*5/100),2)

            # indexing the altered list for calculating quantity & RRP for the months post peak season commencement
            elif (index == (9 + change)%12):
                ini_Quantity = round(ini_Quantity + ini_Quantity*35/100)
                ini_RRP = round(ini_RRP + (ini_RRP*20/100),2)

            #after reaching the last cycle of the simulation period, and last month of the simulation year
            if x == NO_YEAR_SIM and index == 11:

                #remaining days
                month = start_Day - 1

                #quantity & RRP are calculated for the remaining days which is from the last day of the month indexed 11 to the given date
                for i in range(month):
                    Stock,Revenue,DI = cal_everyday_stock_revenue(DI,RRPDI,ini_Quantity,ini_RRP,Stock,Revenue)
                    #print (month, "  ",Stock, "  " , Revenue, "  ", DI)

    
    #to concatenate month & date along with the year in output dictionary
    output_dict['end_year'] = str(next_Year) + '%02d%02d' %(start_Month, start_Day)
    output_dict['end_stock'] = Stock
    output_dict['end_revenue'] = round(Revenue,2)
    return output_dict

#function call to read input year, stock & revenue & save into input dictionary
input_dict = read_data()

#function called & calculated end stock,revenue is saved in output dictionary
output_dict = cal_stock_revenue(input_dict)

#function call to write end stock & revenue into output file
write_data(output_dict)