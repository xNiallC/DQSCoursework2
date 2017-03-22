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

def assignTutor(tutorList, studentName2, tempStudent):
    global runTwice
    global runAgain
    with open('MOCK_DATA.csv') as csvfile:
        reader = csv.reader(csvfile)

        newTempDict = tutorList
        studentName = studentName2
        # This is where it got harder.
        # The while loop checks that the list of available tutors is not 0, which we come to later.
        while len(newTempDict) != 0:

            # Pick random tutor from list
            randomTutor = random.choice(list(tutorList.items()))
            randomTutorString = ""
            # Initialise variable for tutor quote
            numberOfStudentsWithTutor = 0

            # For each row in the student csv, if they currently have the randomly selected tutor, add 1 to the variable.
            for row in reader:
                if row[4] == randomTutor[0]:
                    numberOfStudentsWithTutor += 1

            # We now compare the variable with the tutor's quota number in the CSV.
            # If this number is equal to or exceeds their quota, we delete them from the list.
            # Else the while loop goes again until their are no tutors left.
            if numberOfStudentsWithTutor >= int(randomTutor[1]):
                messagebox.showinfo("Tutor Assignment", "Tutor " + randomTutor[0] + "'s quota is full, press OK to search again.")
                del newTempDict[randomTutor[0]]
            else:
            # TODO: Nothing is actually written to the csv yet, I just completed the algorithm. Next step is to write the tutor name to the CSV.
                result = messagebox.askquestion("Tutor Assignment", "Assigning tutor " + randomTutor[0] + " to " + studentName + ". Is this okay?")
                if result == 'yes':
                    # Create nicely formatted string to return
                    randomTutorString = randomTutor[0] + " " + randomTutor[1]
                    return randomTutorString
                else:
                    # Return an error, then continue loop
                    messagebox.showinfo("Tutor Assignment", "Tutor was not assigned.")
                    return False
        # Total failure. Exit loop and rerun function later.
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
                # Searching for information
                for row in reader:
                    # Returns full info if you know a first/second name
                    if (nameinput == row[0].lower()) or (nameinput == row[1].lower()):
                        answer1.set("--> " + row[0] + " " + row[1] + " " + row[2])
                        break
                    # Returns a name if you know a number
                    elif nameinput == row[2]:
                        answer1.set("--> " + row[0] + " " + row[1])
                        break
                    # Returns a nope if you know nothing
                    else:
                        answer1.set("--> " + "Student not found.")

            if action == "Assign Student":
                # Initialise variables
                tempList = {}
                tempList2 = {}
                tempStudent = ""
                studentName2 = ""
                # Find a student from a number and assign its subject to the tempStudent variable
                for row in reader:
                    if (nameinput == row[2]):
                        tempStudent = row[3]
                        studentName2 = row[0] + " " + row[1]
                    else:
                        answer1.set("--> Student Not Found")
                        break
                # Here it gets more complex. We earlier created a temporary dict.
                # Now we iterate through the csv of tutor, and if the tutor's subject matches the student's
                # we add the tutor's full name and quota number to the dict.
                for row in tutorReader:
                    if tempStudent == row[3]:
                        tempList[row[0] + " " + row[1]] = row[4]

                # Run function using list we made, then get the result. If tutor is found, we return the tutor name,
                # else it fails and we re-run it with a list of tutors who's subject isn't the same as the student's.
                result = assignTutor(tempList, studentName2, tempStudent)
                if result:
                    print("success") # Here we would call the write to csv function, like writeToCSV(result)
                else:
                    # When CSV is read, the cursor is left at the end of the file. So we have to seek back to the start to search again.
                    tutorscsv.seek(0)
                    for row in tutorReader:
                        if tempStudent != row[3]:
                            tempList2[row[0] + " " + row[1]] = row[4]
                    # Second running
                    result2 = assignTutor(tempList2, studentName2, tempStudent)
                    if result2:
                        print("not fully, but still success") # Once again write the result
                    else:
                        print("Failed!") # Final fail state

def returnTutor(*args):
    with open('MOCK_DATA.csv') as csvfile:
        reader = csv.reader(csvfile)

        nameinput = str(tutorName.get())

        action = comboValueTutor.get()

        # Getting info for tutor's srudents
        if action == "Get Info":
            # Initialise variables
            tempStudents = []

            emptyString = ""

            for row in reader:
                # As the tutor name is all one word, first and last, we split into 2 for sake of easy searching
                nameSplit = row[4].split(" ")

                # Check stuff
                if nameinput == "":
                    answer2.set("--> " + "Tutor not found/has no students.")
                elif (nameinput.lower() == str(nameSplit[0]).lower()) or (nameinput.lower() == str(nameSplit[1]).lower()) or (nameinput.lower() == row[4]):
                    # Append to empty list a string of the students name nicely formatted
                    tempStudents.append(row[0] + " " + row[1])
                else:
                    answer2.set("--> " + "Tutor not found/has no students.")

            # We like nice formatting, so if there's only 1 student, correct grammar is used.
            if len(tempStudents) == 1:
                # For each student in list, add to a string for printing
                for i in tempStudents:
                    emptyString += i
                # Message boxes for easy to read information
                messagebox.showinfo("Tutor Info", "Tutor has following Student: \n" + emptyString)
            elif len(tempStudents) > 1:
                # In order to correctly format commas, we take instances for number of iterations
                instances = 0
                for i in tempStudents:
                    # Checks if it's the last name, and if so don't put a comma
                    if instances == (len(tempStudents) - 1):
                        emptyString += (i + "\n")
                    else:
                        emptyString += (i + ", \n")
                    instances += 1
                messagebox.showinfo("Tutor Info", "Tutor has following Students: \n" + emptyString)

def write_tutor(student_row_number, tutor_name):
    r = csv.reader(open('MOCK_DATA.csv')) # open csv file
    lines = [l for l in r]
    lines[student_row_number][4] = tutor_name
     
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

ttk.Label(mainframe, textvariable=answer1).grid(column=2, row=2)
#ttk.Button(mainframe, text="Calculate Surname", command=returnStudent).grid(column=1, row=2, sticky=W)

studentCombo = ttk.Combobox(mainframe, textvariable=comboValue, state='readonly')
studentCombo.bind("<<ComboboxSelected>>", returnStudent)
studentCombo['values'] = ('Get Info', 'Assign Student', 'Reassign Student', 'Delete Student')
studentCombo.current(0)
studentCombo.grid(column=1, row=2, sticky=W)

ttk.Label(mainframe, text="Please Input Student Name/Number: ").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="Please Input Tutor Name/Number: ").grid(column=1, row=3, sticky=W)

ttk.Label(mainframe, textvariable=answer2).grid(column=2, row=4)
#ttk.Button(mainframe, text="Calculate Number/Name", command=returnNumber).grid(column=1, row=4, sticky=W)

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
