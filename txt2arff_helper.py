#!/usr/bin/python

import sys, os


if len(sys.argv) < 2:
    sys.exit('Usage: %s database-name' % sys.argv[0])

if not os.path.exists(sys.argv[1]):
    sys.exit('ERROR: Database %s was not found!' % sys.argv[1])

filename = sys.argv[1]
print filename

out_file = sys.argv[2]
print out_file

text_file = open(filename, "rb")
whole_thing = text_file.read()
#print whole_thing
text_file.close()

#whole_thing = whole_thing.rstrip('\r\n')
#whole_thing = whole_thing.rstrip('\r')
#whole_thing = whole_thing.rstrip('\n')
#whole_thing = whole_thing.strip('\x0A')
#whole_thing = whole_thing[:-1]

line = '"'+filename+'","'+whole_thing+'"\n'

ofile = open(out_file, "ab")
ofile.write(line)
ofile.close()
