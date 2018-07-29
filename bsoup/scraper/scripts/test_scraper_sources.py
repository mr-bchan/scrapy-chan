import sys
sys.path.insert(0,'.')

import bsoup.scraper.rappler as scraper

test_url = 'https://www.rappler.com/nation/208139-filipinos-sentiment-duterte-insulting-un-rights-chief-sws-survey-june-2018'
data = scraper.scrape(test_url)
print(data)