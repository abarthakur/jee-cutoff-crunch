from bs4 import BeautifulSoup
import json

soup=None
with open("2018.html") as fi:
    soup = BeautifulSoup(fi)

table=soup.find_all('table',{"id":"ctl00_ContentPlaceHolder1_GridView1"})
assert(len(table)==1)
table=table[0]
rows=table.find_all('tr')
num_rows=len(rows)
print("Number of rows "+str(num_rows))
header=rows[0]
col_headers=header('th',scope="col")
num_cols=len(col_headers)
print("Number of columns "+str(num_cols))

col_names=[]
for col in col_headers:
	try:
		assert(len(col.contents)==1)
		col_names.append(str(col.contents[0]))
	except Exception as e:
		print(e)
		print("Say what? "+str(col.contents))
		exit()

assert(len(col_names)==num_cols)
print("Columns :"+str(col_names))

row_dicts=[]
problem_rows=set()
for row_idx,row in enumerate(rows[1:]):
	cells=row("td")
	assert(len(cells)==num_cols)
	row_dict={}
	for i,cell in enumerate(cells):
		# print(i,"||",col_names[i],"||",cell)
		if i in [0,1]:
			try:
				assert(len(cell.contents)==1)
				row_dict[col_names[i]]=str(cell.contents[0]).strip()
			except Exception as e:
				print("Exception! "+str(e))
				print("Say what? "+str(cell))
				row_dict[col_names[i]]=""
				problem_rows.add(row_idx)
			continue

		try:
			spans=cell("span")
			assert(len(spans)==1)
			span=spans[0]
			assert(len(span.contents)==1)
			row_dict[col_names[i]]=str(span.contents[0]).strip()
		except Exception as e:
			print("Exception! "+str(e))
			print("Say what? "+str(cell))
			row_dict[col_names[i]]=""
			problem_rows.add(row_idx)
	row_dicts.append(row_dict)

num_problem_rows=len(problem_rows)
print("Number of problem rows :"+str(num_problem_rows))

#Columns :['Round No', 'Institute', 'Academic Program Name', 'Quota', 'Category', 'Gender', 'Opening Rank', 'Closing Rank']
#dtypes :[int,categorical,str,categorical,categorical,categorical,int,int]

problem_rows=set()

rounds=set()
instis=set()
quotas=set()
cats=set()
genders=set()
for idx,row in enumerate(row_dicts):
	try:
		row["Round No"]=int(row["Round No"])
		rounds.add(row["Round No"])

		instis.add(row["Institute"])
		quotas.add(row["Quota"])
		cats.add(row["Category"])
		genders.add(row["Gender"])

		row["Opening Rank"]=int(float(row["Opening Rank"]))
		row["Closing Rank"]=int(float(row["Closing Rank"]))
	except Exception as e:
		print("Exception! "+str(e))
		problem_rows.add(idx)

print("Number of problem rows :"+str(len(problem_rows)))


print("Rounds : "+str(rounds))
print("Institutes : "+str(instis))
print("Quotas : "+str(quotas))
print("Categories : "+str(cats))
print("Genders : "+str(genders))


with open("2018.json","w") as fo:
	json.dump(row_dicts,fo)

