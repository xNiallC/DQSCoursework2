try:
    from Tkinter import *
    import ttk
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

def tutor_quota(tutorName):
    with open('MOCK_TUTORS.csv') as csvfile:
        reader = csv.reader(csvfile)
        tutorNameSplit = ""
        # Check whether we recieved a list or a string, if a list then we make a string
        if " " not in tutorName:
            tutorNameSplit = tutorName
        else:
            tutorNameSplit = tutorName.lower().split(" ")
        for row in reader:
            # Find tutor in CSV and return quota
            if (tutorNameSplit[0] == str(row[0]).lower()) and (tutorNameSplit[1] == str(row[1]).lower()):
                (row[4])
                return int(row[4])

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




def assignTutor(tutorList, studentName2, tempStudent):
    with open('MOCK_DATA.csv') as csvfile:
        reader = csv.reader(csvfile)

        newTempList = tutorList
        studentName = studentName2
        # This is where it got harder.
        # The while loop checks that the list of available tutors is not 0, which we come to later.
        while len(newTempList) != 0:

            # Pick random tutor from list
            randomTutor = random.choice(newTempList)
            # Initialise variable for tutor quote
            numberOfStudentsWithTutor = 0

            # For each row in the student csv, if they currently have the randomly selected tutor, add 1 to the variable.
            for row in reader:
                if row[4] == randomTutor:
                    numberOfStudentsWithTutor += 1

            tutorQuota = tutor_quota(randomTutor)
            # We now compare the variable with the tutor's quota number in the CSV.
            # If this number is equal to or exceeds their quota, we delete them from the list.
            # Else the while loop goes again until their are no tutors left.
            if numberOfStudentsWithTutor >= tutorQuota:
                messagebox.showinfo("Tutor Assignment", "Tutor " + randomTutor + "'s quota is full, press OK to search again.")
                newTempList.remove(randomTutor)
            else:
                result = messagebox.askquestion("Tutor Assignment", "Assigning tutor " + randomTutor + " to " + studentName + ". Is this okay?")
                if result == 'yes':
                    # Create nicely formatted string to return
                    return randomTutor
                else:
                    # Return an error, then continue loop
                    messagebox.showinfo("Tutor Assignment", "Tutor was not assigned.")
                    return False
        # Total failure. Exit loop and rerun function later.
        messagebox.showinfo("Tutor Assignment", "No tutors available.")
        return False

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
                foundStudent = False
                # Searching for information
                for row in reader:
                    # Returns full info if you know a first/second name
                    if (nameinput == row[0].lower()) or (nameinput == row[1].lower()):
                        messagebox.showinfo("Student Info", "Student Name and Number: \n" + row[0] + " " + row[1] + " " + row[2] + "\nTutor: \n" + row[4])
                        foundStudent = True
                        break
                    # Returns a name if you know a number
                    elif nameinput == row[2]:
                        messagebox.showinfo("Student Info", "Student Name: \n" + row[0] + " " + row[1] + "\nTutor: \n" + row[4])
                        foundStudent = True
                        break
                    # Returns a nope if you know nothing
                if not foundStudent:
                    messagebox.showinfo("Student Info", "Student Not Found")

            if action == "Assign Student":
                # Initialise variables
                tempList = []
                tempList2 = []
                tempStudent = ""
                studentName2 = ""
                foundStudent = False
                foundStudentButHasTutor = False
                studentCountForTutor = 0
                # Find a student from a number and assign its subject to the tempStudent variable
                for row in reader:
                    if (nameinput == row[2]) and (str(row[4]) != 'none'):
                        # We check if they have a tutor, if so just end the function
                        messagebox.showinfo("Student Info", "Student already has a tutor.")
                        foundStudentButHasTutor = True
                        foundStudent = True
                        return
                    elif (nameinput == row[2]):
                        tempStudent = row[3]
                        studentName2 = row[0] + " " + row[1]
                        foundStudent = True
                if not foundStudentButHasTutor and not foundStudent:
                    messagebox.showinfo("Student Info", "Student Not Found")
                # Here it gets more complex. We earlier created a temporary dict.
                # Now we iterate through the csv of tutor, and if the tutor's subject matches the student's
                # we add the tutor's full name and quota number to the dict.
                if foundStudent:
                    for row in tutorReader:
                        if tempStudent == row[3]:
                            tempList.append(row[0] + " " + row[1])

                            # Run function using list we made, then get the result. If tutor is found, we return the tutor name,
                            # else it fails and we re-run it with a list of tutors who's subject isn't the same as the student's.
                    result = assignTutor(tempList, studentName2, tempStudent)
                    rowToEdit = get_row_from_name(studentName2)
                    if result:
                        write_tutor(rowToEdit, result)
                    else:
                        # When CSV is read, the cursor is left at the end of the file. So we have to seek back to the start to search again.
                        tutorscsv.seek(0)
                        for row in tutorReader:
                            if tempStudent != row[3]:
                                tempList2.append(row[0] + " " + row[1])
                        # Second running
                        result2 = assignTutor(tempList2, studentName2, tempStudent)
                        if result2:
                            write_tutor(rowToEdit, result2)

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

def returnTutorInfo(tutorInput):
    with open('MOCK_DATA.csv') as csvfile:

        reader = csv.reader(csvfile)

        nameinput = tutorInput
        nameSplit = ""
        tempStudents = []
        foundTutor = False
        nameSplitFinal = ""

        for row in reader:
            # As the tutor name is all one word, first and last, we split into 2 for sake of easy searching
            if " " not in str(row[4]):
                nameSplit = row[4]
            else:
                nameSplit = row[4].split(" ")
            # Check stuff
            if (nameinput.lower() == str(nameSplit[0]).lower()) or (nameinput.lower() == str(nameSplit[1]).lower()) or (nameinput == str(row[4]).lower()):
                # Append to empty list a string of the students name nicely formatted
                nameSplitFinal = nameSplit
                tempStudents.append(row[0] + " " + row[1])
                foundTutor = True

        if foundTutor:
            # To make our software scalable, it returns the students and the name of the teacher. Useful!
            return {'listStudents':tempStudents, 'nameOfTutorAsList':nameSplitFinal}
        if not foundTutor:
            # If the tutor doesn't have any students, they won't be in the student csv, so we need to search the
            # tutor csv. We also then need to return a different value for their students to indicate they have none.
            # So, I use 'failed'
            with open('MOCK_TUTORS.csv') as tutorscsv:
                tutorReader = csv.reader(tutorscsv)
                for row in tutorReader:
                    if (tutorInput == str(row[0]).lower()) or (tutorInput == str(row[1]).lower()) or (tutorInput == str(row[0] + row[1]).lower() or (tutorInput == row[2])):
                        nameinput = str(row[0] + " " + row[1])
            tempStudents = ['failed']
            return {'listStudents':tempStudents, 'nameOfTutorAsList':nameinput}

def returnTutor(*args):
    with open('MOCK_DATA.csv') as csvfile:
        reader = csv.reader(csvfile)

        nameinput = str(tutorName.get())

        action = comboValueTutor.get()

        # Getting info for tutor's srudents
        if action == "Get Info":
            # Initialise variables
            getNeededInfo = returnTutorInfo(nameinput)
            studentList = getNeededInfo['listStudents']
            emptyString = ""

            if str(studentList[0]) != 'failed':

                # We like nice formatting, so if there's only 1 student, correct grammar is used.
                if len(studentList) == 1:
                    # For each student in list, add to a string for ing
                    for i in studentList:
                        emptyString += i
                        # Message boxes for easy to read information
                    messagebox.showinfo("Tutor Info", "Tutor has following Student: \n" + emptyString)
                elif len(studentList) > 1:
                    # In order to correctly format commas, we take instances for number of iterations
                    instances = 0
                    for i in studentList:
                        # Checks if it's the last name, and if so don't put a comma
                        if instances == (len(studentList) - 1):
                            emptyString += (i + "\n")
                        else:
                            emptyString += (i + ", \n")
                        instances += 1
                    messagebox.showinfo("Tutor Info", "Tutor has following Students: \n" + emptyString)

            else:
                messagebox.showinfo("Tutor Info", "Tutor not found/has no students")

        if action == "View Quota":
            # Pretty straight forward feature. Just runs a bunch of functions.
            # We also again check whether we recieve a string or a list
            getNeededInfo = returnTutorInfo(nameinput)
            formattedTutorName = ""
            if getNeededInfo:
                tutorNameToUse = getNeededInfo['nameOfTutorAsList']
                if type(tutorNameToUse) != str:
                    formattedTutorName = tutorNameToUse[0] + " " + tutorNameToUse[1]
                else:
                    formattedTutorName = tutorNameToUse
                result = tutor_quota(formattedTutorName)
                messagebox.showinfo("Tutor Info", "Tutor's Quota is: " + str(result))


# Similair functions. Both create a new CSV with the required info, then replace
# the old ones.

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


root = Tk()
root.title("Team 11")

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


# Push Test
