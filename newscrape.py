# newscrape.py - Sean Lahman / seanlahman@gmail.com
#
# This script reads a list of patent numbers from a file and
#  retrieves information on each one from the USPTO website.
#
# Notes: Need to define sInfile and sOutfile before running 
#
#    2013-10-28     Code rewritten from scratch
#    2012-09-30     Original version based on code developed by Greg Jurman
#                      at FOSS@RIT - http://foss.rit.edu/
#                      http://github.com/FOSSRIT/uspto-scrape
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


import lahmanlib
import csv
import os
import time


# SET FILES TO READ / WRITE
sInfile="newindex.csv"
sOutfile="patents_raw.csv"


if __name__ == "__main__":
    # note start time
    starttime = time.time()

    #start with fresh file
    if os.path.exists(sOutfile):
        os.remove(sOutfile)
        print "Existing output file deleted"
          
    #set file names
    ifile  = open(sInfile, "rb")
    reader = csv.reader(ifile)
    ofile  = open(sOutfile, "wb")
    writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
      
    #calculate and report number of records we'll be getting
    iTotalrows=len(list(csv.reader(open(sInfile)))) 
    print 'patents to process = ',iTotalrows,'\n'
    
    #let's do some scraping
    #initiate counter
    iCurrent=0
    
    #iterate through the data file we read in
    for line in reader:
        p_id=line[1]
        p_title=line[2]

        #do some cleanup - remove commas from patent number
        p_id=p_id.replace(',','')
        
        #TODO - need to handle odd patent types here
        
        #get patent page from USPTO using function from SL Library
        print "Retrieving patent # "+p_id
        patent_info=lahmanlib.PatentScrape(p_id)

        #write to file          
        writer.writerow([p_id, p_title, patent_info['date'], patent_info['inventor'], patent_info['assignee']])

        #display status
        iCurrent=iCurrent+1
        if iCurrent % 5 == 0:
            print "Progress: Have retrieved", iCurrent,"of",iTotalrows

            
    #all done, report status to useer
    endtime=time.time()
    print "\nDone with all patents"
    print "retrieved", iCurrent,"of",iTotalrows
    print 'elapsed time = ',(endtime-starttime), 'seconds'
