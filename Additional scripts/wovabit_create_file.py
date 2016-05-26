import csv
import re

i = 0

def clean(s):
    return " ".join(re.findall(r'\w+', s, flags = re.UNICODE | re.LOCALE)).lower()

with open("/home/andrew/hse_e.csv", "r") as infile, open("/home/andrew/hse_test_data_v2.vw", "ab") as outfile:
    reader = csv.reader(infile)
    for line in reader:
        i += 1
        vw_line = ""

        #for two modality @author and @text
        vw_line += "title_" + str(i) +" " + "|@author"+" "+str(line[0])+" "+"|"
        vw_line += "@text"+" " + str(line[1]) + " "

        #for one modality @text
        #vw_line += "title_" + str(i) +" " + "|@text"+" " + str(line[0]) + " "#clean(str(line[1]).split(",")[0]).replace(" ", "_") + " "

        print(vw_line)
        outfile.write(vw_line[:-1] + "\n")