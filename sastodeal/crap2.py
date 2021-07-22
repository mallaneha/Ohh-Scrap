# List of available books (on the site) with their price is stored in csv

import requests
from bs4 import BeautifulSoup
import csv


SITE = "https://www.sastodeal.com"
wishList = ['before the coffee gets cold', 
            'the bell jar', 
            'mrs dalloway', 
            'never let me go', 
            'pachinko', 
            'the master and margarita', 
            'killing commendatore', 
            'normal people', 
            'the wind-up bird chronicle',
            'the midnight library',
            'emma', 
            'animal farm',
            'all the light we cannot see',
            'the boy in the striped pyjamas']
            
availableBooks = []
notAvailableBooks = []

for i, item in enumerate(wishList):
    search = item.replace(' ', '+')
    URL = SITE + "/catalogsearch/result/?q=" + search
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')

    div = soup.find('ol', attrs = {'class':'products list items product-items'})
    
    if div == None:
        notAvailableBooks.append([i, item])
        # print('chainaaaaaaaaaaaaaaaaaaaaaa')
        continue
    
    table = div.findAll('div', attrs = {'class':'product details product-item-details'})
    
    availability = False
    for row in table:
        book = {}

        if item in row.a.text.lower():
            availability = True
            
            book['number'] = i + 1
            book['title'] = row.a.text
            book['price'] = row.find('span', attrs = {'data-price-type':'finalPrice'}).span.text
            
            availableBooks.append(book)
    
    if availability == False:
        notAvailableBooks.append([i, item])

print(notAvailableBooks)
print(len(availableBooks))

filename = 'wishListBooks.csv'
with open(filename, 'w', newline='', encoding = 'utf-8') as f:
    w = csv.DictWriter(f,['number', 'title', 'price'])
    w.writeheader()
    for book in availableBooks:
        w.writerow(book)
