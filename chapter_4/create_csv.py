import csv

data = [
    {"name": "icecream", "amount": 15, "comment": ""},
    {"name": "water", "amount": 3.2, "comment": "it was hot day"},
    {"name": "bread", "amount": 1.3, "comment": "my favorite one"},
]

output_filename = "output_file.csv"
headers = ("name", "amount", "comment")

with open(output_filename, "w") as csv_file:
    csv_writer = csv.writer(csv_file)
    for item in data:
        csv_writer.writerow([item.get(key) for key in headers])
