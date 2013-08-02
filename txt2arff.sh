#!/bin/bash

# Turn a directory of files ($1, argument 1) into an ARFF file (argument 2, $2)

#convert txt files into a DB format 
find $1 -iname "*.txt" | xargs -i python ./txt2arff_helper.py {} txt.tmp.db

#strip case
echo "Converting to Lowercase"
dd if=txt.tmp.db of=txt.tmp.db.lc conv=lcase
rm -f txt.tmp.db
 
#add arff format header then save as arff
echo "Building ARFF header"
echo "@relation txt_string" > header.tmp
echo "@attribute txt_name string" >> header.tmp
echo "@attribute txt_body string" >> header.tmp
echo "@data" >> header.tmp

echo "Finishing ARFF file"
cat txt.tmp.db.lc >> header.tmp

mv -v header.tmp $2.arff
rm -f txt.tmp.db.lc

echo "Done!"
