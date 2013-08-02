#!/bin/bash
export WEKA_DIR="/home/uzr/bin/weka-3-7-7"
export CP="$WEKA_DIR/snowball.jar:$WEKA_DIR/weka.jar:/home/uzr/wekafiles/packages/multiInstanceFilters/multiInstanceFilters.jar"
echo "String to word vector ..."
java -cp $CP -Xmx13000M weka.filters.unsupervised.attribute.StringToWordVector -I -R first-last -C -W 1000 -prune-rate -1.0 -N 0 -L -stemmer weka.core.stemmers.SnowballStemmer -M 1 -S -stopwords ./stop_words.txt -tokenizer "weka.core.tokenizers.WordTokenizer -delimiters \" \\r\\n\\t.,;:\\\'\\\"()?!\"" -i $1 -o $2
#java -cp $CP -Xmx13000M weka.filters.unsupervised.attribute.StringToWordVector -h
#echo "Propositional to Multi ..."
#cp $2 $2.v.tmp
#java -cp $CP -Xmx13000M weka.filters.unsupervised.attribute.PropositionalToMultiInstance -c last -i $1 -o $2
#echo "Cleaning up ..."
#rm -rf $2.tmp
#java -cp $CP -Xmx1500M weka.filters.unsupervised.attribute.PropositionalToMultiInstance -h
