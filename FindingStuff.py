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
from sys import platform
from tkinter import filedialog


studentCSV = ""  # CSV of students' directory
tutorCSV = ""  # CSV of tutors' directory

# Take a tutor name, and the CSV names
# Using this info, we iterate through the student CSV looking for the tutor's name
# If found, we add 1 to count, then return the count at the end.
def number_of_students(tutor, student_csv, tutor_csv, year):
    tutorInfo = search_csv(tutor, tutor_csv)
    if tutorInfo:
        tutorName = str(tutorInfo[0] + " " + tutorInfo[1]).lower()
        count = 0
        with open(student_csv) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row != []:
                    if tutorName == str(row[4]).lower() and year == row[5]:
                        count += 1
        return count
    else:
        return False

# Big money function, assign every student that doesn't have a tutor currently.
# Returns a list of non-assigned students if quotas are full.
def assignAll():
    with open(studentCSV) as csvfile:
        r = csv.reader(open(studentCSV))  # open csv file
        lines = [l for l in r if l != [] ]
        tutors = return_all_rows(tutorCSV)

        for i in lines:
            if i[4] == 'none':

                getTutorWithSameSubject = search_csv(i[3], tutorCSV, returnAll = True)

                if len(getTutorWithSameSubject) == 0:
                    getTutorWithSameSubject = return_all_rows(tutorCSV)

                result = assignTutor(getTutorWithSameSubject, i)

                if result == False:
                    getEverything = return_all_rows(tutorCSV)
                    getTutorWithSameSubject = search_csv(i[3], tutorCSV, returnAll = True)
                    listToSearch = []
                    for i in getEverything:
                        if i not in getTutorWithSameSubject:
                            listToSearch.append(i)
                    assignTutor(listToSearch, i)

				 #assignTutor(tutors, i)
        
        reader = csv.reader(open(studentCSV))  # open csv file
        lines2 = [l for l in reader if l != []]

        stringToPrint = ""

        for i in lines2:
            if i[4] == 'none':
                stringToPrint += (i[0] + " " + i[1] + "\n")

        if stringToPrint != "":
            messagebox.showinfo('Assignment Info', 'Students Not Assigned Due to Full Quotas: ' + stringToPrint)
            return
        messagebox.showinfo('Assign All', 'All students assigned a tutor')
        return

# Goes through the student CSV with a given tutor name
# Return a nicely formatted list of all the student names that go with that particular tutor
def list_students(tutor, student_csv, tutor_csv):
    tutorInfo = search_csv(tutor, tutor_csv)
    if tutorInfo:
        tutorName = str(tutorInfo[0] + " " + tutorInfo[1]).lower()
        studentList = []
        with open(student_csv) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row != []:
                    if tutorName == str(row[4]).lower():
                        studentList.append(row[0] + " " + row[1])
        return studentList
    else:
        return False

# High functionality search function. Take an input, a CSV, and optionally specify to return all rows that match search_csv
# When a match is found, return a nicely formatted list with all information about that student or tutor
def search_csv(inputToSearch, csvInput, returnAll = False):
    with open(csvInput) as csvfile:
        reader = csv.reader(csvfile)

        if not returnAll:
            for row in reader:
            	if row != []:
	                if inputToSearch == row[2]:
	                    return row
	                elif inputToSearch == str(row[0]).lower():
	                    return row
	                elif inputToSearch == str(row[1]).lower():
	                    return row
	                elif inputToSearch == (str(row[0]).lower() + " " + str(row[1]).lower()):
	                    return row
	                elif inputToSearch == str(row[3]).lower():
	                    return row
	                elif inputToSearch == str(row[4]).lower():
	                    return row
        else:
            all_results = []
            for row in reader:
            	if row != []:
	                if inputToSearch == row[2]:
	                    all_results.append(row)
	                elif inputToSearch == str(row[0]).lower():
	                    all_results.append(row)
	                elif inputToSearch == str(row[1]).lower():
	                    all_results.append(row)
	                elif inputToSearch == (str(row[0]).lower() + " " + str(row[1]).lower()):
	                    all_results.append(row)
	                elif inputToSearch == str(row[3]).lower():
	                    all_results.append(row)
	                elif inputToSearch == str(row[4]).lower():
	                    all_results.append(row)

            return all_results

        messagebox.showinfo("Search Info", "Search not found.")
        return False

# Take input of a student name, iterate through rows of the student CSV looking for that student.
# Every iteration adds 1 to a count. Return count when found the student.
def get_row_from_name(studentName):
    with open(studentCSV) as csvfile:
        # Initiate row count
        rowCount = 0
        reader = csv.reader(csvfile)
        # Turn single string student name into double string
        splitName = studentName.split(" ")
        # Searches through til its found, adding to row count to be returned
        while True:
            for row in reader:
                if row != []:
                    if (splitName[0] == row[0]) and (splitName[1] == row[1]):
                        return rowCount
                    rowCount += 1
            break

# The assignment function. Looks primarily for tutors that have the same subject as the student.
# If there are no tutors that share a subject with the student, then search all tutors.
# We also check the quota of the tutor to check they have room for the student.
# If all goes well, we assign the student, otherwise return false.
# Can only be done with unassigned students.
def assignTutor(tutors, studentInfo):
    tutors = tutors
    studentYear = studentInfo[5]
    while len(tutors) != 0:
        randomTutor = []
        if len(tutors) > 1:
            randomTutor = random.choice(tutors)
        elif len(tutors) == 1:
            randomTutor = tutors[0]
        if type(randomTutor) != list:
            return False
        getNumberOfStudentsWithTutor = number_of_students(str(randomTutor[0]).lower(), studentCSV, tutorCSV, studentYear)
        yearRow = -1
        if studentYear == 1:
            yearRow = 4
        if studentYear == 2:
            yearRow = 5
        if studentYear == 3:
            yearRow = 6

        if int(getNumberOfStudentsWithTutor) >= int(randomTutor[yearRow]):
            tutors.remove(randomTutor)
        else:
            randomTutorName = (randomTutor[0] + " " + randomTutor[1])
            rowNumber = int(row_counter(studentInfo))
            write_tutor(rowNumber, randomTutorName)
            return True
    return False

# Same as assign but we remove the student's current tutor from the search as
# We only want tutors that aren't their current (thus, reassign).
def reassignStudent(tutors, studentInfo):


    currentTutor = str(studentInfo[4]).lower()
    getTutor = search_csv(currentTutor, tutorCSV)


    for tutor in tutors:
        if getTutor[2] == tutor[2]:
            tutors.remove(tutor)

    result = assignTutor(tutors, studentInfo)

    if result == False:
        return False
    return

# Simple function to take information and return a row number
def row_counter(studentInfo):
    with open(studentCSV) as csvfile:
        reader = csv.reader(csvfile)
        csvfile.seek(0)
        count = 0
        for row in reader:
            if row != []:
                if row[2] == studentInfo[2]:
                    return count
                count += 1

# Special function to return every value in a CSV,
# formatted as a list of lists.
# Each row is a list.
def return_all_rows(csvInput):
    with open(csvInput) as csvfile:
        allresults = []
        reader = csv.reader(csvfile)
        for row in reader:
            if row != []:
                allresults.append(row)

        return allresults

# Main student function to handle all options from the GUI.
# Takes the action from the GUI, then runs functions relevant to that.
# Get Info takes the text input from GUI, uses the search function then displays the student's relevant information.
# Assign Student and Reassign student are fairly self explanatory, just run the functions using the user's student input.
# Delete student searches for the row number based on input, then deletes that entire row.
def returnStudent(*args):
    nameinput = str(studentName.get()).lower()
    action = comboValue.get()

    if nameinput == "":
        return

    if action == "Get Info":
        stringOfStudents = ""
        result = search_csv(nameinput, studentCSV, returnAll = True)
        if result:
            for i in result:
                stringOfStudents += ("Name: " + i[0] + " " + i[1] + " | " + "Student No: " + i[2] + " | " + "Tutor: " + i[4] + "\n")
            messagebox.showinfo("Student Info", stringOfStudents)
            return

    if action == "Assign Student":
        getStudent = search_csv(nameinput, studentCSV)

        if getStudent:
            if getStudent[4] != 'none':
                messagebox.showinfo("Student Info", "Student already has a tutor.")
                return

            getTutorWithSameSubject = search_csv(getStudent[3], tutorCSV, returnAll = True)

        if len(getTutorWithSameSubject) == 0:
            getTutorWithSameSubject = return_all_rows(tutorCSV)
        result = assignTutor(getTutorWithSameSubject, getStudent)

        if result == False:
                getEverything = return_all_rows(tutorCSV)
                getTutorWithSameSubject = search_csv(getStudent[3], tutorCSV, returnAll = True)
                listToSearch = []
                for i in getEverything:
                    if i not in getTutorWithSameSubject:
                        listToSearch.append(i)
                assignTutor(listToSearch, getStudent)
        studentFinal = search_csv(nameinput, studentCSV)
        if studentFinal[4] == 'none':
            messagebox.showinfo("Student info", studentFinal[0] + " " + studentFinal[1] + " has not been assigned. No tutors are available.")
            return
        messagebox.showinfo("Student info", studentFinal[0] + " " + studentFinal[1] + " has been assigned to " + studentFinal[4])
        return

    if action == "Reassign Student":
        getStudent = search_csv(nameinput, studentCSV)

        if getStudent[4] == 'none':
            messagebox.showinfo("Student Info", "Student has not yet been assigned a tutor.")
            return

        getTutorWithSameSubject = search_csv(getStudent[3], tutorCSV, returnAll = True)

        if len(getTutorWithSameSubject) == 0:
            getTutorWithSameSubject = return_all_rows(tutorCSV)
        result = reassignStudent(getTutorWithSameSubject, getStudent)

        if result == False:
                getEverything = return_all_rows(tutorCSV)
                getTutorWithSameSubject = search_csv(getStudent[3], tutorCSV, returnAll = True)
                listToSearch = []
                for i in getEverything:
                    if i not in getTutorWithSameSubject:
                        listToSearch.append(i)
                reassignStudent(listToSearch, getStudent)
        studentFinal = search_csv(nameinput, studentCSV)
        if studentFinal[4] == 'none':
            messagebox.showinfo("Student info", studentFinal[0] + " " + studentFinal[1] + " has not been assigned. No tutors are available.")
            return
        messagebox.showinfo("Student info", studentFinal[0] + " " + studentFinal[1] + " has been assigned to " + studentFinal[4])
        return

    if action == "Delete Student":
        result = search_csv(nameinput, studentCSV)
        if result:
            name_to_delete = result[0] + " " + result[1]
            row_number = get_row_from_name(name_to_delete)
            confirmAssign = messagebox.askquestion("Delete Student", "Delete Student " + name_to_delete + "?")
            if confirmAssign == "yes":
                delete_student(int(row_number))
                return True
            else:
                messagebox.showinfo("Tutor Assignment", "Tutor was not assigned.")
                return False
        return
#Handles the user input in the tutor name/number input box
def returnTutor(*args):
    #parses inout value
    nameinput = str(tutorName.get()).lower()
    action = comboValueTutor.get()

    #returns if no command is given
    if nameinput == "":
        return
    #if get info is selected in the combo box then the file is searched for a tutor and their name and students they have are displayed
    if action == "Get Info":
        result1 = search_csv(nameinput, tutorCSV)
        result2 = list_students(nameinput, studentCSV, tutorCSV)
        if result1 and result2:
            instances = 0
            emptyString = ""
            for i in result2:
                if instances == (len(result2) - 1):
                    emptyString += (i + "\n")
                else:
                    emptyString += (i + ", \n")
                instances += 1
            messagebox.showinfo("Tutor Info", "Name: " + result1[0] + " " + result1[1] + " | " + "Staff No: " + result1[2] + " | " + "Subject: " + result1[3] + "\n" + "Students: \n" + emptyString)
            return
        elif result1:
            messagebox.showinfo("Tutor Info", result1[0] + " " + result1[1] + " has no students")
            return

    #Function that finds a tutor in the file according to user input and prints their quota
    if action == "View Quota":
        result = search_csv(nameinput, tutorCSV)
        if result:
            if int(result[4]) <= 1:
                messagebox.showinfo("Tutor Info", result[0] + " " + result[1] + " has a quota of 0")
            elif int(result[4]) > 1:
                messagebox.showinfo("Tutor Info", "Quota for " + result[0] + " " + result[1] + ": \n 1st Year: " + result[4] + "\n 2nd Year: " + result[5] + "\n 3rd Year: " + result[6])

#Function that takes a tutor name and writes it into a given row of the CSV file                
def write_tutor(student_row_number, tutor_name):
    r = csv.reader(open(studentCSV))  # open csv file
    lines = [l for l in r if l != []]
    lines[student_row_number][4] = tutor_name

    writer = csv.writer(open(studentCSV, 'w'))
    writer.writerows(lines)


#Function that takes a row on the CSV file as an argument and deletes that row from the file
def delete_student(row_to_delete):
    r = csv.reader(open(studentCSV))  # open csv file
    lines = [l for l in r if l != []]
    del lines[row_to_delete]

    writer = csv.writer(open(studentCSV, 'w'))
    writer.writerows(lines)




#Gets the directory of the Student CSV file chosen in the file explorer window
def browse_student_csv():
    root.fileName = filedialog.askopenfilename(filetypes=(("Comma-seperated values", ".csv"), ("All files", "*")))
    global studentCSV
    studentCSV = root.fileName
    messagebox.showinfo('File Upload', 'Student file successfully uploaded')

#Gets the directory of the Tutor CSV file chosen in the file explorer window
def browse_tutor_csv():
    root.fileName = filedialog.askopenfilename(filetypes=(("Comma-seperated values", ".csv"), ("All files", "*")))
    global tutorCSV
    tutorCSV = root.fileName
    messagebox.showinfo('File Upload', 'Tutor file successfully uploaded')


root = Tk()
root.title("Team 11")

# Adds browse button

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

ttk.Separator(mainframe).grid(column=3)
ttk.Label(mainframe, text="Choose CSVs to be used: ").grid(column=4, row=2)
ttk.Button(mainframe, text="Upload student CSV", command=browse_student_csv).grid(column=4, row=3, sticky=W)
ttk.Button(mainframe, text="Upload tutor CSV", command=browse_tutor_csv).grid(column=4, row=4, sticky=W)


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
ttk.Button(mainframe, text="Assign All Students", command=assignAll).grid(column=4, row=1, sticky=W)
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
