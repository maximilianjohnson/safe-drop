import openpyxl

def status_change():
    complete=input("Is the transaction complete? (y or n) ")
    returned=input("What is the status of the return? (p or s or f)")

    if complete=="n":
        return "incomplete"
    elif returned=="p":
        return "complete: return pending"
    elif returned=="s":
        return "complete: return success"
    elif returned=="f":
        return "complete: return failed"
    else:
        return "stop being a dumbass"


xfile = openpyxl.load_workbook('SD_Order_info.xlsx')
sheet = xfile["Sheet1"]

sheet.cell(row=6,column=10).value = status_change()

xfile.save('test_SD_Order_info.xlsx')
