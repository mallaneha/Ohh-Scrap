# best books of 2020 from each genre with their respective votes

import requests
from bs4 import BeautifulSoup
import csv


SITE = "https://www.goodreads.com"
URL = "https://www.goodreads.com/choiceawards/best-books-2020"
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html5lib')

div = soup.find('div', attrs = {'class':'clearFix'})
table = div.findAll('div', attrs = {'class':'category clearFix'})

books = []
for row in table:
    # print(row.prettify())
    book = {}
    book['genre'] = row.h4.text.strip('\n')
    book['title'] = row.img['alt']
    
    URLb = SITE + row.a['href']
    rb = requests.get(URLb)
    soupb = BeautifulSoup(rb.content, 'html5lib')
    vote = soupb.find('div', attrs = {'class':'gcaWinnerHeader'})
    book['vote'] = vote.span.text.strip('\n')

    books.append(book)
    # print(book, end = '\n'*2)

sortedBooks = sorted(books, key = lambda x: x['vote'], reverse = True)
# print(sortedBooks)

filename = 'bestBooks2020Sorted.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f,['genre','title', 'vote'])
    w.writeheader()
    for book in sortedBooks:
        w.writerow(book)
