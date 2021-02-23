# tunelist
This script accepts a list of urls, applies tuning, &amp; removes redundancies, and outputs the normalized list

Base use from file, (urlsin.txt and tunelist.cfg already configured):
python3 tunelist.py

Interactive mode, supply a list of urls on the fly:
python3 tunelist.py-n <interactive mode>

Specify custome input file and/or config file
python3 tunelist.py -i <filein (Default urlsin.txt)> -c <configfile (Default tunelist.cfg)>

