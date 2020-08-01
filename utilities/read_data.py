import csv


def get_csv_data(file_name):
    rows = []
    data_file = open(file_name, 'r')
    reader = csv.reader(data_file)
    next(reader)
    for row in reader:
        rows.append(row)
    return rows


