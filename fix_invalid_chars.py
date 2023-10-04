import csv

with open('data.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for c in row[1]:
            if 768 <= ord(c) <= 879:
                print(';'.join(row + [str(' ' + c), str(ord(c))]))
