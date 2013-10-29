patent_scraper
==============

Sean Lahman / seanlahman@gmail.com / 10-29-2013

Script to retrieve list of patents from inventors from a given city or list of cities. Scrapes conten from searchable
database at website for US Patent & Trademark website. Script is used to build and maintain an online listing
of patents issued to inventors from Monroe County, NY - http://rocdocs.democratandchronicle.com/patents


get_index.py - reads list of cities from citylist.csv and retrieves an index of patents that have been issued
     to inventors in those cities. Output is "newindex.csv" and contains  patent number and patent title. 
     Currently, the state is hardcoded, and search is limited to a specific time range.  These can be changed 
     manually in the code.  Future versions will handle differently. Search syntax at USPTO website is non-standard,
     so constructing queries is complicated.

     
newscrape.py - if additional patent information is desired, this reads the list created by script above and
     retrieves name of inventors, patent assignee (owner), and the date the patent was issued. 
     
     
lahmanlib.py - library which contains module for scraping and parsring infor from USPTO website. They 
     use some unusual HTML formatting, so this is hard to do with standard Beautiful Soup coding. Requires
     updates anytime the USPTO folks monkey with their site.  Ugly spaghetti code that somehow works.
     
     
citylist.csv - list of cities used by get_index.py     


