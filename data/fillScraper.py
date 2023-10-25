import csv

filename = "SandPDictionary.csv"

fields = []
rows = []

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    fields = next(csvreader)

    for row in csvreader:
        rows.append(row[0])

    print(rows)