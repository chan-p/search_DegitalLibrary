dic = {}
with open('../src/ver1/PDF_list_column.txt') as g:
	for lines in g:
		line = lines[:-1].split(',')
		for cate in line[1:]:
			if cate not in dic:
				dic[cate] = []
			dic[cate].append(line[0])

with open('../src/ver1/cate_search.txt', 'w') as g:
	for i, v in dic.items():
		g.write(i)
		for ca in v:
			g.write(',' + ca)
		g.write('\n')
