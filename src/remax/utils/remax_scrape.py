from scraping_utils import *
import pandas as pd 
import argparse
from bs4 import BeautifulSoup
import time
#import urllib3

#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# defining argparse
parser = argparse.ArgumentParser(description='Process some arguments')

parser.add_argument('--city',metavar='C',type=str,help='city that you want to scrape e.g. "charlotte" ')
parser.add_argument('--state',metavar='S',type=str,help='two letter abbrv of the state of the city you want to scrape e.g. "NC"')

arg_check = parser.parse_args()
args = vars(parser.parse_args())

def scrapeRemax(city,state):
    d={}
    for pg in xrange(1,140):
        print('scraping page %s') % (str(pg))
        page = createRemaxCityURL(city,state,pg)
        urls = findReMaxURLS(BeautifulSoup(get(page,verify=False).text,'html.parser'))
        for url in urls:
            print('napping for five seconds')
            time.sleep(5)
            home = pullHomeData(url)
            flat = flatten_dict(home)
            slug = flat['address_slug']
            d[slug] = flat
    df = pd.DataFrame.from_dict(d,orient='index')
    df.to_csv('sample.csv',encoding='utf-8')



if __name__ == '__main__':
    if arg_check.city == 'check_string_for_empty':
        print('you didnt supply a city.  please try again.')
    if arg_check.state == 'check_string_for_empty':
        print('you didnt supply a state.  please try again')
    city=args['city']
    state=args['state']
    print('scraping home data for %s, %s :  time elapsed is...') % (city, state)

    scrapeRemax(city,state)
