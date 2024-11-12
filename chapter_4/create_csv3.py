import csv

data = [
    ("icecream", 15, ""),
    ("water", 3.2, "it was hot day, no"),
    ("bread", 1.3, "my favorite one"),
]

output_filename = "output_file.csv"
headers = [("name", "amount", "comment")]

with open(output_filename, "w") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=",", quotechar='"')
    csv_writer.writerows(headers)
    csv_writer.writerows(data)
