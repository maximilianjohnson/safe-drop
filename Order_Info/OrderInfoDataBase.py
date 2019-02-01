#Imports
import pandas
from pandas import ExcelWriter
import uuid
from datetime import datetime
#Set DataFrame
df1 = pandas.read_excel("SD_Order_info.xlsx", sheet_num = 0)
df1.set_index("OID")

#This function checks for duplicate uuid's, probably redundant
#def check_dup_id(UUID):
    #established_uuids = list(df1.loc[:, "RID"])
    #for item in established_uuids:
    #    if UUID == item:
    #        return 1
#Function uses values to add new order to excel sheet
def newOrder (S_name, B_name, I_name, Cost, Location):
    writer = ExcelWriter("SD_Order_Info.xlsx") #Excel file location
    df1 = pandas.read_excel("SD_Order_info.xlsx", sheet_num = 0)
    df1.set_index("OID")
    Order_num = (int(len(list(df1.loc[:, "OID"])))+1)
    ID = uuid.uuid4()
    date = str(datetime.now())
    #while check_dup_id(ID) == 1: #commented out due to redundancy
    #    ID = uuid.uuid4()
    df1_t = df1.T #Currently don't know how to add row, so inveresed, add column and inverse back
    df1_t[Order_num] = [Order_num, ID, S_name, B_name, I_name, Cost, Location, date, "Incomplete"]
    df1 = df1_t.T
    df1.to_excel(writer)
    writer.save() #Save to the excel file

#prototype using cmd line inputs
n1 = input("Enter Seller's Name: ")
n2 = input("Enter Buyer's Name: ")
i1 = input("Enter Item Name: ")
c1 = input("Enter Cost: ")
l1 = input("Enter Location: ")
newOrder(n1, n2, i1, c1, l1)
print("New order logged. Thank you.")
