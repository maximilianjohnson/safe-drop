
#FOR PROTOTYPING ONLY, TO BE EXPANDED UPON FOR WEB INTEGRATION/POSTGRESQL
#Author: Andrew Moreno
#Date: Feb 8th

from tkinter import *
import User_Profiles_DB


def get_selected_row(event):
    try:
        global selected_tuple
        index=list1.curselection()[0]
        selected_tuple=list1.get(index)
        e1.delete(0, END)
        e1.insert(END, selected_tuple[1])
        e2.delete(0, END)
        e2.insert(END, selected_tuple[2])
        e3.delete(0, END)
        e3.insert(END, selected_tuple[3])
        e4.delete(0, END)
        e4.insert(END, selected_tuple[4])
        e5.delete(0, END)
        e5.insert(END, selected_tuple[5])
        e6.delete(0, END)
        e6.insert(END, selected_tuple[6])
        e7.delete(0, END)
        e7.insert(END, selected_tuple[7])
        e8.delete(0, END)
        e8.insert(END, selected_tuple[8])
        e9.delete(0, END)
        e9.insert(END, selected_tuple[9])
        e10.delete(0, END)
        e10.insert(END, selected_tuple[10])
        e11.delete(0, END)
        e11.insert(END, selected_tuple[11])
        e12.delete(0, END)
        e12.insert(END, selected_tuple[12])
        e13.delete(0, END)
        e13.insert(END, selected_tuple[13])
        e14.delete(0, END)
        e14.insert(END, selected_tuple[14])
        e15.delete(0, END)
        e15.insert(END, selected_tuple[15])
    except IndexError:
        pass


def view_command():
    list1.delete(0, END)
    for row in User_Profiles_DB.view():
        list1.insert(END,row)

def search_command():
    list1.delete(0, END)
    for row in User_Profiles_DB.search(firstname_text.get(), lastname_text.get(),\
        username_text.get(), email_text.get(), age_text.get(), \
        datejoined_text.get(), address_text.get(), city_text.get(), province_text.get(), \
        country_text.get(), postalcode_text.get(), distance_value.get(), txa_value.get(), \
        userrating_value.get(), status_text.get()):
        list1.insert(END,row)

def newuser_command():
    User_Profiles_DB.insert_newprofile_up_db(firstname_text.get(), lastname_text.get(),\
        username_text.get(), email_text.get(), age_text.get(), \
        address_text.get(), city_text.get(), province_text.get(), \
        country_text.get(), postalcode_text.get())
    list1.delete(0, END)
    view_command()

def delete_command():
    User_Profiles_DB.delete(selected_tuple[0])
    view_command()

def update_command():
    User_Profiles_DB.update(firstname_text.get(), lastname_text.get(),\
        username_text.get(), email_text.get(), age_text.get(), \
        datejoined_text.get(), address_text.get(), city_text.get(), province_text.get(), \
        country_text.get(), postalcode_text.get(), txa_value.get(), \
        userrating_value.get(), status_text.get(), selected_tuple[0])


window = Tk()

l1 = Label(window, text="First Name")
l1.grid(row=0, column=0)

l2 = Label(window, text="Last Name")
l2.grid(row=0, column=2)

l3 = Label(window, text="Username")
l3.grid(row=0, column=4)

l4 = Label(window, text="Email")
l4.grid(row=0, column=6)

l5 = Label(window, text="Age")
l5.grid(row=0, column=8)

l6 = Label(window, text="Date Joined")
l6.grid(row=1, column=0)

l7 = Label(window, text="Address")
l7.grid(row=1, column=2)

l8 = Label(window, text="City")
l8.grid(row=1, column=4)

l9 = Label(window, text="Province")
l9.grid(row=1, column=6)

l10 = Label(window, text="Country")
l10.grid(row=1, column=8)

l11 = Label(window, text="Postal Code")
l11.grid(row=2, column=0)

l12 = Label(window, text="Distance")
l12.grid(row=2, column=2)

l13 = Label(window, text="TXA")
l13.grid(row=2, column=4)

l14 = Label(window, text="User Rating")
l14.grid(row=2, column=6)

l15 = Label(window, text="Status")
l15.grid(row=2, column=8)


firstname_text = StringVar()
e1 = Entry(window, textvariable=firstname_text)
e1.grid(row=0, column=1)

lastname_text = StringVar()
e2 = Entry(window, textvariable=lastname_text)
e2.grid(row=0, column=3)

username_text = StringVar()
e3 = Entry(window, textvariable=username_text)
e3.grid(row=0, column=5)

email_text = StringVar()
e4 = Entry(window, textvariable=email_text)
e4.grid(row=0, column=7)

age_text = StringVar()
e5 = Entry(window, textvariable=age_text)
e5.grid(row=0, column=9)

datejoined_text = StringVar()
e6 = Entry(window, textvariable=datejoined_text)
e6.grid(row=1, column=1)

address_text = StringVar()
e7 = Entry(window, textvariable=address_text)
e7.grid(row=1, column=3)

city_text = StringVar()
e8 = Entry(window, textvariable=city_text)
e8.grid(row=1, column=5)

province_text = StringVar()
e9 = Entry(window, textvariable=province_text)
e9.grid(row=1, column=7)

country_text = StringVar()
e10 = Entry(window, textvariable=country_text)
e10.grid(row=1, column=9)

postalcode_text = StringVar()
e11 = Entry(window, textvariable=postalcode_text)
e11.grid(row=2, column=1)

distance_value = StringVar()
e12 = Entry(window, textvariable=distance_value)
e12.grid(row=2, column=3)

txa_value = StringVar()
e13 = Entry(window, textvariable=txa_value)
e13.grid(row=2, column=5)

userrating_value = StringVar()
e14 = Entry(window, textvariable=userrating_value)
e14.grid(row=2, column=7)

status_text = StringVar()
e15 = Entry(window, textvariable=status_text)
e15.grid(row=2, column=9)



list1=Listbox(window, height=6, width=150)
list1.grid(row=3, column=0, rowspan=5, columnspan=8)

sb1=Scrollbar(window, orient = VERTICAL)
sb1.grid(row=3, column=14, rowspan=5, sticky=N+S+W)

sb2=Scrollbar(window, orient = HORIZONTAL)
sb2.grid(row=8, column=0, columnspan=8, sticky=W+E+N)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

list1.configure(xscrollcommand=sb2.set)
sb2.configure(command=list1.xview)

list1.bind('<<ListboxSelect>>', get_selected_row)

b1=Button(window, text="View All", width=12, command=view_command)
b1.grid(row=3, column=9)

b2=Button(window, text="Search Entry", width=12, command=search_command)
b2.grid(row=4, column=9)

b3=Button(window, text="Add New User", width=12, command=newuser_command)
b3.grid(row=5, column=9)

b4=Button(window, text="Update Selected", width=12, command=update_command)
b4.grid(row=6, column=9)

b5=Button(window, text="Delete Selected", width=12, command=delete_command)
b5.grid(row=7, column=9)

b6=Button(window, text="Close", width=12, command=window.destroy)
b6.grid(row=8, column=9)

window.mainloop()
