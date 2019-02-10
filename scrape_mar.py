from bs4 import BeautifulSoup
import requests
from splinter import Browser
import time
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser=init_browser()

    url='https://mars.nasa.gov/news'
    browser.visit (url)

    time.sleep(1)

    html1 = browser.html
    soup1 = BeautifulSoup(html1, 'html.parser')

    nasa_titles=[]
    nasa_description=[]
    results1= soup1.find_all('div', class_='list_text')
    for item in results1:
        title=item.a.text
        desc=item.find(class_='article_teaser_body').text
        nasa_titles.append(title)
        nasa_description.append(desc)

    # Featured_url
    browser=init_browser()

    featured_image_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_image_url)

    time.sleep(1)

    html_featured=browser.html
    soup_featured= BeautifulSoup(html_featured, 'html.parser')

    
    results_featured=soup_featured.find_all('div', class_='carousel_items')
    for featured in results_featured:
        partial_url=featured.article['style'].strip()
        par_url=partial_url.split("'")
        featured_full_url=f'https://www.jpl.nasa.gov{par_url[1]}'


    # latest weather
    browser=init_browser()
    mars_twitter='https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_twitter)

    time.sleep(1)

    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')

    tweets=soup2.find_all('p', class_='TweetTextSize')

    for tweet in tweets:
        mars_weather=tweet.text.strip()
        if "pressure" not in mars_weather:
            continue
        else:
            if "pic.twitter" in mars_weather:
                weather=mars_weather.split('pic')
                weather_mars=weather[0]
            break

    # Mars facts
    browser=init_browser()
    facts_url='https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    time.sleep(1)
    df_facts=tables[0]
    df_facts.rename(columns={0:'Paramter', 1:'Value'}, inplace=True)
    html_table = df_facts.to_html(index=False)
    facts_table=html_table.replace('\n', '').strip()

    # Mars hemispheres
    browser=init_browser()
    hemispheres_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    time.sleep(1)

    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')
    hemispheres_results=soup3.find_all('div', class_='item')

    hemi_base_url='https://astrogeology.usgs.gov'
    hemi_links_full=[]
    for hemi in hemispheres_results:
        hemi_link=hemi.a['href']
        hemi_url=f'{hemi_base_url}{hemi_link}'
        hemi_links_full.append(hemi_url)

    hemispheres=[]
    hemi_dict={}
    for links in hemi_links_full:
        browser.visit(links)
        html4=browser.html
        soup4 = BeautifulSoup(html4, 'html.parser')
        hemi_pic_results=soup4.find_all('div', class_='downloads')
        hemi_title_results=soup4.find_all('section', class_='block metadata')
        
        for hemi_title in hemi_title_results:
            hemi_dict['title']=hemi_title.h2.text.strip()
        
        for hemi_pic in hemi_pic_results:
            hemi_dict['img_urls']=hemi_pic.ul.li.a['href']
        
            hemispheres.append(hemi_dict.copy())






    data_scraped={
        'article_titles': nasa_titles[0],
        'article_description': nasa_description[0],
        'featured_url':featured_full_url,
        'weather': weather_mars,
        'facts': facts_table,
        'hemis_data':hemispheres
    }


    browser.quit()
    return data_scraped







