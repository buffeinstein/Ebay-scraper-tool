import argparse
import requests
from bs4 import BeautifulSoup
import json 
import csv

###############################################################################################
#1) Use argpasrse to get a search term from command line 
###############################################################################################

#remember to put quotation marks around a search term with a space in it

parser = argparse.ArgumentParser(description='download Ebay info, convert to JSON')

#change what item you search for 
parser.add_argument('search_term')

#change how many pages of ebay you parse through
parser.add_argument('--page_number', default=10)
#having -- in front means you can set a default value for this argument if nothing is passed into the command line

#change if you want to store as csv file instead of json
parser.add_argument('--csv', action = 'store_true')

args = parser.parse_args()

#remind user of what they inputed
print('searching for:', args.search_term)
print ('going up till page:', args.page_number)
if args.csv == True:
    print ('saving as: csv')
else: 
    print ('saving as: json')
#going to make a list of dictionaries of items
items = []

#a function to get price, shipping costs, and items sold as an int 
def getintcost(text):
    cost = " "
    if text == "Free shipping":
        cost = 0 
        return cost
    elif "to" in text: 
        for i,char in enumerate(text):
            if char.isdigit():
                cost += char
                if text[i+1] == " ": 
                    break
    elif "sold" in text: 
         for i,char in enumerate(text):
            if char.isdigit():
                cost += char
                if text[i+1] == "+": 
                    break
    else:
        for i,char in enumerate(text):
            if char.isdigit():
                cost += char
    return int(cost)
   
###############################################################################################
#2) Use the requests library to download the first 10 webpage results for your search term     
###############################################################################################  

####THIS GOES THRU ONE PAGE of ebay AT AT TIME
for page_number in range(1,int(args.page_number)+1):
    #make the url by plugging in serch term and page number 
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw='
    url += args.search_term
    url += '&_sacat=0&_pgn='
    url += str(page_number)
    #print('url = ', url)

    #download the html from the url
    r = requests.get(url)
    status = r.status_code 
    #200 means success
    #print ('status:', status)
    html = r.text
    #print ('html:', html[:50])

###############################################################################################
#3) Use bs4 to extract all of the items returned in the search results
 ###############################################################################################

    # we're inside the for loop for one page 
    soup = BeautifulSoup(html, 'html.parser')
    #check out scrapingnotes.py in week8

    # ALL ITEMS ON the ONE PAGE youre on###
    itemtags = soup.select('.s-item')

###############################################################################################
#4) Create a python list of the extracted items, where each entry in the list is a dictionary. 
###############################################################################################
  
    #still inside the for loop - IN ALL ITEMS - ON ONE PAGE AT A TIME
    for item in itemtags:    

        #inside 2 two for loops now, ONE ITEM - IN ALL ITEMS - ON ONE PAGE AT A TIME

        #name
        name = None
        nametags = item.select('.s-item__title')
        for name in nametags: 
            name = name.text
        #print ('name:', name)

        #lowest price in cents 
        # (so that it can be saved as int instead of float)
        price = None
        pricetags = item.select('.s-item__price')
        for price in pricetags: 
            price = price.text
            #print ('price text:', price)
            price = getintcost(price)
        #print ('lowest price in cents:', (price))
         
        #owned status
        ownedstatus = None
        ownedstatustags = item.select('.s-item__subtitle')
        for ownedstatus in ownedstatustags:
            ownedstatus = ownedstatus.text
        #print ('owned status:', ownedstatus)

        #shipping cost in cents
        shippingcost = None
        shippingtags = item.select('.s-item__shipping')
        for shippingcost in shippingtags: 
            shippingcost = shippingcost.text
            shippingcost = getintcost(shippingcost)
        #print ('shipping cost in cents:', shippingcost)
        
        #free return boolean 
        freereturnstatus = False
        freereturntags = item.select('.s-item__free-returns')
        for tag in freereturntags: 
            freereturnstatus = True
        #print ('free return status:', freereturnstatus)

        #items sold
        itemssold = None
        itemssoldtags = item.select('.s-item__hotness')
        for itemssold in itemssoldtags: 
            itemssold = itemssold.text
            #print ('items sold text:', itemssold)
            if "sold" not in itemssold:
                itemssold = None
            else: 
                itemssold = getintcost(itemssold)
        #print ('items sold:', itemssold)

        #print ('\n\n')

        item = {
            'name': name, 
            'lowest price in cents': price, 
            'owned status': ownedstatus, 
            'shipping cost in cents': shippingcost, 
            'free return status': freereturnstatus, 
            'items sold': itemssold
        }
        
        items.append(item)

for item in items: 
    if "Shop on eBay" in item.values():
        items.remove(item)

# print ('amount of dictionaries:', len(items))
# print ('amount of items:', len(itemtags))

###############################################################################################
#5) Use the json library to save the list as a json file named SEARCH_TERM.json,
#  where SEARCH_TERM should be replaced by the search term passed in on the command line.
###############################################################################################

###############################################################################################
#6) EXTRA CREDIT: save as csv file instead of json
###############################################################################################


#parser.add_argument('--csv', action = 'store_true')
if args.csv == True:
    filename = args.search_term + '.csv'
    with open(filename, 'w', encoding = 'utf-8') as f:
        for item in items:
            fields = (item.keys())
            row = (item.values())
            writer = csv.writer(f)
            writer.writerow(fields)
            writer.writerow(row)
else: 
    filename = args.search_term + '.json'
    with open(filename,'w', encoding ='ascii') as f:
        f.write(json.dumps(items))
