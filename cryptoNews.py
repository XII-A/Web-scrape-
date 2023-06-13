from bs4 import BeautifulSoup
import requests
from timeit import default_timer as timer
from csv import writer

#Where all the article urls are stored
urls = [
        'https://www.coindesk.com/markets/2023/04/06/dogecoin-drops-after-elon-musks-twitter-stops-using-its-logo/',
        'https://cryptonews.com/news/digitoads-looks-primed-for-10x-growth-an-increased-number-of-decentraland-multiversx-holders-are-converting-over.htm',
        
    ]
# counting the pages
counter = 0
# to see how long the program took
start = timer()

def find_MetaTags(urls):
    with open(f'Webscrape_2\posts\SEO.csv','w' , encoding="utf-8" ,newline='') as f:
        thewriter = writer(f,)
        header = ['Title', 'Description','Publishing Date','url']
        thewriter.writerow(header)

        for url in urls:
            html_text = requests.get(url).text
            soup = BeautifulSoup(html_text , 'lxml')
            
            try:
                title = soup.find("meta", {"property": "og:title"}).attrs['content']
            except AttributeError:
                title = '404'
                
            try:
                description = soup.find("meta", {"property": "og:description"}).attrs['content']
            except AttributeError:
                description = soup.find("meta", {"name": "og:description"}).attrs['content']

            try:
                published_time = soup.find("meta", {"property": "article:published_time"}).attrs['content']
            except AttributeError:
                published_time = soup.find('time').attrs['datetime']

            info = [title,description,published_time,url]
            thewriter.writerow(info)



def getting_URLS(soups):
    global counter
    for soup in soups:
        enteries = soup.find_all("a")
        counter = counter + 1
        for entery in enteries:
            url = 'https://cryptonews.com' + str(entery.attrs['href'])
            urls.append(url)
            
    print(f'the final count is {counter}')

# https://cryptonews.com/paged/news-64.json is the last json file

def fetching_json(json_url):
    soups = [] #to collect all the parsed html from each json file
    page_num = 1
    html_page = '<div>'
    while page_num != 2:
        # returns an array with each element being a div element
        response = requests.get(json_url + str(page_num) + ".json").json()
        for index,item in enumerate(response): 
            html_page = html_page + '<div>' + response[index] + '</div>' + '\n'
        html_page += '</div>'

        
        print("-------------------------------------------")
        soup = BeautifulSoup(response[index] , 'lxml')
        print(soup.prettify)
        soups.append(soup)
        page_num = page_num + 1

    getting_URLS(soups)

if __name__ == "__main__": 
    # base url https://cryptonews.com/news/
    json_url = "https://cryptonews.com/paged/news-"
    
    fetching_json(json_url)
    
    # find_MetaTags(urls)
    
    elapsed_time = timer() - start # in seconds
    
    print(f'the program took {elapsed_time}')