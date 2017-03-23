try:
    from Tkinter import *
    import ttk
    from tkinter import filedialog
except:
    from tkinter import *
    from tkinter import ttk
try:
    import messagebox
except:
    from tkinter import messagebox
import csv
import random
import os
from tkinter import filedialog
def number_of_students(tutor, student_csv, tutor_csv):
    tutorInfo = search_csv(tutor, tutor_csv)
    if tutorInfo:
        tutorName = str(tutorInfo[0] + " " + tutorInfo[1]).lower()
        count = 0
        with open(student_csv) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if tutorName == str(row[4]).lower():
                    count += 1
        return count
    else:
        return False

def list_students(tutor, student_csv, tutor_csv):
    tutorInfo = search_csv(tutor, tutor_csv)
    if tutorInfo:
        tutorName = str(tutorInfo[0] + " " + tutorInfo[1]).lower()
        studentList = []
        with open(student_csv) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if tutorName == str(row[4]).lower():
                    studentList.append(row[0] + " " + row[1])
        return studentList
    else:
        return False


def search_csv(inputToSearch, csvInput, returnAll = False):
    with open(csvInput) as csvfile:
        reader = csv.reader(csvfile)

        if not returnAll:
            for row in reader:
                if inputToSearch == row[2]:
                    return[row[0], row[1], row[2], row[3], row[4]]
                elif inputToSearch == str(row[0]).lower():
                    return[row[0], row[1], row[2], row[3], row[4]]
                elif inputToSearch == str(row[1]).lower():
                    return[row[0], row[1], row[2], row[3], row[4]]
                elif inputToSearch == (str(row[0]).lower() + " " + str(row[1]).lower()):
                    return[row[0], row[1], row[2], row[3], row[4]]
                elif inputToSearch == str(row[3]).lower():
                    return[row[0], row[1], row[2], row[3], row[4]]
                elif inputToSearch == str(row[4]).lower():
                    return[row[0], row[1], row[2], row[3], row[4]]
        else:
            all_results = []
            for row in reader:
                if inputToSearch == row[2]:
                    all_results.append([row[0], row[1], row[2], row[3], row[4]])
                elif inputToSearch == str(row[0]).lower():
                    all_results.append([row[0], row[1], row[2], row[3], row[4]])
                elif inputToSearch == str(row[1]).lower():
                    all_results.append([row[0], row[1], row[2], row[3], row[4]])
                elif inputToSearch == (str(row[0]).lower() + " " + str(row[1]).lower()):
                    all_results.append([row[0], row[1], row[2], row[3], row[4]])
                elif inputToSearch == str(row[3]).lower():
                    all_results.append([row[0], row[1], row[2], row[3], row[4]])
                elif inputToSearch == str(row[4]).lower():
                    all_results.append([row[0], row[1], row[2], row[3], row[4]])
            return all_results

        messagebox.showinfo("Search Info", "Search not found.")
        return False


def get_row_from_name(studentName):
    with open('MOCK_DATA.csv') as csvfile:
        # Initiate row count
        rowCount = 0
        reader = csv.reader(csvfile)
        # Turn single string student name into double string
        splitName = studentName.split(" ")
        # Searches through til its found, adding to row count to be returned
        while True:
            for row in reader:
                if (splitName[0] == row[0]) and (splitName[1] == row[1]):
                    return rowCount
                rowCount += 1
            break

def assignTutor(tutors, studentInfo):
    tutors = tutors
    while len(tutors) != 0:
        randomTutor = []
        if len(tutors) > 1:
            randomTutor = random.choice(tutors)
        elif len(tutors) == 1:
            randomTutor = tutors[0]
        if type(randomTutor) != list:
            return False
        getNumberOfStudentsWithTutor = number_of_students(str(randomTutor[0]).lower(), 'MOCK_DATA.csv', 'MOCK_TUTORS.csv')
        if int(getNumberOfStudentsWithTutor) >= int(randomTutor[4]):
            messagebox.showinfo("Tutor Assignment", "Tutor " + str(randomTutor[0]) + " " + str(randomTutor[1]) + "'s quota is full, press OK to search again.")
            tutors.remove(randomTutor)
        else:
            confirmAssign = messagebox.askquestion("Tutor Assignment", "Assigning tutor " + str(randomTutor[0]) + " " + str(randomTutor[1]) + " to " + studentInfo[0] + " " + studentInfo[1] + ". Is this okay?")
            if confirmAssign == "yes":
                randomTutorName = (randomTutor[0] + " " + randomTutor[1])
                rowNumber = int(row_counter(studentInfo))
                write_tutor(rowNumber, randomTutorName)
                return True
            else:
                messagebox.showinfo("Tutor Assignment", "Tutor was not assigned.")
                return False
    return False

def row_counter(studentInfo):
    with open('MOCK_DATA.csv') as csvfile:
        reader = csv.reader(csvfile)
        count = 0
        for row in reader:
            if row[0] == studentInfo[0]:
                return count
            count += 1

def return_all_rows(csvInput):
    with open(csvInput) as csvfile:
        allresults = []
        reader = csv.reader(csvfile)
        for row in reader:
            allresults.append([row[0], row[1], row[2], row[3], row[4]])
        return allresults

def returnStudent(*args):
    nameinput = str(studentName.get()).lower()
    action = comboValue.get()

    if nameinput == "":
        return

    if action == "Get Info":
        stringOfStudents = ""
        result = search_csv(nameinput, 'MOCK_DATA.csv', returnAll = True)
        for i in result:
            stringOfStudents += (i[0] + " " + i[1] + ", " + i[2] + "\n")
        messagebox.showinfo("Student Info", stringOfStudents)
        return

    if action == "Assign Student":
        getStudent = search_csv(nameinput, 'MOCK_DATA.csv')

        if getStudent[4] != 'none':
            messagebox.showinfo("Student Info", "Student already has a tutor.")
            return

        getTutorWithSameSubject = search_csv(getStudent[3], 'MOCK_TUTORS.csv', returnAll = True)

        if len(getTutorWithSameSubject) == 0:
            getTutorWithSameSubject = return_all_rows('MOCK_TUTORS')

        result = assignTutor(getTutorWithSameSubject, getStudent)

        if result == False:
            getEverything = return_all_rows('MOCK_TUTORS.csv')
            print(getEverything)
            for i in getEverything:
                for z in getTutorWithSameSubject:
                    if i == z:
                        print(z)
                        getEverything.remove(z)
            assignTutor(getEverything, getStudent)
            return




        if action == "Delete Student":
            foundStudent = False
            for row in reader:
                if (nameinput == row[0].lower()) or (nameinput == row[1].lower()) or (nameinput == (row[0].lower() + " " + row[1].lower()) or (nameinput == row[2])):
                    row_to_find = get_row_from_name((row[0] + " " + row[1]))
                    result = messagebox.askquestion("Delete Student", "Deleting student " + (row[0] + " " + row[1]) + ". Is this okay?")
                    if result == "yes":
                        messagebox.showinfo("Delete Student", "Student was deleted.")
                        delete_student(row_to_find)
                    else:
                        messagebox.showinfo("Tutor Assignment", "Student was not deleted.")
                    foundStudent = True
            if not foundStudent:
                messagebox.showinfo("Student Info", "Student Not Found")

def returnTutor(*args):
    nameinput = str(tutorName.get()).lower()
    action = comboValueTutor.get()

    if nameinput == "":
        return

    if action == "Get Info":
        result1 = search_csv(nameinput, 'MOCK_TUTORS.csv')
        result2 = list_students(nameinput, 'MOCK_DATA.csv', 'MOCK_TUTORS.csv')
        if result1 and result2:
            instances = 0
            emptyString = ""
            for i in result2:
                if instances == (len(result2) - 1):
                    emptyString += (i + "\n")
                else:
                    emptyString += (i + ", \n")
                instances += 1
            messagebox.showinfo("Tutor Info", "Tutor has following Students: \n" + emptyString)

    if action == "View Quota":
        result = search_csv(nameinput, 'MOCK_TUTORS.csv')
        if result:
            messagebox.showinfo("Tutor Info", "Tutor has a quota of: " + result[4])

def write_tutor(student_row_number, tutor_name):
    r = csv.reader(open('MOCK_DATA.csv')) # open csv file
    lines = [l for l in r]
    lines[student_row_number][4] = tutor_name

    writer = csv.writer(open('MOCK_DATA_2.csv', 'w'))
    writer.writerows(lines)

    os.remove('MOCK_DATA.csv')
    os.rename('MOCK_DATA_2.csv', 'MOCK_DATA.csv')


def delete_student(row_to_delete):
    r = csv.reader(open('MOCK_DATA.csv'))  # open csv file
    lines = [l for l in r]
    del lines[row_to_delete]

    writer = csv.writer(open('MOCK_DATA_2.csv', 'w'))
    writer.writerows(lines)

    os.remove('MOCK_DATA.csv')
    os.rename('MOCK_DATA_2.csv', 'MOCK_DATA.csv')


# Browse files to select csv
def browse_csv():
    root.fileName = filedialog.askopenfilename(filetypes=(("Comma-seperated values", ".csv"), ("All files", "*")))
    print(root.fileName)  # Bug-testing
    return root.fileName


root = Tk()
root.title("Team 11")

# Adds browse button
button = Button(root, text="Browse", command=browse_csv)
button.grid(column=0, row=4)

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

comboValue = StringVar()
comboValueTutor = StringVar()
studentName = StringVar()
tutorName = StringVar()
answer1 = StringVar()
answer2 = StringVar()


name_entry = ttk.Entry(mainframe, width=10, textvariable=studentName)
name_entry.grid(column=2, row=1, sticky=(W, E))

tutor_entry = ttk.Entry(mainframe, width=10, textvariable=tutorName)
tutor_entry.grid(column=2, row=3, sticky=(W, E))

ttk.Button(mainframe, text="Submit Student", command=returnStudent).grid(column=2, row=2, sticky=W)
#ttk.Label(mainframe, textvariable=answer1).grid(column=2, row=2)
#ttk.Button(mainframe, text="Calculate Surname", command=returnStudent).grid(column=1, row=2, sticky=W)

studentCombo = ttk.Combobox(mainframe, textvariable=comboValue, state='readonly')
studentCombo.bind("<<ComboboxSelected>>", returnStudent)
studentCombo['values'] = ('Get Info', 'Assign Student', 'Reassign Student', 'Delete Student')
studentCombo.current(0)
studentCombo.grid(column=1, row=2, sticky=W)

ttk.Label(mainframe, text="Please Input Student Name/Number: ").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="Please Input Tutor Name/Number: ").grid(column=1, row=3, sticky=W)

#ttk.Label(mainframe, textvariable=answer2).grid(column=2, row=4)
#ttk.Button(mainframe, text="Calculate Number/Name", command=returnNumber).grid(column=1, row=4, sticky=W)
ttk.Button(mainframe, text="Submit Tutor", command=returnTutor).grid(column=2, row=4, sticky=W)

tutorCombo = ttk.Combobox(mainframe, textvariable=comboValueTutor, state='readonly')
tutorCombo.bind("<<ComboboxSelected>>", returnTutor)
tutorCombo['values'] = ('Get Info', 'View Quota')
tutorCombo.current(0)
tutorCombo.grid(column=1, row=4, sticky=W)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

name_entry.focus()
root.bind('<Return>', returnStudent, add="+")
root.bind('<Return>', returnTutor, add="+")

root.mainloop()
