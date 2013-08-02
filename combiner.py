#!/usr/bin/python

import sys
import argparse
import string
from collections import defaultdict
import operator


parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description="This program reads politician data from an ARFF file and adds all nominal values together")
parser.add_argument("-v", "--verbose", action="store_true", help="output more stuff, not good is you're piping to disk", default=0)
parser.add_argument("infile", type=str, help="ARFF file to read")
parser.add_argument("outfile", type=str, help="output file")
args = parser.parse_args()


#open our file
fileIN = open(args.infile, "r")
#print "test"
#fileIN = open("candidate_occupation.nominal.arff", "r")
line = fileIN.readline()

i = []
n = 0
header = ''

while line:
  #we have an instance line
  if line[0] == "{":
    line = line.replace("{", "").replace("}","")
    vals = string.split(line, ",")

    # Run through all values in this line and create a list of them
    l = []
    for val in vals:
      #split into num & value
      s = string.split(val, " ")
      s[0]=int(s[0].rstrip("\n"))
      s[1]=s[1].rstrip("\n")
      l.append(s)
    if args.verbose: print l

    # Do we have to create a (new or first) line?
    f = True
    try:
      len(i[n])
      f = False
    except IndexError:
      # It's our first
      i.append(l)

    # Not our first. Is it same as old?
    if not f:
      if i[n][0][1] == l[0][1]:
        # Same, so add number values to old line
        if args.verbose: print "Same"

        # Any new lines to add?
        for v in l:
          matched = False
          for ii in i[n]:
            if ii[0] == v[0]:
              matched = True
          if not matched:
            i[n].append(v)


        # Go through values in this line and add them to old
        #tmp = i[n]
        for ii in i[n]:
          matched = False
          nn=0
          for v in l:
            matched = False
            # Can we add them?
            if v[1].isdigit():
              # Are they the same?
              if ii[0] == v[0]:
                if args.verbose: print "Match"
                if args.verbose: print "i[%s][%s] %s"%(n,nn,i[n][nn])
                if args.verbose: print "v: ",v
                if args.verbose: print "ii: ",ii
                ii[1] = str(float(ii[1]) + float(v[1]))
                if args.verbose: print "after ",i[n][nn][1]
                if args.verbose: print i[n]
            nn=nn+1
            
      else:
        # New line, increment and add it
        if args.verbose: print "Old"
        i.append(l)
        n=n+1

    if args.verbose: print "i[n]: ",i[n]
  elif line[0] == "@" or line[0] == "%":
    header = header+line
  # nxt ln
  line = fileIN.readline()

fileIN.close()
fileOUT = open(args.outfile, "w")
#fileOUT = open("comb.out", "w")
#if args.verbose: print "Finished processing, now outputting..."

fileOUT.write(header)

def score(item): # define a score function for your list items
  return item[0]

for ii in i:
  ii = sorted(ii, key=lambda x: x[0]) #operator.itemgetter(0,1))
  print ii
  first = True
  fileOUT.write("{")
  for iii in ii:
    if first:
      c = ""
      first = False
    else:
      c = ","
    o = "%s%s %s" %(c,iii[0],iii[1])
    fileOUT.write(o)
  fileOUT.write("}\n")
fileOUT.close()
#if args.verbose: print "Done!"
