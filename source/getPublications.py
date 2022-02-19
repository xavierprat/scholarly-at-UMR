#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 14:48:07 2020

@author: xavier
"""

from scholarly import scholarly
#scholarly builds a pickle that cannot be turned into json right a way, so Ill write it into a pickle text that on the browser will be used as
import jsonpickle
import json
import os

#path = "/Users/xavier/Gd/Service/Scholarly"
#os.chdir(path)


# Retrieve the author's data, fill-in, and print

faculty = [
    ["Xavier Prat-Resina","b0fbol0AAAAJ",   "Xavier Prat;X Prat-Resina;Xavier Prat Resina"],
    ["Abraham Ayebo","nw1yBdUAAAAJ",        "A Ayebo"],
    ["Marcia D Nichols","hy6FBKgAAAAJ",     "Marcia Nichols;M.D Nichols"],
    ["Andrew Petzold","wZWv8KYAAAAJ",       "Andrew M Petzold;Andrew Michael Petzold;AM Petzold"],
    ["Molly Dingel","-6iHfAcAAAAJ",         "M Dingel;Molly J Dingel"],
    ["Angie Mejia","VucmQHIAAAAJ",          "Angie P Mejia;Angie Pamela Mejia"],
    ["Kelsey Metzger","_oJQvj0AAAAJ",       "Kelsey J Metzger;K Metzger;Kelsey Jean Metzger"],
    ["Cassidy R. Terrell","-mHQBIrrxoMC",   "Cassidy Terrell;Cassidy R Terrell;C Terrell;Cassidy Renee Terrell"],
    ["Bijaya Aryal","xLrK_rQAAAAJ",         "B Aryal"],
    ["Jake Wright","jtONKUUAAAAJ",          "J Wright"]
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
