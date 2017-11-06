# SonaScraper
Web scrapper for automatically signing up to surveys on WLU Sona

# Dependencies
1. Install python 2.7 https://www.python.org/downloads/
2. Install pip https://pip.pypa.io/en/stable/installing/
3. Install virtualenv & virtualenvwrapper http://docs.python-guide.org/en/latest/dev/virtualenvs/

# Setup Virtual Environment
1. `mkvirtualenv sona`
2. `workon sona`

# Installation
1. `git clone git@github.com:mattBlackDesign/SonaScraper.git`
2. `cd SonaScraper`
3. `cp sona_scraper/settings.default.py sona_scraper/settings.py`
4. Edit settings.py
5. `scrapy crawl sona`

### Learning Resources 
https://doc.scrapy.org/en/latest/
