with open('relatorio_1.txt') as f:
	lines = f.read().split("', '")

print(lines[0])
#lines = lines.split("', '")

for line in range(0, len(lines)):
	lines[line] = lines[line].replace("is not in CSV \\n","")
	lines[line] = lines[line].replace("['","").replace("'","").replace("]","")
	lines[line] = lines[line].replace(" '","")


part = 0

for item in range(0, len(lines)):
	if item % 10000 == 0:
		part += 1 

	with open('relatorio/relatorio-tranf-'+str(part)+'.txt', "a+") as f:
		f.write("%s\n" % lines[item])