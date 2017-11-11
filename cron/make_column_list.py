g = open('../src/ver1/column_list.txt', 'w')
column_list = []
with open('../src/ver1/PDF_list_column.txt') as f:
	for lines in f:
		line = lines[:-1].split(',')
		for co in line[1:]:
			if co not in column_list:
				column_list.append(co)

for ii in column_list:
	g.write(ii + '\n')
g.close()
