#!/usr/bin/python

INFILE="/home/uzr/Desktop/research/us-campaign-finance/senate2009/vote_111_1_00350.xml"
OFILE="franken.2009.arff"
LAST="Franken"
FIRST="Al"

import sys
import xml.etree.ElementTree as ET
import glob
import os

o = open(OFILE, "w")
header = "\
@RELATION 'SENATE_VOTES'\n\
@ATTRIBUTE VOTE_TXT STRING\n\
@ATTRIBUTE VOTE {Yea,Nay}\n\
@DATA\n"
o.write(header)

f = open(INFILE, "r")
xmlf = f.read()
f.close()

tree = ET.fromstring(xmlf)

# Get votes from this record
text = tree[7].text

last = ""
first= ""
vote = ""

p = False

for member in tree[17]:
  l = member[1].text
  f = member[2].text
  v = member[5].text
  if l.lower() == LAST.lower():
    if f.lower() == FIRST.lower():
      last = l
      first = f
      vote = v
      if p:
        print last, first
        p = True
i = "\"%s\",%s\n"%(text,vote)
o.write(i)

o.close() 
