# tunelist
This script accepts a list of urls, applies tuning, &amp; removes redundancies, and outputs the normalized list

Base use from file, (urlsin.txt and tunelist.cfg already configured):

_python3 tunelist.py_

Interactive mode, supply a list of urls on the fly:

_python3 tunelist.py -n <interactive mode>_

Specify custome input file and/or config file

_python3 tunelist.py -i <filein (Default urlsin.txt)> -c <configfile (Default tunelist.cfg)>_




Available modes (as configured in tunelist.cfg)
Mode 1 tune by url path only

Mode 2 tune by URL path and query params without values

Mode 3 tune by URL and query with selected navigational values only

Mode 4 tune by all URL paths params and values

