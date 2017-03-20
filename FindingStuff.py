try:
    from Tkinter import *
    import ttk
except:
    from tkinter import *
    from tkinter import ttk
import csv

def returnSurname(*args):
    with open('MOCK_DATA.csv') as csvfile:
        reader = csv.reader(csvfile)

        nameinput = str(name.get()).lower()

        for row in reader:
            if nameinput == row[0].lower():
                answer1.set("--> " + row[1])
                break
            else:
                answer1.set("--> " + "Name not found.")

def returnNumber(*args):
    with open('MOCK_DATA.csv') as csvfile:
        reader = csv.reader(csvfile)

        nameinput = str(name.get())

        if not nameinput.isdigit():
            for row in reader:
                if nameinput.lower() == row[0].lower():
                    answer2.set("--> " + row[2])
                    break
            else:
                answer2.set("--> " + "Name not found.")
        else:
            for row in reader:
                if nameinput == row[2]:
                    answer2.set("--> " + row[0] + " " + row[1])
                    break
            else:
                answer2.set("--> " + "Number not found.")



root = Tk()
root.title("Get Surname")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

name = StringVar()
answer1 = StringVar()
answer2 = StringVar()


name_entry = ttk.Entry(mainframe, width=10, textvariable=name)
name_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe, textvariable=answer1).grid(column=2, row=2)
ttk.Button(mainframe, text="Lookup Surname", command=returnSurname).grid(column=1, row=2, sticky=W)
ttk.Label(mainframe, text="Please Input Information: ").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="Find a Surname from a Forename.").grid(column=1, row=3, sticky=W)

ttk.Label(mainframe, textvariable=answer2).grid(column=2, row=4)
ttk.Button(mainframe, text="Calculate Number/Name", command=returnNumber).grid(column=1, row=4, sticky=W)
ttk.Label(mainframe, text="Find a Number from Forename, or vice versa.").grid(column=1, row=5, sticky=W)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

name_entry.focus()
root.bind('<Return>', returnSurname)

root.mainloop()
