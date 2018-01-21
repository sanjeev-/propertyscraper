import os
import sys
from bs4 import BeautifulSoup
from requests import get







def findReMaxURLS(soup):
    """
    soup:  bs4 soup -  BeautifulSoup object of a url of a remax search result page
    BASE_URL: string - the beginning of the URL that remax uses
    -
    returns: list - a list of all URLs of homes on the given page  
    """
    BASE_URL='https://leadingedge-northcarolina.remax.com'
    remax_urls = []
    linksoup = soup.find_all('a',class_='listing-pane-info js-detaillink')
    for crouton in linksoup:
        remax_urls.append(BASE_URL+crouton['href'])
    return remax_urls


def pullHomeData(home_url):
"""
home_url - string: url of the remax home from which we wish to extract data

- 
returns: home_dict: dict {

        address:{

                address_line1: string - street number, street
                address_line2: string - optional, apartment number, extra info
                state: string - state abbreviation (two letter)
                country: string - country str
                zipcode: int - five number zipcode
                }
                
        listing_data: {
        
                list_price: int - home listing price (in USD)
                num_bedrooms: float - number of bedrooms (1 decimal)
                num_bathrooms: float - number of bathrooms (1 decimal)
                building_area_sq_ft: positive int in SQUARE FEET
        
        }
        
        valuation: {
      
        }
        
        features: {
            
            lot_size: float - size of the yard, in ACRES
            floors: int - number of floors of the house
            garage: int - is there a garage (not quite sure what this one is tbh)
            date_listed_on_site: [datetime] date that the house was listed on the site 
            school: [text] - average rating of all nearby schools
            coords: [tuple] a tuple of the latitude and longitude of the address
            desc: [text] a paragraph description of the home
            mls: [int] MLS listing number
            recent_selling_history: [list of tuples] list of tuples of buying history
            is_foreclosure: [boolean] is this a foreclosure home?
            
        }
        
        images: {
        
            image_list: list - a list of all the image urls associated with this house
        
        }
}       

"""
	address = {}
	homesoup = BeautifulSoup(get(home_url).text,'html.parser')
	address['address_line1']  = homesoup.find_all('li',attrs={'hmsitemprop':'Address'})[0].text.strip()
	address['city']  = homesoup.find_all('li',attrs={'hmsitemprop':'City'})[0].text.strip()
	address['state']  = homesoup.find_all('li',attrs={'hmsitemprop':'State'})[0].text.strip()
	address['zipcode']  = homesoup.find_all('li',attrs={'hmsitemprop':'Zip'})[0].text.strip()

	listing_data = {}
	listing_data['num_bedrooms'] = int(homesoup.find_all('span',class_='listing-detail-beds-val')[0].text.strip())
	listing_data['num_bathrooms'] = int(homesoup.find_all('span',class_='listing-detail-baths-val')[0].text.strip())
	listing_data['building_area_sq_ft'] = int(homesoup.find_all('span',class_='listing-detail-sqft-val')[0].text.strip().replace(',',''))
	listing_data['list_price'] = int(homesoup.find_all('span',class_='listing-detail-price-amount  pad-half-right')[0].text.strip().replace(',',''))

	features = {}
	features['MLS'] = int(homesoup.find_all('li',attrs={'hmsitemprop':'MLSNumber'})[0].text.strip())
	features['is_foreclosure'] = str(house_soup.find_all('li',attrs={'hmsitemprop':'IsForeclosure'})[0].text.strip()) == 'True'
	features['desc'] = homesoup.find_all('p',class_="listing-bio")[0].text.strip()
	features['year_built'] = findYearBuilt(homesoup)
	features['']





	images={}
	images['img_urls'] = pullImageURLSFromSlideshow(homesoup)

	home_dict = {}
	home_dict['address'] = address
	home_dict['listing_data'] = listing_data
	home_dict['images'] = images
	home_dict['features'] = features



	return home_dict




def pullImageURLSFromSlideshow(soup):
    """
    soup: [bs4 soup object]  the soup object of the website that we are going to be scraping from.
    
    returns: [list] a list of urls of images of the house of a given webpage
    """
    imglist = []
    for noodle in soup.find_all('figure',class_='figure figure__slideshow'):
        if len(noodle) == 3:
            imglist.append(noodle['data-href'])
    return imglist


def findYearBuilt(soup):
    """
    soup: [bs4 soup obj] the soup obj of webpage to scrape
    
    returns: [int] year the house was built
    
    """

    for idx, noodle in enumerate(house_soup.find_all('dt',class_='listing-detail-stats-main-key')):
        if 'Year Built' in noodle.text.strip():
            data = house_soup.find_all('dd',class_="listing-detail-stats-main-val")[idx]
            data= data.text.strip()
    return data