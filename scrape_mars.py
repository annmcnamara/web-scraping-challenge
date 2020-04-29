from splinter import Browser
from bs4 import BeautifulSoup 
import pandas as pd
import time
import re

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    # return Browser("chrome", **executable_path, headless=False)
    return Browser("chrome", "/usr/local/bin/chromedriver", headless=True)  # set headless to False to open pages

def scrape_site(url, browser):
    browser.visit(url)
    time.sleep(5)
    # scrape and parse the data
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def scrape_news(mars_data, browser):
    soup = scrape_site('https://mars.nasa.gov/news/', browser)


    if (browser.is_element_present_by_tag('li', wait_time=10)):
        latest_news = soup.find('li', class_="slide")
        # Locate the object containing the news data
        mars_data["headline"] = soup.find('li',class_="slide").h3.text
        mars_data["news_p"]   = latest_news.find('div', class_= 'article_teaser_body').text
    
    else:
        mars_data["headline"] = "https://mars.nasa.gov/news/ Headline Not Found"
        mars_data["news_p  "] = "https://mars.nasa.gov/news/ News Teaser Not Found"


    return mars_data

def scrape_twitter(mars_data, browser):
    soup = scrape_site('https://twitter.com/marswxreport?lang=en', browser)

    if (browser.is_element_present_by_tag('div', wait_time=5)):
        tweet = soup.find('div',class_="css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
        mars_weather = tweet.text

        mars_data["weather"] = mars_weather
    else: 
        mars_data["weather"] = "https://twitter.com/marswxreport?lang=en Weather Not Found"

    return mars_data

def scrape_featured(mars_data, browser):
    soup = scrape_site('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars', browser)

    if (browser.is_element_present_by_tag('div', wait_time=5)):
        header = soup.find('div', class_="brand2")
        base_url ="http:"+header.a['href']

        # Locate the object containing the link
        if (browser.is_element_present_by_tag('article', wait_time=5)):
            space_images = soup.find('article', class_="carousel_item")
            style =  space_images['style']

            #strip url 
            start = style.find('/')
            end    = style.find('\')')
            image_link = style[start+1:end]

            ### Concatenate base and link to get entire link to image
            featured_image_url = base_url + image_link

            mars_data["featured_image"] = featured_image_url
        else:
            mars_data["featured_image"] = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars Image Not Found"
    return mars_data

def scrape_table_data(mars_data, browser):
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(2)
    if (browser.is_element_present_by_tag('table', wait_time=5)):
        tables = pd.read_html(url)

        df = tables[0]
        df.columns = ['Attribute', 'Data']
        table_html = df.to_html(index=False)

        mars_data['table'] = table_html
    else: 
        mars_data['table'] = 'https://space-facts.com/mars/ table not found'

    return mars_data

def scrape_hemisphere_images(mars_data, browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    driver = browser.driver
    full_url = driver.current_url
    time.sleep(5)
    # strip out after third /
    base_url = full_url.rsplit('/',2)[0]

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    if (browser.is_element_present_by_tag('div', wait_time=5)):
        image_links = soup.find_all('div', class_="description")
    
    # for p in image_links:
    #     print(p.a.text)
    #     print(p.a['href'])
    #     print('\n')

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
        if (browser.is_element_present_by_tag('div', wait_time=5)):
            image_links = soup.find_all('div', class_="downloads")
            dict_item = {'title':title, 'img_url':image_links[0].a['href']}
            hemisphere_image_urls.append(dict_item)
            mars_data["hemisphere_image_urls"]    = hemisphere_image_urls
        else:
            mars_data["hemisphere_image_urls"]    = f"{img_url} not reached"
    return mars_data

def scrape():
    browser = init_browser()

    mars_data = {}

    # # SCRAPE THE LATEST NEWS FROM 'https://mars.nasa.gov/news/'
    mars_data = scrape_news(mars_data,browser)
    
    # SCRAPE THE WEATHER FROM 'https://twitter.com/marswxreport?lang=en'
    mars_data = scrape_twitter(mars_data, browser)

    # SCRAPE THE IMAGE FROM 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    mars_data = scrape_featured(mars_data, browser)
  
    # SCRAPE THE TABLE DATA 'https://space-facts.com/mars/'
    mars_data = scrape_table_data(mars_data, browser)

    # SCRAPE THE HEMISPHERE IMAGES FROM 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    mars_data = scrape_hemisphere_images(mars_data, browser)

    return mars_data 


# To enable testingJ
if __name__ == "__main__":
    print("\nTesting Data Retrieval:....\n")
    print(scrape())    
