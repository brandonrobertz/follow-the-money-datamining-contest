#!/bin/bash
# ./pdfs2cleantxt dir_pdfs dir_txt

find  $1 -iname "*.pdf" | xargs -i pdftotext {}
mv -v $1/*.txt $2/
find $2 -iname "*.txt" | xargs -i sed -i 's/[^a-zA-Z0-9 ]//g' {}
find $2 -iname "*.txt" | xargs -I{} sh -c "grep . '{}' | tr '\012' ' ' > '{}.tr'"
find $2 -size 0b | xargs -i rm -fv {}
find $2 -iname "*.txt" | xargs -i rm {}
find $2 "*.tr" | sed 's/.tr//g' | xargs -i mv {}.tr {} 
