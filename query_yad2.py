import urllib.request
import json

__author__ = 'Lior'
#


def start():

    #add &Page=2
        full_url = 'http://www.yad2.co.il/Nadlan/rent.php?AreaID=1&City=&HomeTypeID=&fromRooms=&untilRooms=&fromPrice=&untilPrice=&PriceType=1&FromFloor=&ToFloor=&EnterDate=&Info=&PriceOnly=1'
        txt = urllib.request.urlopen(full_url).read()
        ur = txt.decode('utf8')











if __name__=="__main__":
     """
The guy who wrote Padmapper says this tool puts a pretty heavy load on his server and he
would rather it was run no more than once a month.  If you're just looking for some
apartment data, I've put some in apts-2013-01-29, which is for Boston in January 2013.
"""
     start()

     """
Ones labeled $6000 in the output file are really $6000+.  You can fix them manually
by going to https://www.padmapper.com/show.php?type=0&id=[ID]&src=main for each one (the
id is the third output column) and looking at what it says there.

You probably also want to look over expensive '0 bedroom' apartments to check that none
are commercial listings.
"""
