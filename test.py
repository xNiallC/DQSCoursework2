import csv

with open('test.csv') as csvfile:
    reader = csv.reader(csvfile)

    nameinput = "Jim"

    for row in reader:
        print(row[0])
        if nameinput == row[0]:
            print(row[1])
