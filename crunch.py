import json

row_dicts=None

####CHANGE YEAR
with open("2018.json") as fi:
	row_dicts=json.load(fi)

if not row_dicts:
	exit()

#Columns :['Round No', 'Institute', 'Academic Program Name', 'Quota', 'Category', 'Gender', 'Opening Rank', 'Closing Rank']

####SEARCH/FILTER PARAMETERS
# Leave a value ="" for undefined string, -1 for undefined numbers
min_closing_rank=0
max_closing_rank=2000

quota="AI"#All India
cat="General"
gender=""
# gender="Female-only (including Supernumerary)"
# gender="NA" #for 2016 & 2018
insti=""#all institutes
##################


matches=[]
for row in row_dicts:
	if quota and row["Quota"]!=quota:
		continue
	if cat and row["Category"]!=cat:
		continue
	if gender and row["Gender"]!=gender:
		continue
	if insti and row["Institute"]!=insti:
		continue
	if min_closing_rank>0 and row["Closing Rank"]<min_closing_rank:
		continue
	if max_closing_rank>0 and row["Closing Rank"]>max_closing_rank:
		continue
	
	matches.append(row)

num_matches = len(matches)
print("Number of matches : "+str(num_matches))

######CHANGE SORTING KEY
def sort_closing(val):
	return val["Closing Rank"]

matches.sort(key=sort_closing)
string=""
for key in row:
	if key in ["Round No","Quota","Category","Gender"]:
		continue
	string+=key+" || "

print("HEADERS")
print("#"*30)
print(string)
print("#"*30)
for row in matches:
	string=""
	for key in row:
		if key in ["Round No","Quota","Category","Gender"]:
			continue
		if key in ["Institute"]:
			row[key]=row[key].replace("Indian Institute  of Technology","IIT")
		string+=str(row[key])+" || "
	print(string)
print("#"*30)

