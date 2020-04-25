from splinter import Browser
from bs4 import BeautifulSoup 
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    # return Browser("chrome", **executable_path, headless=False)
    return Browser("chrome", "/usr/local/bin/chromedriver", headless=False)

def scrape():
    browser = init_browser()


    # SCRAPE THE LATEST NEWS FROM 'https://mars.nasa.gov/news/'
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
    #print(f"{start}  {end}")
    image_link = style[start+1:end]
    # print (image_link)
    ### Concatenate base and link to get entire link to image
    featured_image_url = base_url + image_link

    mars_data["featured_image"] = featured_image_url

    return mars_data 


# To enable testingJ
if __name__ == "__main__":
    print("\nTesting Data Retrieval:....\n")
    print(scrape())    
