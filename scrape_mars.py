from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import os
import pandas as pd
import time 
import requests

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
 #_________________________________________________ NASA MARS NEWS ______________________________________________________________________________________________

    # Webpage to scrape
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(1)

     # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Collect title 
    news_title = soup.find('div', class_='content_title').text

    # Collect subtitle
    news_paragraph = soup.find('div', class_='rollover_description_inner').text

 #______________________________________________ JPL MARS SPACE IMAGES - FEATURED IMAGE _________________________________________________________________________

    # Open Browser
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Browser visits site
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    time.sleep(1)

    # Browser clicks FULL IMAGE button
    browser.click_link_by_partial_text('FULL')

    # Create url string variable
    page_url = browser.html

    # Create soup object
    soup = bs(page_url, 'html.parser')

    # Close the browser
    browser.quit()

    # Collect featured image url
    image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    
    # Define the base url
    base_url = 'https://www.jpl.nasa.gov'

    # Combine two url into one
    featured_image_url = base_url + image_url

 #________________________________________________ MARS WEATHER _________________________________________________________________________________________________

    weather_url = 'https://twitter.com/marswxreport?lang=en'
    response_w = requests.get(weather_url)
    soup = bs(response_w.text, 'html.parser')
    results = soup.find('div', class_='stream').ol.find_all('li', class_='js-stream-item stream-item stream-item')

    for result in results:
        if result.find('div', class_='js-tweet-text-container').find('p', class_='TweetTextSize').text[:3] == 'Sol':
            mars_weather_tag = result.find('div', class_='js-tweet-text-container').find('p', class_='TweetTextSize')
        
            mars_weather = mars_weather_tag.text.replace(mars_weather_tag.a.text, '')
            break

  #________________________________________________ MARS FACTS ____________________________________________________________________________________________________

    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns=['Feature', 'info']
    df.set_index('Feature', inplace=True)

    facts_html_table = df.to_html()
    
    #_______________________________________________ MARS HEMISPHERES_______________________________________________________________________________________________

    mars_imgs = [
        {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
        {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"}
        ]

    #____________________________________________ SAVE ALL DATA IN DICTIONARY ______________________________________________________________________________________
    mars_data = {
        'news_title': news_title ,
        'news_paragraph': news_paragraph,
        'featured_image_url': featured_image_url,
        'mars_weather': mars_weather,
        'facts_html_table': facts_html_table, 
        'mars_imgs': mars_imgs
    }

    # Close the browser 
    browser.quit()
    # Return results
    return mars_data

    