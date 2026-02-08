import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

FILE = "transport_data.csv"

# create csv if not exists
if not os.path.exists(FILE):
    with open(FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Owner","OwnerPhone","Address","AC","Bank",
            "Driver","DriverPhone","Vehicle",
            "From","To","Departure","Arrival",
            "Income","Fuel","Toll","Repair","Food","Parking","Police"
        ])

root = tk.Tk()
root.title("Transport Business Dashboard")
root.geometry("900x650")

FONT_LABEL = ("Arial", 12, "bold")
FONT_ENTRY = ("Arial", 12)
FONT_HEAD = ("Arial", 16, "bold")

# ================= VARIABLES =================
owner = tk.StringVar()
owner_phone = tk.StringVar()
address = tk.StringVar()
ac = tk.StringVar()
bank = tk.StringVar()

driver = tk.StringVar()
driver_phone = tk.StringVar()
vehicle = tk.StringVar()

trip_from = tk.StringVar()
trip_to = tk.StringVar()

income = tk.StringVar()
fuel = tk.StringVar()
toll = tk.StringVar()
repair = tk.StringVar()
food = tk.StringVar()
parking = tk.StringVar()
police = tk.StringVar()

dep_day = tk.StringVar(value="01")
dep_month = tk.StringVar(value="01")
dep_year = tk.StringVar(value="2026")

arr_day = tk.StringVar(value="01")
arr_month = tk.StringVar(value="01")
arr_year = tk.StringVar(value="2026")

# ================= FUNCTIONS =================
def calculate():
    try:
        inc = float(income.get() or 0)
        exp = sum([
            float(fuel.get() or 0),
            float(toll.get() or 0),
            float(repair.get() or 0),
            float(food.get() or 0),
            float(parking.get() or 0),
            float(police.get() or 0),
        ])
        total_lbl.config(text=f"Total Expense: ₹{exp}")
        profit_lbl.config(text=f"Profit: ₹{inc-exp}")
    except:
        pass

def clear_fields():
    for v in [
        owner,owner_phone,address,ac,bank,
        driver,driver_phone,vehicle,
        trip_from,trip_to,income,fuel,toll,repair,food,parking,police
    ]:
        v.set("")

def save_data():
    if driver.get()=="" or vehicle.get()=="":
        messagebox.showerror("Error","Driver & Vehicle required")
        return

    departure = f"{dep_day.get()}-{dep_month.get()}-{dep_year.get()}"
    arrival = f"{arr_day.get()}-{arr_month.get()}-{arr_year.get()}"

    with open(FILE,"a",newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            owner.get(),owner_phone.get(),address.get(),ac.get(),bank.get(),
            driver.get(),driver_phone.get(),vehicle.get(),
            trip_from.get(),trip_to.get(),
            departure,arrival,
            income.get(),fuel.get(),toll.get(),repair.get(),food.get(),parking.get(),police.get()
        ])

    clear_fields()
    calculate()
    messagebox.showinfo("Saved","Data saved successfully")

# ================= TABLE VIEW =================
def table_view():
    win = tk.Toplevel(root)
    win.title("Records")
    win.geometry("1200x450")

    search_var = tk.StringVar()

    top = tk.Frame(win)
    top.pack(fill="x", pady=5)

    tk.Label(top, text="Search:", font=FONT_LABEL).pack(side="left", padx=5)
    tk.Entry(top, textvariable=search_var, font=FONT_ENTRY, width=30).pack(side="left")

    table_frame = tk.Frame(win)
    table_frame.pack(fill="both", expand=True)

    y_scroll = tk.Scrollbar(table_frame, orient="vertical")
    x_scroll = tk.Scrollbar(table_frame, orient="horizontal")

    tree = ttk.Treeview(
        table_frame,
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
    )

    y_scroll.config(command=tree.yview)
    x_scroll.config(command=tree.xview)

    y_scroll.pack(side="right", fill="y")
    x_scroll.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)

    with open(FILE) as f:
        reader = list(csv.reader(f))
        headers = reader[0]
        rows = reader[1:]

    tree["columns"] = headers
    tree["show"] = "headings"
    for c in headers:
        tree.heading(c, text=c)
        tree.column(c, width=130, anchor="center")

    def load_data(data):
        tree.delete(*tree.get_children())
        for r in data:
            tree.insert("", "end", values=r)

    load_data(rows)

    def search_data(*args):
        keyword = search_var.get().lower()
        filtered = [r for r in rows if keyword in " ".join(r).lower()]
        load_data(filtered)

    search_var.trace("w", search_data)

# ================= PDF =================
def generate_pdf():
    if driver.get() == "":
        messagebox.showerror("Error", "Driver required")
        return

    filename = f"Bill_{driver.get()}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)

    y = 750
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, y, "Transport Bill")

    c.setFont("Helvetica", 11)
    y -= 40

    lines = [
        f"Owner: {owner.get()}",
        f"Driver: {driver.get()}",
        f"Vehicle: {vehicle.get()}",
        f"From: {trip_from.get()}",
        f"To: {trip_to.get()}",
        "",
        f"Income: {income.get()}",
        f"Fuel: {fuel.get()}",
        f"Toll: {toll.get()}",
        f"Repair: {repair.get()}",
        f"Food: {food.get()}",
        f"Parking: {parking.get()}",
        f"Police: {police.get()}",
        "",
        total_lbl.cget("text"),
        profit_lbl.cget("text")
    ]

    for line in lines:
        c.drawString(50, y, line)
        y -= 20

    c.save()
    messagebox.showinfo("PDF", f"Bill saved as {filename}")

# ================= UI =================
tk.Label(root,text="Transport Business Dashboard",font=FONT_HEAD).pack(pady=10)

main = tk.Frame(root)
main.pack()

def make_frame(title, row, col):
    f = tk.LabelFrame(main,text=title,font=FONT_LABEL)
    f.grid(row=row,column=col,padx=10,pady=10)
    return f

owner_frame = make_frame("Owner Details",0,0)
driver_frame = make_frame("Driver Details",0,1)
income_frame = make_frame("Income & Expenses",1,0)
trip_frame = make_frame("Trip Details",1,1)

# Owner UI
for i,(t,v) in enumerate([("Name",owner),("Phone",owner_phone),
("Address",address),("A/C",ac),("Bank",bank)]):
    tk.Label(owner_frame,text=t,font=FONT_LABEL).grid(row=i,column=0)
    tk.Entry(owner_frame,textvariable=v,font=FONT_ENTRY,width=18).grid(row=i,column=1)

# Driver UI
for i,(t,v) in enumerate([("Driver",driver),("Phone",driver_phone),("Vehicle",vehicle)]):
    tk.Label(driver_frame,text=t,font=FONT_LABEL).grid(row=i,column=0)
    tk.Entry(driver_frame,textvariable=v,font=FONT_ENTRY,width=18).grid(row=i,column=1)

# Income UI
fields = [("Income",income),("Fuel",fuel),("Toll",toll),
("Repair",repair),("Food",food),("Parking",parking),("Police",police)]

for i,(t,v) in enumerate(fields):
    tk.Label(income_frame,text=t,font=FONT_LABEL).grid(row=i,column=0)
    tk.Entry(income_frame,textvariable=v,font=FONT_ENTRY,width=18).grid(row=i,column=1)
    v.trace("w",lambda *args:calculate())

# Trip UI
tk.Label(trip_frame,text="From",font=FONT_LABEL).grid(row=0,column=0)
tk.Entry(trip_frame,textvariable=trip_from,font=FONT_ENTRY).grid(row=0,column=1)

tk.Label(trip_frame,text="To",font=FONT_LABEL).grid(row=1,column=0)
tk.Entry(trip_frame,textvariable=trip_to,font=FONT_ENTRY).grid(row=1,column=1)

tk.Label(trip_frame,text="Kab Gayi",font=FONT_LABEL).grid(row=2,column=0)
ttk.Combobox(trip_frame,textvariable=dep_day,values=[f"{i:02d}" for i in range(1,32)],width=4).grid(row=2,column=1,sticky="w")
ttk.Combobox(trip_frame,textvariable=dep_month,values=[f"{i:02d}" for i in range(1,13)],width=4).grid(row=2,column=1)
ttk.Combobox(trip_frame,textvariable=dep_year,values=[str(i) for i in range(2024,2031)],width=6).grid(row=2,column=1,sticky="e")

tk.Label(trip_frame,text="Kab Aayi",font=FONT_LABEL).grid(row=3,column=0)
ttk.Combobox(trip_frame,textvariable=arr_day,values=[f"{i:02d}" for i in range(1,32)],width=4).grid(row=3,column=1,sticky="w")
ttk.Combobox(trip_frame,textvariable=arr_month,values=[f"{i:02d}" for i in range(1,13)],width=4).grid(row=3,column=1)
ttk.Combobox(trip_frame,textvariable=arr_year,values=[str(i) for i in range(2024,2031)],width=6).grid(row=3,column=1,sticky="e")

total_lbl = tk.Label(root,text="Total Expense: ₹0",font=("Arial",13,"bold"))
total_lbl.pack()

profit_lbl = tk.Label(root,text="Profit: ₹0",fg="green",font=("Arial",13,"bold"))
profit_lbl.pack()

tk.Button(root,text="Save Data",bg="green",fg="white",font=FONT_LABEL,command=save_data).pack(pady=5)
tk.Button(root,text="Table View",font=FONT_LABEL,command=table_view).pack()
tk.Button(root,text="Generate PDF Bill",bg="#1E88E5",fg="white",font=FONT_LABEL,command=generate_pdf).pack(pady=5)

root.mainloop()