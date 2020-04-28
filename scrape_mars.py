from splinter import Browser
from bs4 import BeautifulSoup 
import pandas as pd
import time
import re

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    # return Browser("chrome", **executable_path, headless=False)
    return Browser("chrome", "/usr/local/bin/chromedriver", headless=False)

def scrape():
    browser = init_browser()

    # # SCRAPE THE LATEST NEWS FROM 'https://mars.nasa.gov/news/'
    mars_data = {}

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)
    # scrape and parse the data
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Locate the object containing the news data
    mars_data["headline"] = soup.find('div',class_="image_and_description_container").h3.text
    mars_data["news_p"]   = soup.find('div',class_="image_and_description_container").get_text()
    
    # SCRAPE THE WEATHER FROM 'https://twitter.com/marswxreport?lang=en'
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    tweet = soup.find('div',class_="css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    mars_weather = tweet.text

    mars_data["weather"] = mars_weather


    # SCRAPE THE IMAGE FROM 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(5)

    # scrape and parse the data
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    header = soup.find('div', class_="brand2")
    base_url ="http:"+header.a['href']

    # Locate the object containing the link
    space_images = soup.find('article', class_="carousel_item")
    style =  space_images['style']

    #strip url 
    start = style.find('/')
    end    = style.find('\')')
    image_link = style[start+1:end]

    ### Concatenate base and link to get entire link to image
    featured_image_url = base_url + image_link

    mars_data["featured_image"] = featured_image_url


    # SCRAPE THE TABLE DATA
    ## set the url and open the web page
    ## so we can scrape the data
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(5)
    tables = pd.read_html(url)
    

    df = tables[0]
    df.columns = ['Attribute', 'Data']

    #table_html = df.to_html(classes='table')

    #table_html = re.sub("class=\"dataframe ", "class=\"", df.head(5).to_html(classes='table'))

    table_html = re.sub("border=\"1\" class=\"dataframe ", "class=\"", df.head(10).to_html(classes='table'))
    table_html = table_html.replace('\n', ' ')


    print(table_html)
  
    mars_data['table'] = table_html


    # SCRAPE THE HEMISPHERE IMAGES FROM 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    driver = browser.driver
    full_url = driver.current_url
    time.sleep(5)
    # strip out after third /
    base_url = full_url.rsplit('/',2)[0]

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image_links = soup.find_all('div', class_="description")
    for p in image_links:
        print(p.a.text)
        print(p.a['href'])
        print('\n')

    image_urls = []

    for image in image_links:
        #print(image.a.text.replace(' Enhanced', ""))   
        title = image.a.text.replace(' Enhanced', "")
        dict_item = {'title':title, 'img_url':base_url+image.a['href']}
        image_urls.append(dict_item)
    
    hemisphere_image_urls = []
    for img_url in image_urls: 
        url   = img_url['img_url']
        title = img_url['title']
        browser.visit(url)
        time.sleep(3)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
    
        image_links = soup.find_all('div', class_="downloads")
        dict_item = {'title':title, 'img_url':image_links[0].a['href']}
        hemisphere_image_urls.append(dict_item)

    for i in hemisphere_image_urls:
        print(i['title'])
        print(i['img_url'])


    mars_data["hemisphere_image_urls"]    = hemisphere_image_urls

    # print (f" CHECK {mars_data.hemisphere_image_urls[0]} \n")

    print("SCRAPED :-) \n\n")
    return mars_data 



# To enable testingJ
if __name__ == "__main__":
    print("\nTesting Data Retrieval:....\n")
    print(scrape())    
