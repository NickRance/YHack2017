import csv, json

numberOfProcedures = 22

with open('./data/OperationPrices.csv', 'r') as inputfp:
    reader = csv.reader(inputfp)
    headers = next(reader)
    procedure = {}
    for p in range(1,numberOfProcedures):
        row = next(reader)
        # print(row)
        procedure[row[0]] = {}
        for i in range(1, len(headers)-1):
            procedure[row[0]] = {**procedure[row[0]], **{headers[i]: row[i]}}
    # print(procedure)
    json.dump(fp=open('operations.json','w'), obj=procedure, indent=4)
