import csv

folder = 'datasets/test/'

with open(folder+'train.txt', encoding='utf-8') as txtfile:
    all_text = txtfile.read()
with open(folder+'train.csv', mode='w', encoding='utf-8') as csv_file:
    fieldnames = ['text']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'text': all_text})


with open(folder+'validation.txt', encoding='utf-8') as txtfile:
    all_text = txtfile.read()
with open(folder+'validation.csv', mode='w', encoding='utf-8') as csv_file:
    fieldnames = ['text']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'text': all_text})

print("created train.csv and validation.csv files")


