#!/usr/bin/python
# This tool loads Senate Data directly from the government's website, parses thru the XML files, and converts into a usable ARFF file to be data mined in WEKA. It's classified by Yea or Nay vote and looks at the description of the bill as the string. You'll have to nominalize that yourself either using transform.sh or the WEKA explorer (same thing). by Brandon Roberts 2012 copyleft.
import sys
import subprocess
import argparse
import sys
import xml.etree.ElementTree as ET
import glob
import os
import re

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description="This tool loads Senate Data directly from the government's website, parses thru the XML files, and converts into a usable ARFF file to be data mined in WEKA. It's classified by Yea or Nay vote and looks at the description of the bill as the string. You'll have to nominalize that yourself either using transform.sh or the WEKA explorer (same thing). by Brandon Roberts 2012 copyleft.")
parser.add_argument("first", type=str, help="first name of politician")
parser.add_argument("last", type=str, help="last name of politician")
parser.add_argument("senate", type=str, help="senate ... 111th would be 111")
parser.add_argument("session", type=str, help="1 or 2")
parser.add_argument("dir", type=str, help="directory to write xml files (there will be hundreds of them)")
parser.add_argument("ofile", type=str, help="file to write arff to")
args = parser.parse_args()


SENATE = args.senate
SESSION = args.session
LAST=args.last
FIRST=args.first
OFILE=args.ofile
DIR=args.dir

'''Al Franken 111 1 ../us-campaign-finance/senate2009/ franken.2009.arff
SENATE =111
SESSION = 1
LAST="Franken"
FIRST="Al"
OFILE="franken.2009.arff"
DIR="../us-campaign-finance/senate2009/"
'''

# Get number of bills from internet
URLM="http://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_"+SENATE+"_"+SESSION+".xml"
cmd = "wget -P %s %s"%(DIR, URLM)
print cmd 
try:
  subprocess.check_output(cmd, shell=True)
except:
  print "Couldn't get # of bills."
  sys.exit(1)

MFILE=DIR+"vote_menu_"+SENATE+"_"+SESSION+".xml"
f = open(MFILE, "r")
xmlf0 = f.read()
#print xmlf0
f.close()

tree = ET.fromstring(xmlf0)
TOTAL_BILLS = int(tree[3][0][0].text)

print "Total Bills: %s"%TOTAL_BILLS

os.remove(MFILE)

# Get all senate voting files

for b in range(TOTAL_BILLS):
  b=b+1
  b = str(b).zfill(5) 
  URL="http://www.senate.gov/legislative/LIS/roll_call_votes/vote%s%s/vote_%s_%s_%s.xml"%(SENATE, SESSION, SENATE, SESSION, b)
  # uncomment below and comment below that to overwrite files
  # cmd = "wget -P %s %s"%(DIR, URL)
  cmd = "wget -nc -P %s %s"%(DIR, URL)
  print cmd 
  try:
    subprocess.check_output(cmd, shell=True)
  except:
    print "Bummer on wget."
    sys.exit(1)
  
print "Boom!"

# Process them & make arff

o = open(OFILE, "w")
header = "\
@RELATION 'SENATE_VOTES'\n\
@ATTRIBUTE VOTE_TXT STRING\n\
@ATTRIBUTE VOTE {\"Yea\",\"Nay\"}\n\
@DATA\n"
o.write(header)

os.chdir(DIR)
for INFILE in glob.glob("*.xml"):
  print INFILE

  f = open(INFILE, "r")
  xmlf = f.read()
  f.close()

  tree = ET.fromstring(xmlf)

  # Get votes from this record
  text = tree[7].text
  if text:
    text = re.sub('[^A-Za-z0-9 ]', '', text)

  last = ""
  first= ""
  vote = ""

  p = False
  matched = False

  for member in tree[17]:
    l = member[1].text
    f = member[2].text
    v = member[5].text
    if l.lower() == LAST.lower():
      if f.lower() == FIRST.lower():
        last = l
        first = f
        vote = v
        matched = True
        if p:
          print last, first
        else:
          print text, v
          p = True
  if vote == "Yea" or vote == "Nay":
    i = "\"%s\",\"%s\"\n"%(text ,vote)
    if matched:
      o.write(i)

o.close() 
print "Shucka lucka."
