import os
import sys
from bs4 import BeautifulSoup
from requests import get
import requests
from datetime import datetime, timedelta
import time
import argparse


parser = argparse.ArgumentParser(description='Process some arguments')

parser.add_argument('--csv_path',metavar='C',type=str,help='city that you want to scrape e.g. "charlotte" ')
parser.add_argument('--sort_method',metavar='S',type=str,help='two letter abbrv of the state of the city you want to scrape e.g. "NC"')

