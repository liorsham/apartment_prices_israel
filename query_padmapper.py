import time
import sys
import urllib.request
import json
import time

# boston
MIN_LAT=42.255594
MAX_LAT=42.4351936
MIN_LON=-71.1828231
MAX_LON=-70.975800

# baltimore
#MAX_LAT=39.388979
#MIN_LON=-76.752548
#MIN_LAT=39.208315
#MAX_LON=-76.464844

# atlanta
#MIN_LAT=33.453214
#MAX_LON=-84.017944
#MAX_LAT=33.934245
#MIN_LON=-84.508209

# bay area from google maps: ll=37.53151,-122.163849&spn=0.634907,1.0849
#MIN_LAT=37.23
#MAX_LON=-121.62
#MAX_LAT=37.83
#MIN_LON=-122.70

# tel aviv
#https://www.google.co.il/maps/@32.0756686,34.7984026,14z
MIN_LAT=31.975742453595963  #southLat
MAX_LAT=32.16688183134553  #northLat
MIN_LON=34.523274442382785  #westLong
MAX_LON=35.017659208007785 #eastLong
#LAT=32.0756686
#LON=34.7984026
#ZOOM=14
#from site:
# http://www.padmapper.com/reloadMarkersJSON.php?eastLong=35.017659208007785&northLat=32.16688183134553&westLong=34.523274442382785&southLat=31.975742453595963&cities=false&showPOI=false&limit=1575&minRent=0&maxRent=6000&searchTerms=Words+Required+In+Listing&maxPricePerBedroom=6000&minBR=0&maxBR=10&minBA=1&maxAge=7&imagesOnly=false&phoneReq=false&cats=false&dogs=false&noFee=false&showSubs=true&showNonSubs=true&showRooms=true&showVac=true&userId=-1&cl=true&pl=true&aptsrch=true&rnt=true&airbnb=true&ood=true&af=true&rltr=true&zoom=14&favsOnly=false&onlyHQ=true&showHidden=false&am=false&workplaceLat=0&workplaceLong=0&maxTime=0
#

#from script:
# https://www.padmapper.com/reloadMarkersJSON.php?
#&eastLong=35.017659208007785&northLat=32.16688183134553&westLong=34.523274442382785&southLat=31.975742453595963
#&cities=false&showPOI=false&limit=2000&maxRent=20000&minRent=0&searchTerms=&maxPricePerBedroom=20000&minBR=0&maxBR=10&minBA=1&maxAge=7&imagesOnly=false&phoneReq=false&cats=false&dogs=false&noFee=false&showSubs=true&showNonSubs=true&showRooms=true&userId=-1&cl=true&
# &showHidden=false&maxTime=0&workplaceLong=0&ood=true&apts=true&workplaceLat=0&onlyHQ=true&zoom=15&favsOnly=false

MAX_RENT=10000

DEFAULTS = {
    'cities': 'false',
    'showPOI': 'false',
    'limit': 2000,  #1575
    'minRent': 0,
    'maxRent': MAX_RENT,
    'searchTerms': '',                  #Words+Required+In+Listing
    'maxPricePerBedroom': MAX_RENT,
    'minBR': 0,
    'maxBR': 10,
    'minBA': 1,
    'maxAge': 7,
    'imagesOnly': 'false',
    'phoneReq': 'false',
    'cats': 'false',
    'dogs': 'false',
    'noFee': 'false',
    'showSubs': 'true',
    'showNonSubs': 'true',
    'showVac': 'true',            #was missing
    'showRooms': 'true',
    'userId': -1,
    'cl': 'true',
    'pl': 'true',                   #was missing
    'aptsrch': 'true',        #was missing
    'rnt': 'true',             #was missing
    'airbnb': 'true',       #was missing
    'af': 'true',      #was missing
    'rltr': 'true',      #was missing
    'am': 'false',     #was missing
    'apts': 'true',
    'ood': 'true',
    'zoom': '14',
    'favsOnly': 'false',
    'onlyHQ': 'true',           #what is it? maybe set to false?
    'showHidden': 'false',      #what is it? maybe set to true?
    'workplaceLat': 0,
    'workplaceLong': 0,
    'maxTime': 0
    }

def query(kwargs):
    assert 'eastLong' in kwargs
    assert 'northLat' in kwargs
    assert 'westLong' in kwargs
    assert 'southLat' in kwargs

    url='https://www.padmapper.com/reloadMarkersJSON.php'

    full_url = '%s?%s' % (url, '&'.join('%s=%s' % (k,v) for (k,v) in kwargs.items()))

    apts = []

    txt = ""
    try:
        txt = urllib.request.urlopen(full_url).read()
        ur = txt.decode('utf8')
        j = json.loads(ur)
    except Exception as e:
        print(e)
        print(txt)
        print("ERROR", full_url)
        return []

    for apartment in j:
        apts.append(( apartment['id'], apartment['lng'], apartment['lat'] ))

    assert len(apts) < kwargs['limit']-1

    return apts

def start():
    kwargs = dict((k,v) for (k,v) in DEFAULTS.items())
    kwargs['southLat']=MIN_LAT
    kwargs['westLong']=MIN_LON
    kwargs['northLat']=MAX_LAT
    kwargs['eastLong']=MAX_LON

    seen_ids = set()

    epoch_timestamp = int(time.mktime(time.gmtime()))
    with open("apts-%s.txt" % epoch_timestamp, 'w') as outf:
        for rent in range(1000,MAX_RENT,100):
            print("querying from %s ..." % rent)
            for bedrooms in range(10):
                kwargs['minRent'] = rent-100
                kwargs['maxRent'] = rent
                kwargs['minBR'] = bedrooms
                kwargs['maxBR'] = bedrooms

                for apt_id, lon, lat in query(kwargs):
                     if apt_id not in seen_ids:
                        outf.write("%s %s %s %s %s\n" % (
                              rent, bedrooms, apt_id, lon, lat))
                        sys.stdout.flush()
                        seen_ids.add(apt_id)

            time.sleep(1)


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
