from customtkinter import *
from PIL import Image
from tkinter import ttk,messagebox
import database

#Functions:

def delete_all():
    result=messagebox.askyesno('Confirm','Do You Really Want to Delete All the Records?')
    if result:
        database.deleteall_records()
        treeview_data()

def show_all():
    treeview_data()
    searchEntry.delete(0,END)
    searchBox.set('Search By')

def search_employee():
    if searchEntry.get()=='':
        messagebox.showerror('Error','Enter Value to Search')
    elif searchBox.get()=='Search By':
        messagebox.showerror('Error', 'Please Select an Option')
    else:
        searched_data=database.search(searchBox.get(),searchEntry.get())
        tree.delete(*tree.get_children())
        for employee in searched_data:
            tree.insert('', END, values=employee)

def delete_employee():
    selected_item=tree.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Select Data To Delete')
    else:
        database.delete(idEntry.get())
        treeview_data()
        clear()
        messagebox.showinfo('Error','Data is Deleted')

def update_employee():
    selected_item=tree.selection()
    if not selected_item:
        messagebox.showerror('Error','Select Data To Update')
    else:
        database.update(idEntry.get(),nameEntry.get(),phoneEntry.get(),roleBox.get(),genderBox.get(),salaryEntry.get())
        treeview_data()
        clear()
        messagebox.showinfo('Success','Data is Updated')

def selection(event):
    selected_item=tree.selection()
    if selected_item:
        row=tree.item(selected_item)['values']
        clear()
        idEntry.insert(0,row[0])
        nameEntry.insert(0,row[1])
        phoneEntry.insert(0,row[2])
        roleBox.set(row[3])
        genderBox.set(row[4])
        salaryEntry.insert(0,row[5])

def clear(value=False):
    if value:
        tree.selection_remove(tree.focus())
    idEntry.delete(0,END)
    nameEntry.delete(0,END)
    phoneEntry.delete(0,END)
    roleBox.set('Web Developer')
    genderBox.set('Male')
    salaryEntry.delete(0,END)

def treeview_data():
    employees=database.fetch_employees()
    tree.delete(*tree.get_children())
    for employee in employees:
        tree.insert('',END,values=employee)

def add_employee():
    if idEntry.get()=='' or phoneEntry.get()=='' or nameEntry.get()=='' or salaryEntry.get()=='':
        messagebox.showerror('Error','All Fields are Required')
    elif database.id_exists(idEntry.get()):
        messagebox.showerror('Error','Employee Already Exists')
    elif not idEntry.get().startswith('EMP'):
        messagebox.showerror('Error', "Invalid ID Format. Use 'EMP' followed by a number (e.g., 'EMP1').")
    else:
        database.insert(idEntry.get(),nameEntry.get(),phoneEntry.get(),roleBox.get(),genderBox.get(),salaryEntry.get())
        treeview_data()
        clear()
        messagebox.showinfo('Success','Data Added Successfully')

window=CTk()
window.geometry('930x580+100+100')
window.resizable(False,False)
window.title('Employee Management System')
window.configure(fg_color='#161C30')
logo=CTkImage(Image.open('bg.jpg'),size=(930,158))
logoLabel=CTkLabel(window,image=logo,text='')
logoLabel.grid(row=0,column=0,columnspan=2)

leftFrame=CTkFrame(window,fg_color='#161C30')
leftFrame.grid(row=1,column=0)

idLabel=CTkLabel(leftFrame,text='Id',font=('arial',18,'bold'),text_color='white')
idLabel.grid(row=0,column=0,padx=20,pady=15,sticky='w')

idEntry=CTkEntry(leftFrame,font=('arial',15,'bold'),width=180,fg_color='white',text_color='black')
idEntry.grid(row=0,column=1)

nameLabel=CTkLabel(leftFrame,text='Name',font=('arial',18,'bold'),text_color='white')
nameLabel.grid(row=1,column=0,padx=20,pady=15,sticky='w')

nameEntry=CTkEntry(leftFrame,font=('arial',15,'bold'),width=180,fg_color='white',text_color='black')
nameEntry.grid(row=1,column=1)

phoneLabel=CTkLabel(leftFrame,text='Phone',font=('arial',18,'bold'),text_color='white')
phoneLabel.grid(row=2,column=0,padx=20,pady=15,sticky='w')

phoneEntry=CTkEntry(leftFrame,font=('arial',15,'bold'),width=180,fg_color='white',text_color='black')
phoneEntry.grid(row=2,column=1)

roleLabel=CTkLabel(leftFrame,text='Role',font=('arial',18,'bold'),text_color='white')
roleLabel.grid(row=3,column=0,padx=20,pady=15,sticky='w')

role_options=['Web Developer','Cloud Architect','Technical Writer','Network Engineer','DevOps Engineer','Data Scientist','Business Analyst','IT Consultant','UI/UX Designer']
roleBox=CTkComboBox(leftFrame,values=role_options,width=180,font=('arial',18,'bold'),state='readonly',fg_color='white',text_color='black')
roleBox.grid(row=3,column=1)
roleBox.set(role_options[0])

genderLabel=CTkLabel(leftFrame,text='Gender',font=('arial',18,'bold'),text_color='white')
genderLabel.grid(row=4,column=0,padx=20,pady=15,sticky='w')

gender_options=['Male','Female']
genderBox=CTkComboBox(leftFrame,values=gender_options,width=180,font=('arial',18,'bold'),state='readonly',fg_color='white',text_color='black')
genderBox.grid(row=4,column=1)
genderBox.set(gender_options[0])

salaryLabel=CTkLabel(leftFrame,text='Salary',font=('arial',18,'bold'),text_color='white')
salaryLabel.grid(row=5,column=0,padx=20,pady=15,sticky='w')

salaryEntry=CTkEntry(leftFrame,font=('arial',15,'bold'),width=180,fg_color='white',text_color='black')
salaryEntry.grid(row=5,column=1)

rightFrame=CTkFrame(window,fg_color='white')
rightFrame.grid(row=1,column=1)

search_options=['Id','Name','Phone','Role','Gender','Salary']
searchBox=CTkComboBox(rightFrame,values=search_options,state='readonly',fg_color='white',text_color='black')
searchBox.grid(row=0,column=0,padx=5)
searchBox.set('Search By')

searchEntry=CTkEntry(rightFrame,fg_color='white',text_color='black')
searchEntry.grid(row=0,column=1,padx=5)

searchButton=CTkButton(rightFrame,text='Search',width=100,command=search_employee)
searchButton.grid(row=0,column=2,padx=5)

showallButton=CTkButton(rightFrame,text='Show All',width=100,command=show_all)
showallButton.grid(row=0,column=3,pady=5,padx=5)

tree=ttk.Treeview(rightFrame,height=13)
tree.grid(row=1,column=0,columnspan=4)

tree['columns']=('Id','Name','Phone','Role','Gender','Salary')

tree.heading('Id',text='Id')
tree.heading('Name',text='Name')
tree.heading('Phone',text='Phone')
tree.heading('Role',text='Role')
tree.heading('Gender',text='Gender')
tree.heading('Salary',text='Salary')

tree.configure(show='headings')

tree.column('Id',width=100)
tree.column('Name',width=160)
tree.column('Phone',width=160)
tree.column('Role',width=200)
tree.column('Gender',width=100)
tree.column('Salary',width=140)

style=ttk.Style()

style.configure('Treeview.Heading',font=('arial',18,'bold'))
style.configure('Treeview',font=('arial',15,'bold'),rowheight=41,background='#161C30',foreground='white')

scrollbar=ttk.Scrollbar(rightFrame,orient=VERTICAL,command=tree.yview)
scrollbar.grid(row=1,column=4,sticky='ns')

tree.config(yscrollcommand=scrollbar.set)

buttonFrame=CTkFrame(window,fg_color='#161C30')
buttonFrame.grid(row=2,column=0,columnspan=2,pady=10)

newButton=CTkButton(buttonFrame,text='New Employee',font=('arial',15,'bold'),width=160,corner_radius=15,command=lambda: clear(True))
newButton.grid(row=0,column=0,pady=5)

addButton=CTkButton(buttonFrame,text='Add Employee',font=('arial',15,'bold'),width=160,corner_radius=15,command=add_employee)
addButton.grid(row=0,column=1,pady=5,padx=5)

updateButton=CTkButton(buttonFrame,text='Update Employee',font=('arial',15,'bold'),width=160,corner_radius=15,command=update_employee)
updateButton.grid(row=0,column=2,pady=5,padx=5)

deleteButton=CTkButton(buttonFrame,text='Delete Employee',font=('arial',15,'bold'),width=160,corner_radius=15,command=delete_employee)
deleteButton.grid(row=0,column=3,pady=5,padx=5)

deleteallButton=CTkButton(buttonFrame,text='Delete All',font=('arial',15,'bold'),width=160,corner_radius=15,command=delete_all)
deleteallButton.grid(row=0,column=4,pady=5,padx=5)

treeview_data()

window.bind('<ButtonRelease>',selection)

window.mainloop()