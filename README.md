# smartplot
plot S.M.A.R.T. HDD data

You need to supply a attrlog-CSV file.

Project homepage: https://f00l.de/smartplot/  
Online Version: https://f00l.de/hacking/smartplot.php

For examples see /examples/  
It looks like:  
![Analysis of Temperature_Celsius to check for potential temperature problems.](https://github.com/Rup0rt/smartplot/blob/master/examples/temperature.png?raw=true "Analysis of Temperature_Celsius to check for potential temperature problems.")

### Help output

smartplot v1.1 (c) 2019 Robert Krause  

Usage: smartplot.py [options] <inputfile>  

Options:  
  -h, --help  show this help message and exit  
  -o FILE, --output=FILE write report to FILE  
  -f format, --format=format choose output format (PDF or PNG)  
  -e DATE, --event=DATE mark event in graphs (format: DD.MM.YYYY-HH:MM  
  -d DAYS, --days=DAYS only handle last days until today  
  -s, --seagate interpret values with seagate calculation  
