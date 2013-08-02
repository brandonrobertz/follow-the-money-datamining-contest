#!/bin/bash
#echo Remove First Line
#sed -i '1d' $1 

echo "[*] Escape Backslashes"
sed -i 's/\\/\//g' $1 

echo "[*] Escape Commas"
sed -i 's/\([A-Za-z0-9]\),/\1\\,/g' $1

echo "[*] Remove All \xA0"
cat $1 | tr '\240' ' ' > $1.tmp

echo "[*] Remove All \x1A"
cat $1.tmp | tr -d '\032' > $1

echo "[*] Finishing up"
rm $1.tmp

echo "[*] Done!"
