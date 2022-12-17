import csv

with open('dbgwas_data.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='	')

        with open('converted_data.csv', 'w') as new_file:
            csv_writer = csv.writer(new_file, delimiter=' ')
            
            csv_writer.writerow(['ID', 'Phenotype', 'Path'])

            next(csv_reader)

            for line in csv_reader:
                print(line)
                csv_writer.writerow([line[0], round(float(line[1])), "/jj523/individual/{}.fasta".format(line[0])])
