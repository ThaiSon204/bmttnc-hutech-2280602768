input_str = input("Nhap X, Y :")
dimensisons = [int(x) for x in input_str.split(',')]
rowNum = dimensisons[0]
colNum = dimensisons[1]
multilist = [[0 for col in range(colNum)] for row in range(rowNum)]
for row in range(rowNum):
    for col in range(colNum):
        multilist[row][col]= row*col  
print(multilist)