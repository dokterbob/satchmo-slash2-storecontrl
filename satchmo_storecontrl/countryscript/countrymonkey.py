import pprint
import csv
import gettext
import pycountry

lang = gettext.translation('iso3166', pycountry.LOCALES_DIR,     
                           languages=['nl'])
lang.install()

reader = csv.DictReader(open('landen.csv', 'rb'), delimiter=';')

clist = {}

for row in reader:
    slashid = row['ID']
    dutchname = row['Land']    

    match = False    
    
    for country in pycountry.countries:
        transname = _(country.name)
        
        if dutchname == transname:
            print slashid, dutchname, country.alpha2
            
            clist[country.alpha2] = slashid
            
            match = True
            break
    
    if not match:
        print 'No match for %s' % dutchname

pprint.pprint(clist)

