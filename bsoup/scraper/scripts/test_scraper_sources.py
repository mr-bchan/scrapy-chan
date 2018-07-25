import sys
sys.path.insert(0,'.')

import bsoup.scraper.abscbn as scraper

data = scraper.scrape('http://news.abscbn.com/news/01/05/18/2-sugatan-sa-pag-araro-ng-trak-sa-karinderya-tindahan-sa-jaro.html')
print(data)