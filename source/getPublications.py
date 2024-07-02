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
   ["Amy Collins-Warfield","8egZNOMAAAAJ", 	"AE Collins-Warfield;A Collins-Warfield;Amy E Collins-Warfield"],
   ["Olivia Crandell","nY0udHMAAAAJ", 		"Olivia Crandell;OM Crandell;Olivia M. Crandell;Olivia Marie Crandell;Olivia M Crandell"],
   ["Molly Dingel","-6iHfAcAAAAJ",         "M Dingel;Molly J Dingel"],
   ["Tim Doherty","bz1A2PAAAAAJ",         "Tim Doherty;Tim F Doherty"],
   ["Robert M. Erdmann","BMnhiyAAAAAJ",	"RM Erdmann;R Erdmann;Robert Erdmann;Robert M Erdmann"],
   ["Kelsey Metzger","_oJQvj0AAAAJ",       "Kelsey J Metzger;K Metzger;Kelsey Jean Metzger"],
   ["Marcia D Nichols","hy6FBKgAAAAJ",     "Marcia Nichols;M.D Nichols"],
   ["Xavier Prat-Resina","b0fbol0AAAAJ",   "Xavier Prat;X Prat-Resina;Xavier Prat Resina"],
   ["Andrew Petzold","wZWv8KYAAAAJ",       "Andrew M Petzold;Andrew Michael Petzold;AM Petzold"],
   ["Cassidy R. Terrell","NDYTevUAAAAJ",   "Cassidy Terrell;Cassidy R Terrell;C Terrell;Cassidy Renee Terrell"],
   ["Jake Wright","jtONKUUAAAAJ",          	"J Wright"]

    ]


#with open("authorId.txt","w") as f:
    #f.write(str(faculty))
#    json.dump(faculty,f)

allPubs = []
onlyPubs = []
authorFile = open("authors.txt","w")
for item in faculty:
    authName = item[0]
    authID = item[1]
    #write author file for alternative spellings
    authorFile.write(";".join(item)+"\n")
    #continue
    #search_query = scholarly.search_author(auth)
    #author = next(search_query).fill()
    print("searching ", authID)
    search_query = scholarly.search_author_id(authID)
    #author = search_query.fill()
    #author2 = next(search_query)
    author = scholarly.fill(search_query, sections=['publications'])
    #scholarly.pprint(author)
    count = 0
    bibEntry = ""
    for pubindex in range(len(author["publications"])):
        try:
            #lets get more info for each publication
            #pub.fill()
            pub = scholarly.fill(author["publications"][pubindex])
        except:
            a=1
        onlyPubs.append(pub["bib"])
        print(pub["bib"])

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


authorFile.close()

# Writing to sample.json
json_object = json.dumps(onlyPubs,indent=2)
with open("allPubs.json", "w",encoding="utf-8") as outfile:
    outfile.write(json_object)
