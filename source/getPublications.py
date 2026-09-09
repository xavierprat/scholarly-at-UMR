#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 14:48:07 2020

@author: xavier

May 24 2022:
currently works with scholarly 1.6 in python3.9

conda create --name scholar python=3.9
conda activate scholar
conda install -c conda-forge scholarly
conda install -c conda-forge jsonpickle
"""

from scholarly import scholarly
from scholarly import *
#scholarly builds a pickle that cannot be turned into json right a way, so Ill write it into a pickle text that on the browser will be used as
import jsonpickle
import json
import os
import sys
import time
import random

#from scholarly import ProxyGenerator
#pg = ProxyGenerator()
#pg.FreeProxies()
#pg.Tor_Internal()
#scholarly.use_proxy(pg)

#path = "/Users/xavier/Gd/Service/Scholarly"
#os.chdir(path)


# Retrieve the author's data, fill-in, and print

faculty = [
   ["Bijaya Aryal","xLrK_rQAAAAJ",         "B Aryal;B. Aryal"],
   ["Abraham Ayebo","nw1yBdUAAAAJ",        "A Ayebo"],
   ["Amy Collins","8egZNOMAAAAJ", 	"AE Collins-Warfield;A Collins-Warfield;Amy E Collins-Warfield;Amy Collins-Warfield;A Collins;Amy E Collins"],
   ["Olivia Crandell","nY0udHMAAAAJ", 		"Olivia Crandell;OM Crandell;Olivia M. Crandell;Olivia Marie Crandell;Olivia M Crandell"],
   ["Cate Denial","spufJKkAAAAJ",         "Catherine Denial;Catherine J Denial;C.J. Denial"],
   ["Molly Dingel","-6iHfAcAAAAJ",         "M Dingel;Molly J Dingel"],
   ["Tim Doherty","bz1A2PAAAAAJ",         "Tim Doherty;Tim F Doherty"],
   ["Elizabeth Dunens","S7o0B6QAAAAJ", "E Dunens;E. Dunens;Elizabeth Dunens"],
   ["Alexander Eden","Ae03qroAAAAJ",         "A Eden;Alexander Eden"],
   ["Robert M. Erdmann","BMnhiyAAAAAJ",	"RM Erdmann;R Erdmann;Robert Erdmann;Robert M Erdmann"],
   ["Connor Ferguson","fAavXVcAAAAJ",	"Connor L Ferguson;Connor L. Ferguson;Connor Ferguson;C.L. Ferguson;CL Ferguson;Connor Lynn Ferguson"],
   ["Casandra Koevoets-Beach","uuDgG7UAAAAJ",	"Casandra Koevoets-Beach;C Koevoets-Beach;C. Koevoets-Beach"],
   ["Kelsey Metzger","_oJQvj0AAAAJ",       "Kelsey J Metzger;K Metzger;Kelsey Jean Metzger"],
   ["Marcia D Nichols","hy6FBKgAAAAJ",     "Marcia Nichols;M.D Nichols"],
   ["Xavier Prat-Resina","b0fbol0AAAAJ",   "Xavier Prat;X Prat-Resina;Xavier Prat Resina"],
   ["Andrew Petzold","wZWv8KYAAAAJ",       "Andrew M Petzold;Andrew Michael Petzold;AM Petzold"],
   ["Cassidy R. Terrell","NDYTevUAAAAJ",   "Cassidy Terrell;Cassidy R Terrell;C Terrell;Cassidy Renee Terrell"],
   ["Sarah Collier Villaume","VlBrdScAAAAJ",          	"S Collier Villaume;SC Villaume;Sarah Collier;S. Collier Villaume"],
   ["Jake Wright","jtONKUUAAAAJ",          	"J Wright"]

    ]

onlyWriteAuthorFile = False

#
def polite_sleep(low=5, high=12, label="request"):
    seconds = random.uniform(low, high)
    print(f"Sleeping {seconds:.1f} s before {label}...")
    time.sleep(seconds)

# Display the list
print("Select faculty members by number (comma-separated):")
for i, f in enumerate(faculty, 1):
    print(f"{i}: {f[0]}")
print("99: All faculty")
print("0: None")

# Get user input
selection = input("Enter numbers (e.g., 1,3,5 or 99 for all, 0 for none): ")

try:
    selection = selection.strip()
    if selection == "99":
        selected_faculty = faculty  # all
    elif selection == "0":
        onlyWriteAuthorFile = True
        selected_faculty = []  # none
    else:
        selected_indices = [int(x.strip()) - 1 for x in selection.split(",")]
        selected_faculty = [faculty[i] for i in selected_indices if 0 <= i < len(faculty)]

    print("\nYou selected:")
    if selected_faculty:
        for f in selected_faculty:
            print(f[0])
    else:
        print("No faculty selected.")
except Exception as e:
    print(f"Error in selection: {e}")




#Author file
authorFile = open("authors.txt","w")

for item in faculty:
    authName = item[0]
    authID = item[1]
    #write author file for alternative spellings
    authorFile.write(";".join(item)+"\n")
authorFile.close()

print(faculty)
print(selected_faculty)

#sys.exit()

allPubs = []
onlyPubs = []

for item in selected_faculty:
    authName = item[0]
    authID = item[1]

    print("searching ", authID)

    polite_sleep(8, 18, "author query")
    search_query = scholarly.search_author_id(authID)
    author = scholarly.fill(search_query, sections=['publications'])

    count = 0
    bibEntry = ""

    for pubindex in range(len(author["publications"])):
        try:
            polite_sleep(4, 10, f"publication {pubindex+1}")
            pub = scholarly.fill(author["publications"][pubindex])

        except Exception as e:
            print(f"Failed publication {pubindex+1}: {e}")
            continue

        onlyPubs.append(pub["bib"])
        print(pub["bib"])

        if (pubindex + 1) % 10 == 0:
            polite_sleep(30, 90, "long cooldown")

        #the bibtex module doesnt work ,we can do it manually
        #create a new bibtex entry
        bibEntry += "@article{"+authName.replace(" ","")+str(count)+",\n"
        count +=1
        for key in pub["bib"]:
            v = pub["bib"][key]
            if key == "abstract":
                v = v.replace("\"","").replace("'","'")
            bibEntry += key+" = {"+str(v)+"},\n"
        #remove last character from string
        bibEntry = bibEntry[:-2]
        bibEntry += "\n}\n\n"
    #write bibtex for each author
    with open(authName+".bibtex","w",encoding="utf-8") as f:
        f.write(bibEntry)
    #allPubs[auth] = author
    allPubs.append(author)
    frozen = jsonpickle.encode(author)
    with open(authName+".txt","w",encoding="utf-8") as f:
        f.write(str(author))
    with open(authName+".json","w",encoding="utf-8") as f:
        json.dump(frozen,f)



# Writing to sample.json
#json_object = json.dumps(onlyPubs,indent=2)
#with open("allPubs.json", "w",encoding="utf-8") as outfile:
#    outfile.write(json_object)
