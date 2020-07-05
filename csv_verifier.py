import pandas as pd

#df = pd.read_csv("color_emotion.csv", delimiter="\t")
df = pd.read_csv("color_emotion-sem-grandes-7.csv", delimiter="\t")

print("Checking H...")

for i in range(0, 360):

	a = (i >= df["h_s"]) & (i <= df["h_e"])	

	if not a.any():    	
		print(str(i) + " is not in CSV")


    # for index, row in df.iterrows():
    #     if (i >= row["h_s"]) and (i <= row["h_e"]):
    #         z = 1
    #         break
    # if z == 0:
    #     print(str(i) + " is not in CSV")


print("Checking HSV...")

z_list = []

for h in range(0, 360):
	print("H:",str(h))
	for s in range(0, 100):
		for v in range(0, 100):
			a = ((h >= df["h_s"])  & (h <= df["h_e"])) \
            	& ((s >= df["s_s"]) & (s <= df["s_e"])) \
            	& ((v >= df["v_s"]) & (v <= df["v_e"]))
			
			if not a.any():
				z_list.append("{},{},{} is not in CSV \n".format(str(h),str(s),str(v)))

print(z_list)

# for h in range(0, 360):
#     for s in range(0, 100):
#         for v in range(0, 100):
#             z = 0
#             for index, row in df.iterrows():
#                 if ((h >= row["h_s"]) and (h <= row["h_e"])) \
#                         and ((s >= row["s_s"]) and (s <= row["s_e"])) \
#                         and ((v >= row["v_s"]) and (v <= row["v_e"])):
#                     z = 1
#                     break
#             if z == 0:
#                 z_list.append("{},{},{} is not in CSV \n".format(str(h),str(s),str(v)))

# print(z_list)