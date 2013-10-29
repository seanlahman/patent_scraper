#
# get_index_updates.py
#    2012-09-30     Sean Lahman / seanlahman@gmail.com
#
# This script reads a list of cities and creates a list of
#   patents that have been issued to inventors from each.
#   Done by querying the USPTO website.
#
# Script requires file "citylist.csv" to execute
#
#   Based very loosely on code developed by Greg Jurman
#   at FOSS@RIT - http://foss.rit.edu/
#   http://github.com/FOSSRIT/uspto-scrape
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import urllib2
from bs4 import BeautifulSoup # For processing HTML
import csv
import math
import os
import re
import datetime

#lib_path="C:\Users\slahman\Dropbox\D&C\projects\python\sl-work\2013-07-19\""
lib_path=""
nuke_lines = (lambda w: ' '.join([x.strip() for x in w.strip().splitlines()]))

#declare variables
citylistfile=lib_path + "citylist.csv"
sState = "ny"
sOutfile=lib_path + "newindex-raw.csv"
sFinalfile=lib_path + "newindex.csv"
targetdate="+and+isd%2F20130101->20131231"   # this is harcoded to get current year
errorlogfile=lib_path + "errorlog.csv"


if __name__ == "__main__":

        #SL Sep 2012 -- here we go
        print "----------------------------------------"
        if os.path.exists(sOutfile):
          os.remove(sOutfile)
          print "overwriting existing file"

        print "----------------------------------------"
        print "Reading list of cities from:",citylistfile

        ifile  = open(citylistfile, "rb")
        reader = csv.reader(ifile)

        #get list of cities from file
        city_list = []
        city_list.extend(reader)
        lCities = []
        for data in city_list:
            lCities.append(data[0])
        print "List of cities has been read..."
        print "----------------------------------------"
        print ""
        print "Starting at:",
        print str(datetime.datetime.now())



        #get list of patents for each city in the list
        for item in lCities:
            sCity= item

            #set URLs
            counturl= "http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&p=1&f=S&l=50&Query=ic%2F"+sCity+"+and+is%2F"+sState+targetdate+"&d=PTXT"

            # get total number of patents (this is incredibly ugly but it works)
            page = urllib2.urlopen(counturl)
            soup = BeautifulSoup(page)

            #handle if search returns nothing or single page returned
            SingleDocFound=str(soup).find("Single Document")
            NoneFound=str(soup).find("No patents have matched your query")

            if NoneFound > 0:
               print "none found"
               maxpages=0
               iPatentCount=0

            elif SingleDocFound > 0:
               print "Single Doc Found - skipping"
               maxpages=0
               iPatentCount=0
               #write to errorlog
               err_string=sCity +",Single Doc Found,"+ str(datetime.datetime.now())+"\n"
               log_file = open(errorlogfile, "a")
               log_file.write(err_string)
               log_file.close()


            else:
               #results returned, proceed
               print "list received"
               iPatentCount=int((soup.html.body.findAll('strong')[2]).string)
               maxpages=int((iPatentCount-1)/50)+1        # (IP-1) is to handle if count is divisible by 50


            # index_search_page
            with open(sOutfile, 'ab') as csv_index_out_file:
              csv_out = csv.writer(csv_index_out_file, quoting=csv.QUOTE_MINIMAL)

              p_count = 0
              patent_id_list = []

              print "----------------------------------------"
              print "Starting: ", sCity
              print maxpages,"pages /",iPatentCount,"patents"
              print "-------------------------"

              #print headers for CSV file
              #csv_out.writerow(["Town","Count", "Patent inNo.", "Title"])

              # go through each page of list and pull info
              for i in range(0, maxpages):
                getpage=str(i+1)     #they start count from one, we star from zero. also convert to string

                #url = baseurl.format(0, (i*50)+1) # r is result (0 is result page)
                #note, URL scheme from RIT (above) works only up to 12,000 patents. URL below is universal
                url="http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&f=S&l=50&d=PTXT&s1=(("+sCity+".INCI.)+AND+("+sState+".INST.))&p="+getpage+"&Page=Next&OS=ic/"+sCity+"+and+is/"+sState+"&RS=((IC/"+sCity+")+AND+IS/"+sState+")"

                page = urllib2.urlopen(url)
                soup = BeautifulSoup(page)

                patent_table = soup.html.body.findAll('table')[1]
                patent_rows = patent_table.findAll('tr')[1:] # Skip first row (header)

                for row in patent_rows:
                    row_td = row.findAll('td')
                    row_id = row_td[0].string
                    patent_url = row_td[1].a['href']
                    patent_id = row_td[1].a.string.strip()
                    patent_id_list.append(patent_id)
                    patent_title = row_td[3].a.string
                    patent_title = nuke_lines(patent_title)
                    csv_out.writerow([row_id.strip(), patent_id.strip(), patent_title,sCity])

                print "Logged page {0}, {1} patents indexed.".format(i, len(patent_rows))
                p_count = p_count + len(patent_rows)


              # done, let user know
              print "-----"
              print "Indexing completed, {0} patents indexed.".format(p_count)
              print "----------------------------------------"


        print "Done reading all the cities"
        print "Ended at:",
        print str(datetime.datetime.now())



        #remove duplicates from master list
        #   because a patent might have an inventor from Greece and another from Webster

        fIn=sOutfile
        fOut=sFinalfile
        compare_row=1


        print "Starting to de-deupe full file at:",
        print str(datetime.datetime.now())

        f1 = csv.reader(open(fIn, 'rb'))
        writer = csv.writer(open(fOut, "wb"))
        lPatents = set()

        for row in f1:
            if row[compare_row] not in lPatents:
                writer.writerow(row)
                lPatents.add( row[compare_row] )



        print "all done, slick"
        print "Done at:",
        print str(datetime.datetime.now())





