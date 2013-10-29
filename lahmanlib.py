#lahmanlib
#   Collection of modules written by Sean Lahman - seanlahman@gmail.com
#       Created 2013-10-27


def HelloWorld():
    print 'hello world'
        
        
def PatentScrape(p_id):
    # ----------------------------------------------------------------------------
    #  Given the number of a US patent, scrape information about it from 
    #   the USPTO website and return it as a data dictionary
    # ----------------------------------------------------------------------------
    
    #import libraries
    from bs4 import BeautifulSoup # For processing HTML
    import urllib2
    #import sys
    
    #set the URL based on the patent ID passed
    url="http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=1&p=1&f=G&l=50&d=PTXT&S1="+p_id+".PN.&OS=pn/"+p_id+"&RS=PN/"+p_id

    try:
        #get webpage
        downloaded_page = urllib2.urlopen(url)
        soup = BeautifulSoup(downloaded_page)

        #initialize variables
        outdate=''
        outinv=''
        outass='-'      #note, some patents have no assignee, so this state is likely not an error
        
        #page through TD tags to find targeted text
        mylist=soup.find_all('td')
        count=1

        #note: Loop uses length-3 since we are looking for markers to identify subsequent records, we don't want to iterate too far.    
        #      in practice, we could stop after 25-30 or lines, but hardcoding that way could cause problems
        #      if USPTO changes their format in the future
        while (count < (len(mylist)-3)):        
            count = count + 1
            
            #look for markers
            if 'United States Patent' in str(mylist[count]):
                #patdate
                patdate=(mylist[count+3])
                outdate=patdate.find('b').string
                outdate=str(outdate.strip())
                    
            if 'Inventors' in str(mylist[count]):
                patinv=str(mylist[count+1])
                outinv=patinv[patinv.index('90%')+5:-5]
                outinv=outinv.strip()
                outinv=outinv.replace('<b>','')
                outinv=outinv.replace('</b>',' ')
                outinv=outinv.replace(';',', ')
                
            if 'Assignee' in str(mylist[count]):
                patass=str(mylist[count+1])
                outass=patass[patass.index('90%')+5:-15]
                outass=outass.strip()
                outass = "".join(outass.split('\n'))    #strip newlines
                outass=outass.replace('<b>','')
                outass=outass.replace('</b>',' ')
                outass=outass.replace('<br>','')
                outass=outass.replace('<br>','')
                
                #individual inventors have no assignee, so set value to "-"
                if outass=='':
                    outass='-'
                
        #all done, build dictionary and return what we found
        patent_info = {'date' : outdate, 'inventor': outinv, 'assignee': outass}
        return patent_info    

    except:
        #The most rudimentary error handling possible
        print "SL-Unexpected error:", sys.exc_info()[0]
        patent_info = {'date' : "ERR", 'inventor': "ERR", 'assignee': "ERR"}
        return patent_info    
        
