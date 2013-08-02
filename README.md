Follow the Money Datamining Contest Entry
=========================================

This was my entry to the CIR/IRE's Kaggle "follow the money" datamining contest. This code is messy, and was written in ten days. It works, but prepare for your eyes to bleed after seeing the raw number of hacks. Here are instructions on how to use this hot mess:

## Compiling data on contributors:

1) Edit the files for your system. Breakdown.py (the version included here is out of date, but supports the ARFF file format ... a more up to date, CSV-based version of this code can be found at https://github.com/brandonrobertz/FECAnalysisTools), in particular needs to be filled in with your DB information. The shell scripts need paths.

2) Pull your candidate / contributor data from DB. This assume you're using a DB formatted like the FEC Campaign Finance CSV files. breakdown.py will convert it into a WEKA readable ARFF (use "-f" aka "--arff") 

    # This particular example is outputting all of Al Franken's contributors, grouped by occupation 
    ./breakdown.py -o -f -v "Franken, Al" out.arff

    # This will output all contributors to all candidates into an arff file.
    ./ breakdown.py -f -v all allCandidates.arff

    # This is literally a hack (SQL injection, I was running out of time here), but you can do multiple candidates in a competing race (and whether they won/lost) the following way:
    ./breakdown.py -f -v -w 'Franken, Al" or candidate_name="Coleman, Norm' franken.coleman.2008.contributors.arff

3) Convert the outputted string fields in out.arff to a numeric format. transform.py will do this. You can edit the file to change where your WEKA install is & options.

    ./transform.sh out.arff o.nom.arff

4) Now what we have in o.nom.arff is a long list of contributors with word frequencies for each. What we need is one, combined word frequency instance for each candidate. combiner.py will do this.

    ./combiner.py o.nom.arff o.comb.arff

What this leaves you with is an ARFF file with each instance representing every candidate's contributor word frequencies. 

## Converting a particular candidate's Senate votes to arff:

1) Luckily this tool does all the work for you (again, a more up to date, cleaner CSV-based version of this code can be found at https://github.com/brandonrobertz/SenateVotingRecord2CSV)

    ./senatevotes2arff.py First Last 111 1 ./senate_xml/ SenatorFirstLastSenateVotesSenate111Session1.arff
