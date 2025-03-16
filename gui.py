import tkinter as tk
from PIL import Image, ImageTk
from api import app, db  # Import your Flask app and database instance
from api import Employee
import tkcalendar as tkc
from datetime import datetime
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk

def on_click():
    # Create a new Toplevel window
    popup = tk.Toplevel(window)

    # Set the window title
    popup.title('Popup Window')

    # Create labels and text fields for username, password, confirm password, DOB, phone number, designation, and department
    label1 = tk.Label(popup, text='Username')
    label1.grid(row=0, column=0, padx=10, pady=10)
    textfield1 = tk.Entry(popup)
    textfield1.grid(row=0, column=1, padx=10, pady=10)

    label2 = tk.Label(popup, text='Password')
    label2.grid(row=1, column=0, padx=10, pady=10)
    textfield2 = tk.Entry(popup)
    textfield2.grid(row=1, column=1, padx=10, pady=10)

    label3 = tk.Label(popup, text='Confirm Password')
    label3.grid(row=2, column=0, padx=10, pady=10)
    textfield3 = tk.Entry(popup)
    textfield3.grid(row=2, column=1, padx=10, pady=10)
    
    label8 = tk.Label(popup, text='Name')
    label8.grid(row=3, column=0, padx=10, pady=10)
    textfield8 = tk.Entry(popup)
    textfield8.grid(row=3, column=1, padx=10, pady=10)
    
    label4 = tk.Label(popup, text='Date of Birth')
    label4.grid(row=7, column=0, padx=10, pady=10)
    date_entry = tkc.DateEntry(popup, date_pattern='y-mm-dd')
    date_entry.grid(row=7, column=1, padx=10, pady=10)

    label5 = tk.Label(popup, text='Phone Number')
    label5.grid(row=4, column=0, padx=10, pady=10)
    textfield5 = tk.Entry(popup)
    textfield5.grid(row=4, column=1, padx=10, pady=10)

    label6 = tk.Label(popup, text='Designation')
    label6.grid(row=5, column=0, padx=10, pady=10)
    textfield6 = tk.Entry(popup)
    textfield6.grid(row=5, column=1, padx=10, pady=10)

    label7 = tk.Label(popup, text='Department')
    label7.grid(row=6, column=0, padx=10, pady=10)
    textfield7 = tk.Entry(popup)
    textfield7.grid(row=6, column=1, padx=10, pady=10)
    

    # Create a button to create a user
    def create_user():
        # Get the text from the text fields
        text1 = textfield1.get()
        text2 = textfield2.get()
        text3 = textfield3.get()
        text4 = date_entry.get()
        text5 = textfield5.get()
        text6 = textfield6.get()
        text7 = textfield7.get()
        text8 = textfield8.get()
        dob = datetime.strptime(text4, '%Y-%m-%d').date()

        if text2 != text3:
            messagebox.showinfo('Warning', 'Password and Confirm Password are not same.Kindly recheck it.Thank You.')
            return
        with app.app_context():
            employee = Employee(text1,text2,dob,int(text5),text6,text7,text8)
            db.session.add(employee)
            db.session.commit()
        popup.destroy()

        # Display a toast message
        messagebox.showinfo('User Created', 'User created successfully')
        # Create a new user with the text from the text fields
        # (Replace this with your own code to create a user)
        

    # Create a button with the "Create User" text and bind it to the create_user function
    create_button = tk.Button(popup, text='Create User', command=create_user)
    create_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

# Create a button to show data of all users
def show_data():
     # Create a new Toplevel window
    popup = tk.Toplevel(window)

    # Set the window title
    popup.title('Employee Data')

    # Create a Treeview frame
    tree_frame = ttk.Frame(popup)
    tree_frame.pack(fill=tk.BOTH, expand=True)

    # Create a Treeview widget
    tree = ttk.Treeview(tree_frame, columns=('username', 'name','password', 'dob', 'phone_number', 'designation', 'department'))

    # Define the column headings
    tree.heading('#0', text='ID')
    tree.heading('username', text='Username')
    tree.heading('name', text='Name')
    tree.heading('password', text='Password')
    tree.heading('dob', text='Date of Birth')
    tree.heading('phone_number', text='Phone Number')
    tree.heading('designation', text='Designation')
    tree.heading('department', text='Department')

    # Define the column widths
    tree.column('#0', width=50)
    tree.column('username', width=100)
    tree.column('name', width=100)
    tree.column('password', width=100)
    tree.column('dob', width=100)
    tree.column('phone_number', width=100)
    tree.column('designation', width=100)
    tree.column('department', width=100)

    # Add data to the Treeview
    with app.app_context():
        employees = Employee.query.all()
        for i, employee in enumerate(employees):
            tree.insert('', 'end', text=str(i+1), values=(employee.email, employee.name,employee.pswd, employee.dob, employee.phone, employee.desigination, employee.department))

    # Add the Treeview to the frame
    tree.pack(fill=tk.BOTH, expand=True)
    pass


# Create a new Tkinter window
window = tk.Tk()
window.attributes('-fullscreen',False)
# Load the image and convert it to a Tkinter-compatible photo image
image = Image.open('bg.png')
photo = ImageTk.PhotoImage(image)

# Create a label with the photo image and add it to the window
label = tk.Label(window, image=photo)
label.place(x=0, y=0)
label.pack()

button = tk.Button(window, text='Create User', bg='White', width=20, height=4, command=on_click) 
button.place(relx=0.85, rely=0.35, anchor='center')

show_button = tk.Button(window, text='Show Data', bg='White', width=20, height=4, command=show_data) 
show_button.place(relx=0.85, rely=0.6, anchor='center')

button = tk.Button(window, text='Exit', bg='White', width=20, height=4, command=window.destroy) 
button.place(relx=0.85, rely=0.85, anchor='center')

# Start the Tkinter event loop
window.mainloop()

