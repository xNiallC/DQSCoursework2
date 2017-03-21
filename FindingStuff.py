try:
    from Tkinter import *
    import ttk
except:
    from tkinter import *
    from tkinter import ttk
import csv
import random

def assignTutor(tutorList):
    with open('MOCK_DATA.csv') as csvfile:
        reader = csv.reader(csvfile)

        newTempDict = tutorList

        while len(newTempDict) != 0:
            randomTutor = random.choice(list(tutorList.items()))
            numberOfStudentsWithTutor = 0
            for row in reader:
                if row[4] == randomTutor[0]:
                    numberOfStudentsWithTutor += 1
            if numberOfStudentsWithTutor >= int(randomTutor[1]):
                del newTempDict[randomTutor[0]]
            else:
                print("success")
                break


def returnStudent(*args):
    # Open CSV File
    with open('MOCK_DATA.csv', 'r+') as csvfile:
        with open('MOCK_TUTORS.csv', 'r+') as tutorscsv:
            # Variable names
            tutorReader = csv.reader(tutorscsv)
            reader = csv.reader(csvfile)

            nameinput = str(studentName.get()).lower()
            action = comboValue.get()

            if action == "Get Info":
                for row in reader:
                    if (nameinput == row[0].lower()) or (nameinput == row[1].lower()):
                        answer1.set("--> " + row[0] + " " + row[1] + " " + row[2])
                        break
                    elif nameinput == row[2]:
                        answer1.set("--> " + row[0] + " " + row[1])
                        break
                    else:
                        answer1.set("--> " + "Student not found.")

            if action == "Assign Student":
                tempList = {}
                tempStudent = ""
                for row in reader:
                    if (nameinput == row[2]):
                        tempStudent = row[3]
                    else:
                        answer1.set("--> Student Not Found")
                        break
                for row in tutorReader:
                    if tempStudent == row[3]:
                        tempList[row[0] + " " + row[1]] = row[4]
                if len(tempList) == 0:
                    for row in tutorReader:
                        tempList[row[0] + " " + row[1]] = row[4]
                    assignTutor(tempList)
                else:
                    assignTutor(tempList)

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

comboValue = StringVar()
studentName = StringVar()
answer1 = StringVar()
answer2 = StringVar()


name_entry = ttk.Entry(mainframe, width=10, textvariable=studentName)
name_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe, textvariable=answer1).grid(column=2, row=2)
#ttk.Button(mainframe, text="Calculate Surname", command=returnStudent).grid(column=1, row=2, sticky=W)

studentCombo = ttk.Combobox(mainframe, textvariable=comboValue, state='readonly')
studentCombo.bind("<<ComboboxSelected>>", returnStudent)
studentCombo['values'] = ('Get Info', 'Assign Student', 'Reassign Student', 'Delete Student')
studentCombo.current(0)
studentCombo.grid(column=1, row=2, sticky=W)

ttk.Label(mainframe, text="Please Input Student Name/Number: ").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="Find a Surname from a Forename.").grid(column=1, row=3, sticky=W)

ttk.Label(mainframe, textvariable=answer2).grid(column=2, row=4)
ttk.Button(mainframe, text="Calculate Number/Name", command=returnNumber).grid(column=1, row=4, sticky=W)
ttk.Label(mainframe, text="Find a Number from Forename, or vice versa.").grid(column=1, row=5, sticky=W)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

name_entry.focus()
root.bind('<Return>', returnStudent)

root.mainloop()
