# -*- coding: <encoding name> -*-
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url  = 'https://store.steampowered.com/search/?specials=1'
currentPage = 1
fileName = "Steam_Sales.csv"
f = open(fileName, "w")
headers = "Title, Release Date, Discount, Original Price, Sale Price"
f.write(headers + "\n")

def Scrape(my_url):

 
    #Adding our webpage and then opening it.
    uClient = uReq(my_url)
    page_html = uClient.read()
    #Close the connection
    uClient.close()
    #HTML Parse
    page_soup = soup(page_html, "html.parser")
    #Specials section of Steam
    #deals = page_soup.findAll("div", {"id":"search_results"})
    products = page_soup.findAll("div", {"id":"search_result_container"})
    products = products[0].findAll("div", class_= False, id=False)
    products = products[0].findAll("a")
    i = 0

    for product in products:
        if (i <= len(products)):
            
            titleholder = product.findAll("span", {"class":"title"})
            title = titleholder[0].text
            
            releaseDateHolder = product.findAll("div", {"class": "col search_released responsive_secondrow"})
            releaseDate = releaseDateHolder[0].text
            discountHolder = product.findAll("div", {"class":"col search_discount responsive_secondrow"})
            discountHolder = discountHolder[0].text.strip()
            discountPercent = discountHolder
            PriceHolder = product.findAll("div", {"class":"col search_price discounted responsive_secondrow"})
            try:
                PriceHolder = PriceHolder[0].text
                PriceHolder = PriceHolder.split("$")
                normalPrice = PriceHolder[1]
                discountedPrice = PriceHolder[-1] 
            except IndexError:
                normalPrice = "NULL";
                discountedPrice = "NULL"
   
            print ("Title: " + title)
            print ("Release Date: " + releaseDate)
            print ("Original Price: " + normalPrice)
            print ("Discounted Price: " + discountedPrice)
            print ("Discount Percentage: " + discountPercent)
            i += 1
            try:
                #writing info to file
                f.write(title.replace(",","") + "," + releaseDate.replace(",","") + "," + discountPercent + "," + normalPrice + "," + discountedPrice + "\n")
            except UnicodeError:
                #handeling unknown characters
                title = title.encode('utf-8')
                f.write(str(title) + "," + releaseDate.replace(",","") + "," + discountPercent + "," + normalPrice + "," + discountedPrice + "\n")
                

           
            if (i >= len(products)):
                global currentPage
                numbers = page_soup.findAll("div", {"id":"search_result_container"})
                maxPage = numbers[0].findAll("div", {"class": "search_pagination"})
                maxPage = maxPage[0].findAll("div", {"class": "search_pagination_right"})
                maxPage = maxPage[0].findAll("a")
                maxPage = maxPage[len(maxPage)-2:-1]
                maxPage = maxPage[0].text
                nextPageToGo = currentPage + 1
                my_url = "https://store.steampowered.com/search/?sort_by=&sort_order=0&special_categories=&specials=1&page=" + str(nextPageToGo)  
                currentPage = currentPage + 1
                i=0
                print(my_url)
                print(maxPage)                
                if (nextPageToGo <= int(maxPage)):
                    Scrape(my_url)
                else:
                    f.close()


Scrape(my_url)