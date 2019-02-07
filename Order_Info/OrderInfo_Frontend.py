"""
Order info database viewer

User can:

View all records
Search an Entry
add entry
update Entry
delete Entry
close

"""
#FOR PROTOTYPING ONLY, TO BE EXPANDED UPON FOR WEB INTEGRATION/POSTGRESQL
#Author: Maximilian Johnson
#Date: Feb 6th

from tkinter import *
import OrderInfo_Backend

def get_selected_row(event):
    global selected_tuple
    index=list1.curselection()[0]
    selected_tuple=list1.get(index)
    e1.delete(0, END)
    e1.insert(END, selected_tuple[0])
    e2.delete(0, END)
    e2.insert(END, selected_tuple[4])
    e3.delete(0, END)
    e3.insert(END, selected_tuple[1])
    e4.delete(0, END)
    e4.insert(END, selected_tuple[6])
    e5.delete(0, END)
    e5.insert(END, selected_tuple[3])
    e6.delete(0, END)
    e6.insert(END, selected_tuple[7])
    e7.delete(0, END)
    e7.insert(END, selected_tuple[2])
    e8.delete(0, END)
    e8.insert(END, selected_tuple[5])

def view_command():
    list1.delete(0, END)
    for row in OrderInfo_Backend.view():
        list1.insert(END,row)

def search_command():
    list1.delete(0, END)
    for row in OrderInfo_Backend.search(OrderNum_value.get(), TXID_value.get(),\
    SUN_value.get(), BUN_value.get(), Item_value.get(),\
    Cost_value.get(), Location_value.get(), DI_value.get()):
        list1.insert(END,row)

def order_command():
    OrderInfo_Backend.newOrder(SUN_value.get(), BUN_value.get(),\
    Item_value.get(), Cost_value.get(), Location_value.get())
    list1.delete(0, END)

def delete_command():
    OrderInfo_Backend.delete(selected_tuple[0])

def update_command():
    OrderInfo_Backend.update(selected_tuple[0], SUN_value.get(),\
    BUN_value.get(), Item_value.get(), Cost_value.get(), Location_value.get())

window = Tk()

l1 = Label(window, text="Order Number")
l1.grid(row=0, column=0)

l2 = Label(window, text="Item Name")
l2.grid(row=1, column=0)

l3 = Label(window, text="TX ID")
l3.grid(row=0, column=2)

l4 = Label(window, text="Cost")
l4.grid(row=1, column=2)

l5 = Label(window, text="Seller Username")
l5.grid(row=0, column=4)

l6 = Label(window, text="Location")
l6.grid(row=1, column=4)

l7 = Label(window, text="Buyer Username")
l7.grid(row=0, column=6)

l8 = Label(window, text="Date Initialized")
l8.grid(row=1, column=6)


OrderNum_value = StringVar()
e1 = Entry(window, textvariable=OrderNum_value)
e1.grid(row=0, column=1)


TXID_value = StringVar()
e3 = Entry(window, textvariable=TXID_value)
e3.grid(row=0, column=3)

#SUN = Seller User Name
SUN_value = StringVar()
e5 = Entry(window, textvariable=SUN_value)
e5.grid(row=0, column=5)

#BUN = Buyer User Name
BUN_value = StringVar()
e7 = Entry(window, textvariable=BUN_value)
e7.grid(row=0, column=7)

Item_value = StringVar()
e2 = Entry(window, textvariable=Item_value)
e2.grid(row=1, column=1)

Cost_value = StringVar()
e4 = Entry(window, textvariable=Cost_value)
e4.grid(row=1, column=3)

Location_value = StringVar()
e6 = Entry(window, textvariable=Location_value)
e6.grid(row=1, column=5)

#DI = Date Initialized
DI_value = StringVar()
e8 = Entry(window, textvariable=DI_value)
e8.grid(row=1, column=7)


list1=Listbox(window, height=6, width=100)
list1.grid(row=2, column=0, rowspan=5, columnspan=6)

sb1=Scrollbar(window, orient = VERTICAL)
sb1.grid(row=2, column=6, rowspan=5, sticky=N+S+W)

sb2=Scrollbar(window, orient = HORIZONTAL)
sb2.grid(row=7, column=0, columnspan=6, sticky=W+E+N)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

list1.configure(xscrollcommand=sb2.set)
sb2.configure(command=list1.xview)

list1.bind('<<ListboxSelect>>', get_selected_row)

b1=Button(window, text="View All", width=12, command=view_command)
b1.grid(row=2, column=7)

b2=Button(window, text="Search Entry", width=12, command=search_command)
b2.grid(row=3, column=7)

b3=Button(window, text="Add New Order", width=12, command=order_command)
b3.grid(row=4, column=7)

b4=Button(window, text="Update Selected", width=12, command=update_command)
b4.grid(row=5, column=7)

b5=Button(window, text="Delete Selected", width=12, command=delete_command)
b5.grid(row=6, column=7)

b6=Button(window, text="Close", width=12, command=window.destroy)
b6.grid(row=7, column=7)

window.mainloop()
